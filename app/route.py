import logging
log = logging.getLogger()

import asyncio
from aiohttp import web

from app.config import config

from app.auth.login import LoginHandler
login_handler = LoginHandler()

from app.auth.register import RegistrationHandler, EmailValidationHandler
registration_handler = RegistrationHandler()
email_validation_handler = EmailValidationHandler()


@asyncio.coroutine
def hello(request):
    log.debug(request)
    return web.Response(body=b"Hello, world")


application = web.Application()
application.router.add_route('GET', '/api/v1/hello', hello)
application.router.add_route('POST', '/api/v1/auth/login', login_handler.post)
application.router.add_route('POST', '/api/v1/auth/register', registration_handler.post)
application.router.add_route('POST', '/api/v1/auth/validate', email_validation_handler.post)

if config.debug:
    from app.debug.user import UserDebug
    user_debug = UserDebug().get
    application.router.add_route('GET', '/api/v1/debug/user/{email}', user_debug)
