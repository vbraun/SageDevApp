
import logging
log = logging.getLogger()


from aiohttp import web
from app.auth.token import jwt_decode, InvalidTokenError


def require_login(request):
    print(request.headers)
    authorization = request.headers.get('Authorization', '')
    if not authorization:
        log.error('No authorization header')
        raise web.HTTPForbidden()
    print('authorization', authorization)
    bearer = 'bearer '
    if not authorization.lower().startswith(bearer):
        log.error('Authorization header does not start with bearer: {0}'.format(authorization))
        raise web.HTTPForbidden()
    authorization = authorization[len(bearer):]
    try:
        jwt = jwt_decode(authorization)
    except InvalidTokenError as err:
        log.error('JWT is invalid: {0}'.format(err))
        raise web.HTTPForbidden()
        
