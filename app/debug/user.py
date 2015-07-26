import logging
log = logging.getLogger()

import json
import asyncio
from aiohttp import web

from app.config import config
from app.auth.token import jwt_encode
from app.auth.user_model import (
    User,
    EmailNotVerifiedException, InvalidPasswordException
)



class UserDebug(object):

    @asyncio.coroutine
    def get(self, request):
        if not config.debug:
            return error_forbidden('can only be accessed in debug mode')
        
        log.debug('{0}: {1}'.format(request, request.match_info))
        email = request.match_info['email']
        
        try:
            user = User.select().where(User.email == email).get()
        except User.DoesNotExist as exc:
            return self.error_unauthorized('Invalid email validation URL')

        reply = dict(
            success=True,
            user=dict(
                join_date=str(user.join_date),
                name=user.name,
                email=user.email,
                password=user.password,
                email_validated=user.email_validated,
                email_validation_secret=user.email_validation_secret,
                recovery_requested=user.recovery_requested,
                recovery_date=str(user.recovery_date),
                recovery_secret=user.recovery_secret,
            ),
        )
        return web.Response(body=json.dumps(reply).encode('utf-8'))

    def error_forbidden(self, message):
        reply = dict(
            success=False,
            reason=str(message),
        )
        return web.HTTPForbidden(body=json.dumps(reply).encode('utf-8'))
    
    def error_unauthorized(self, message):
        reply = dict(
            success=False,
            reason=str(message),
        )
        return web.HTTPUnauthorized(body=json.dumps(reply).encode('utf-8'))

        
