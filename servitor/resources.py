# -*- coding: utf-8 -*-
import logging

import docker
from docker.tls import TLSConfig
from flask import request
from flask_restful import Resource, abort

import config

logger = logging.getLogger(__name__)


def get_service_image(service):
    return service.attrs["Spec"]["TaskTemplate"]["ContainerSpec"]["Image"]


class Swarm(object):
    def __init__(self, key):
        logger.debug(f"Initializing swarm: {key}")
        try:
            swarm = config.DOCKER_SWARMS[key]

        except KeyError:
            logger.warn(f"Invalid swarm: {key}")
            abort(404)

        kwargs = {}

        tls_config = swarm.get("tls", False)
        if tls_config:
            kwargs["tls"] = TLSConfig(
                client_cert=(tls_config["cert"], tls_config["key"]))

        self.client = docker.DockerClient(base_url=swarm["url"], **kwargs)

    def get_service(self, name):
        # Service filters match substrings, this must return exactly one match.
        services = self.client.services.list()
        matches = [service for service in services if service.name == name]

        if not len(matches):
            abort(404)

        else:
            return matches[0]

    def get_stack_services(self, name):
        try:
            targets = config.DOCKER_STACKS[name]

        except KeyError:
            abort(404)

        services = self.client.services.list(filters={
            "label": f"com.docker.stack.namespace={name}"
        })
        return [service for service in services if service.name in targets]


class TokenMixin(object):
    def __init__(self):
        super().__init__()

        token = request.args.get("token", "")
        if token != config.TOKEN:
            logger.warn(f"Invalid request token: {token!r}")
            abort(403)


class Service(Resource, TokenMixin):
    def get(self, env, name):
        logger.info(f"Fetching service: {name}, env: {env}")

        swarm = Swarm(env)
        service = swarm.get_service(name)

        image = get_service_image(service)
        return ({service.name: image}, 200)

    def post(self, env, name):
        logger.info(f"Updating service: {name}, env: {env}")

        image = request.args.get("image")
        if not image:
            logger.warn("No image supplied")
            abort(400)

        swarm = Swarm(env)
        service = swarm.get_service(name)

        service.update(image=image)
        return ("ok", 200)


class Stack(Resource, TokenMixin):
    def get(self, env, name):
        logger.info(f"Fetching stack: {name}, env: {env}")

        swarm = Swarm(env)
        services = swarm.get_stack_services(name)

        images = {
            service.name: get_service_image(service)
            for service in services
        }
        return (images, 200)

    def post(self, env, name):
        logger.info(f"Updating stack: {name}, env: {env}")

        image = request.args.get("image")
        if not image:
            logger.warn("No image supplied")
            abort(400)

        swarm = Swarm(env)
        services = swarm.get_stack_services(name)

        for service in services:
            service.update(image=image)

        return ("ok", 200)
