# -*- coding: utf-8 -*-
import os
from tempfile import mkstemp
from unittest import TestCase, skip

import yaml

try:
    from mock import MagicMock, patch
except ImportError:
    from unittest.mock import MagicMock, patch

__all__ = ['TestCase', 'MagicMock', "patch", "skip", "TEST_TOKEN"]

TEST_TOKEN = "TestToken"

CONFIG_FILE = None
CONFIG_FIXTURE = {
    "swarm": {
        "some-swarm": {
            "url": "sa-staging-app-01:2375",
            "tls": False
        },
        "secure-swarm": {
            "url": "sa-live-app-01:2376",
            "tls": {
                "ca_cert": "/etc/servitor/tls-ca.pem",
                "client_cert": "/etc/servitor/tls-swarm.pem",
                "client_key": "/etc/servitor/tls-swarm.pem"
            }
        }
    }
}


def setup_module(module):
    global CONFIG_FILE

    _, CONFIG_FILE = mkstemp()
    with open(CONFIG_FILE, "w") as f:
        yaml.dump(CONFIG_FIXTURE, f)

    os.environ.setdefault("CONFIG_FILE", CONFIG_FILE)
    os.environ.setdefault("AUTH_TOKEN", TEST_TOKEN)


def teardown_module(module):
    os.remove(CONFIG_FILE)
