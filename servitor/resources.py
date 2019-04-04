# -*- coding: utf-8 -*-
import logging
import re

from flask import request
from flask_restful import Resource, abort

from . import settings
from .docker import Swarm

logger = logging.getLogger(__name__)


def image_parts(image):
    match = re.match(r'^(?P<name>.*?):(?P<tag>[^@:]+)(?:@[\w:]+)?$', image)

    if not match:
        raise ValueError('Unable to parse image spec')
    else:
        return match.groups()


class TokenMixin(object):
    def __init__(self):
        super().__init__()

        token = request.args.get("token", "")
        if token != settings.TOKEN:
            logger.warn(f"Invalid request token: {token!r}")
            abort(403)


class Service(Resource, TokenMixin):
    def get(self, env, name):
        logger.info(f"Fetching service: {name}, env: {env}")

        swarm = Swarm(env)
        service = swarm.get_service(name)

        image = swarm.get_service_image(service)
        return (image, 200)

    def put(self, env, name):
        logger.info(f"Updating service: {name}, env: {env}")

        image = request.args.get("image")
        if not image:
            logger.warn("No image supplied")
            abort(400)

        swarm = Swarm(env)
        service = swarm.get_service(name)

        service.update(image=image)
        return (image, 200)


class Stack(Resource, TokenMixin):
    def get(self, env, name):
        logger.info(f"Fetching stack: {name}, env: {env}")

        swarm = Swarm(env)
        services = swarm.get_stack_services(name)

        images = {
            service.name: swarm.get_service_image(service)
            for service in services
        }
        return (images, 200)

    def put(self, env, name):
        logger.info(f"Updating stack: {name}, env: {env}")

        image_spec = request.args.get("image")
        try:
            image, tag = image_parts(image_spec)

        except Exception:
            logger.warn(f"bad image spec: {image_spec}")
            abort(400)

        swarm = Swarm(env)

        matching_services = [
            service for service in swarm.get_stack_services(name)
            if image_parts(swarm.get_service_image(service))[0] == image
        ]

        if not len(matching_services):
            logger.warn(f"No services of swarm: {name} matches: {image}")
            abort(400)

        result = {}
        for service in matching_services:
            service.update(image=image_spec)
            result[service.name] = image_spec

        return (result, 200)
