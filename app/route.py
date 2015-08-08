import os
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

@asyncio.coroutine
def redirect_to_index(request):
    raise web.HTTPMovedPermanently('/index.html')


DIST_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), 'dist')
log.debug('DIST_DIR = {0}'.format(DIST_DIR))


application = web.Application()
application.router.add_route('GET', '/', redirect_to_index)

# Dummy route for testing
application.router.add_route('GET', '/api/v1/hello', hello)

# Authentication
application.router.add_route('POST', '/api/v1/auth/login', login_handler.post)
application.router.add_route('POST', '/api/v1/auth/register', registration_handler.post)
application.router.add_route('POST', '/api/v1/auth/validate', email_validation_handler.post)

# Package Management
from app.pkg.view import list_packages_handler, view_package_handler
application.router.add_route('GET', '/api/v1/pkg/list', list_packages_handler)
application.router.add_route('GET', '/api/v1/pkg/view/{name}', view_package_handler)

from app.pkg.file_upload import FileUploadHandler
application.router.add_route('POST', '/api/v1/pkg/upload', FileUploadHandler().post)
from app.pkg.file_download import FileDownloadHandler
application.router.add_route('GET', '/api/v1/pkg/download/{sha1}', FileDownloadHandler().get)

# Cron
from app.cron.handler import cron_handler
application.router.add_route('GET', '/cron/daily', cron_handler)

# Debug
if config.debug:
    from app.debug.user import UserDebug
    user_debug = UserDebug().get
    application.router.add_route('GET', '/api/v1/debug/user/{email}', user_debug)

# Static files
application.router.add_static('/', DIST_DIR)
    
