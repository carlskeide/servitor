#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

from flask import Flask
from flask_restful import Api

from . import settings
from .resources import Service, Stack

logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(settings)

api = Api(app)
api.add_resource(Service, "/service/<string:env>/<string:name>")
api.add_resource(Stack, "/stack/<string:env>/<string:name>")

if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)
    app.run(debug=True)
