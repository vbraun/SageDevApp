import logging
log = logging.getLogger()

import json
import asyncio
from aiohttp import web

from app.pkg.package_model import Package


@asyncio.coroutine
def list_packages_handler(request):
    log.debug(request)
    reply = dict(
        success=True,
        packages=[model.name for model in Package.select()],
    )
    return web.Response(body=json.dumps(reply).encode('utf-8'))


@asyncio.coroutine
def view_package_handler(request):
    log.debug(request)
    name = request.match_info['name']
    reply = dict(
        success = True,
        package = Package.get(Package.name == name).to_json(),
    )
    return web.Response(body=json.dumps(reply).encode('utf-8'))
