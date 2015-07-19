
import logging
log = logging.getLogger()

from datetime import datetime


import jwt
from jwt import InvalidTokenError

from app.config import config


ALGORITHM = 'HS256'

ISSUER = 'http://www.sagemath.org'



def jwt_encode(email):
    payload = dict(
        iss=ISSUER,
        iat=datetime.utcnow(),
        sub=email
    )
    return jwt.encode(
        payload,
        config.cookie_secret_key,
        algorithm=ALGORITHM,
    ).decode('ascii')


def jwt_decode(token):
    result = jwt.decode(
        token,
        config.cookie_secret_key,
        algorithms=[ALGORITHM],
        issuer=ISSUER,
    )
    assert result['iss'] == ISSUER
    return result
