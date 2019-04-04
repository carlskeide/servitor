# -*- coding: utf-8 -*-
from flask_httpauth import HTTPTokenAuth

from . import settings

token_auth = HTTPTokenAuth(scheme='Bearer')


@token_auth.verify_token
def verify_token(token):
    return (token == settings.TOKEN)
