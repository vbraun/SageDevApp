import logging
log = logging.getLogger()

import json
import asyncio
from aiohttp import web

from app.auth.token import jwt_encode
from app.auth.user_model import (
    User,
    EmailNotVerifiedException, InvalidPasswordException
)



class LoginHandler(object):

    @asyncio.coroutine
    def post(self, request):
        data = yield from request.read()
        log.debug('{0}: {1}'.format(request, data))
        if not data:
            return self.error_bad_request('Empty request')
        data = yield from request.json()
        email = data['email']
        password = data['password']

        try:
            user = User.login(email, password)
        except (EmailNotVerifiedException, InvalidPasswordException) as exc:
            return self.error_forbidden(exc)

        reply = dict(
            success=True,
            jwt=jwt_encode(email)
        )
        return web.Response(body=json.dumps(reply).encode('utf-8'))

    def error_bad_request(self, message):
        reply = dict(
            success=False,
            reason=str(message),
        )
        return web.HTTPBadRequest(body=json.dumps(reply).encode('utf-8'))

    def error_forbidden(self, message):
        reply = dict(
            success=False,
            reason=str(message),
        )
        return web.HTTPForbidden(body=json.dumps(reply).encode('utf-8'))

        
