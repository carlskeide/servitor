# -*- coding: utf-8 -*-
import logging
import sys

import yaml
import sec

logger = logging.getLogger(__name__)

DEBUG = False
ERROR_404_HELP = False

# App config
LOG_LEVEL = sec.load("LOG_LEVEL", fallback="INFO").upper()

# Secrets
TOKEN = sec.load("AUTH_TOKEN", fallback="")
if not TOKEN:
    logger.error("Auth token must be set")
    sys.exit(1)

# Swarm config
CONFIG_FILE = sec.load("CONFIG_FILE", fallback="/servitor.yaml")

try:
    with open(CONFIG_FILE) as f:
        _service_config = yaml.safe_load(f)

    DOCKER_SWARMS = _service_config["swarm"]

except Exception:
    logger.exception("Invalid service config.")
    sys.exit(1)
