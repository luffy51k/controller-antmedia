# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present SnowData.Tech
"""

from functools import wraps
from os import abort

from flask import abort, request, make_response
from apps import app


def api_login_required(func):
    """Login required with api key"""

    @wraps(func)
    def decorated_view(*args, **kwargs):

        # api-key cua ben Headend backend
        if "api_key" in request.args:
            api_key = request.args.get("api_key")
            if api_key != app.config['SECRET_KEY']:
                make_response('authentication failed', 401)
        else:
            make_response('missing api_key', 400)

        return func(*args, **kwargs)

    return decorated_view
