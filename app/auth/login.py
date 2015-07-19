import json
import asyncio
from aiohttp import web

from app.auth.token import jwt_encode


class LoginHandler(object):

    @asyncio.coroutine
    def post(self, request):
        print(request)
        data = yield from request.read()
        print(data)
        data = yield from request.json()
        email = data['email']
        password = data['password']
        
        reply = dict(
            success=True,
            jwt=jwt_encode(email)
        )
        return web.Response(body=json.dumps(reply).encode('ascii'))
        
        
        
