#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

from flask import Flask
from flask_restful import Api

from . import config
from .resources import Service, Stack

logging.basicConfig(level=config.LOG_LEVEL)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(config)

api = Api(app)
api.add_resource(Service, "/service/<string:env>/<string:name>")
api.add_resource(Stack, "/stack/<string:env>/<string:name>")

if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)

    logger.info("Starting debug server")
    app.run(debug=True)
