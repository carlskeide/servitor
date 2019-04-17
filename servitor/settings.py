# -*- coding: utf-8 -*-
from os import environ as env
import logging
import sys

import yaml

logger = logging.getLogger(__name__)

DEBUG = False
ERROR_404_HELP = False

# App config
LOG_LEVEL = env.get("LOG_LEVEL", "INFO").upper()

# Secrets
TOKEN = env.get("TOKEN", "")
if not TOKEN:
    logger.error("Auth token must be set")
    sys.exit(1)

# Swarm config
CONFIG_FILE = env.get("CONFIG_FILE", "/servitor.yaml")

try:
    with open(CONFIG_FILE) as f:
        _service_config = yaml.safe_load(f)

    DOCKER_SWARMS = _service_config["swarm"]

except Exception:
    logger.exception("Invalid service config.")
    sys.exit(1)
