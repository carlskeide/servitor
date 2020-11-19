# -*- coding: utf-8 -*-
import logging
import re

import docker
from docker.tls import TLSConfig
from flask_restful import abort

from . import settings

logger = logging.getLogger(__name__)


def image_parts(image):
    match = re.match(r'^(?P<name>.*?):(?P<tag>[^@:]+)(?:@[\w:]+)?$', image)

    if not match:
        raise ValueError('Unable to parse image spec')
    else:
        return match.groups()


class Swarm(object):
    def __init__(self, key):
        logger.debug(f"Initializing swarm: {key}")
        try:
            swarm = settings.DOCKER_SWARMS[key]

        except KeyError:
            logger.warning(f"Invalid swarm: {key}")
            abort(404)

        kwargs = {}

        tls_config = swarm.get("tls", False)
        if tls_config:
            kwargs["tls"] = TLSConfig(ca_cert=tls_config["ca_cert"],
                                      client_cert=(tls_config["client_cert"],
                                                   tls_config["client_key"]))

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

    def force_update(self, service, image_spec):
        """
            Extract the image from a service object
        """
        if self.get_service_image(service) == image_spec:
            logger.info(f"Pulling the latest version of: {image_spec}")
            self.client.images.pull(image_spec)

            service.force_update()

        else:
            service.update(image=image_spec)
