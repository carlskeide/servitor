# -*- coding: utf-8 -*-
from os import environ as env

import yaml

DEBUG = False
ERROR_404_HELP = False

# App config
LOG_LEVEL = env.get("LOG_LEVEL", "INFO").upper()

# Secrets
TOKEN = env.get("TOKEN")
if not TOKEN:
    raise Exception("Token must be set")

# Services
CONFIG_FILE = env.get("CONFIG_FILE", "/conf/servitor.yaml")
with open(CONFIG_FILE) as f:
    _service_config = yaml.load(f)

try:
    DOCKER_SWARMS = _service_config["swarm"]

except KeyError:
    raise Exception("Invalid service config")
