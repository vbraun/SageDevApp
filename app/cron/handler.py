
import logging
log = logging.getLogger()

import asyncio
from aiohttp import web

from app.cron.cache_packages import cache_packages
from app.cron.update_repo import update_repo

@asyncio.coroutine
def cron_handler(request):
    output = []
    output.append(cache_packages())
    output.append(update_repo())
    return web.Response(
        content_type='text/plain',
        body='\n'.join(output).encode('utf-8'))

