# -*- coding: utf-8 -*-
import logging

import docker
from docker.tls import TLSConfig
from flask_restful import abort

from . import settings

logger = logging.getLogger(__name__)


class Swarm(object):
    def __init__(self, key):
        logger.debug(f"Initializing swarm: {key}")
        try:
            swarm = settings.DOCKER_SWARMS[key]

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
        """
            Get a swarm service by name
        """
        services = self.client.services.list()

        for service in services:
            if service.name == name:
                return service

        else:
            logger.error(f"No service matched name: {name!r}")
            abort(404)

    def get_stack_services(self, name):
        """
            Get all swarm services attached to a stack
        """
        services = self.client.services.list(filters={
            "label": f"com.docker.stack.namespace={name}"
        })

        return services

    def get_service_image(self, service):
        """
            Extract the image from a service object
        """
        return service.attrs["Spec"]["TaskTemplate"]["ContainerSpec"]["Image"]
