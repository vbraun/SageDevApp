import logging
log = logging.getLogger()

import json
import functools
import asyncio
from aiohttp import web

from app.config import config
from app.auth.token import jwt_encode
from app.auth.known_email_model import KnownEmail
from app.auth.user_model import User, EmailExistsException
from app.auth.validation_email import send_validation_email



class RegistrationHandler(object):

    @asyncio.coroutine
    def post(self, request):
        data = yield from request.read()
        log.debug('{0}: {1}'.format(request, data))
        data = yield from request.json()
        name = data['name']
        email = data['email']
        password = data['password']

        if not KnownEmail.select().where(KnownEmail.email == email).exists():
            return self.error_forbidden('Email address must appear in the git commit log')
        
        try:
            user = User.create_from_registration(name, email, password)
        except EmailExistsException as exc:
            return self.error_forbidden(exc);

        asyncio.get_event_loop().create_task(self.send_validation_link(user))

        reply = dict(
            success=True,
            name=name,
            email=email,
        )
        return web.Response(body=json.dumps(reply).encode('utf-8'))
        
    def error_forbidden(self, message):
        reply = dict(
            success=False,
            reason=str(message),
        )
        return web.HTTPForbidden(body=json.dumps(reply).encode('utf-8'))

    @asyncio.coroutine
    def send_validation_link(self, user):
        yield from asyncio.sleep(2)
        send_validation_email(user)
    


class EmailValidationHandler(object):

    @asyncio.coroutine
    def post(self, request):
        data = yield from request.read()
        log.debug('{0}: {1}'.format(request, data))
        data = yield from request.json()
        secret = data['secret']

        try:
            user = User.select().where(User.email_validation_secret == secret).get()
        except User.DoesNotExist as exc:
            return self.error_unauthorized('Invalid email validation URL')
        else:
            user.email_validated = True
            user.save()
        
        reply = dict(
            success=True,
            name=user.name,
            email=user.email,
        )
        return web.Response(body=json.dumps(reply).encode('utf-8'))
    
    def error_unauthorized(self, message):
        reply = dict(
            success=False,
            reason=str(message),
        )
        return web.HTTPUnauthorized(body=json.dumps(reply).encode('utf-8'))

        

    
