import asyncio
from aiohttp import web

from app.auth.login import LoginHandler
login_handler = LoginHandler()



@asyncio.coroutine
def hello(request):
    return web.Response(body=b"Hello, world")


application = web.Application()
application.router.add_route('GET', '/api/hello', hello)
application.router.add_route('POST', '/api/v1/auth/login', login_handler.post)
