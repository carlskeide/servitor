# -*- coding: utf-8 -*-
import logging

from flask import request
from flask_restful import Resource, abort

from .docker import Swarm, image_parts
from .auth import token_auth

logger = logging.getLogger(__name__)


class ProtectedsResource(Resource):
    method_decorators = [token_auth.login_required]


class Service(ProtectedsResource):
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

        swarm.force_update(service, image)
        return (image, 200)


class Stack(ProtectedsResource):
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
            swarm.force_update(service, image_spec)
            result[service.name] = image_spec

        return (result, 200)
