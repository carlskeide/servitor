# -*- coding: utf-8 -*-
import sys
from os import environ as env

import yaml

DEBUG = False
ERROR_404_HELP = False

# App config
LOG_LEVEL = env.get("LOG_LEVEL", "INFO").upper()

# Secrets
TOKEN = env.get("TOKEN")

# Services
CONFIG_FILE = env.get("CONFIG_FILE", "/etc/servitor/config.yaml")
with open(CONFIG_FILE) as f:
    _service_config = yaml.load(f)

try:
    DOCKER_SWARMS = _service_config["swarms"]
    DOCKER_STACKS = _service_config["stacks"]

except KeyError:
    print("Invalid service config")
    sys.exit(1)
