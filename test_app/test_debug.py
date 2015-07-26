

import logging
log = logging.getLogger()

import json
import asyncio
import unittest
import jwt
import aiohttp

from app.identifier import Identifier
from app.auth.token import jwt_decode
from app.config import config


class TestUserDebug(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)
        self.session = aiohttp.ClientSession(loop=self.loop)

    def tearDown(self):
        self.session.close()
        self.loop.close()

    def test_user_data(self):
        def go():
            email = 'vbraun.name+{0}@gmail.com'.format(Identifier.new_random())
            registrationdata = json.dumps(dict(
                name='Volker Braun',
                email=email,
                password='s3kr1t'
            ))
            # Create account
            resp = yield from self.session.post('http://localhost:8080/api/v1/auth/register', data=registrationdata)
            self.assertEqual(resp.status, 200)
            # Try to login without validating email
            resp = yield from self.session.get('http://localhost:8080/api/v1/debug/user/{0}'.format(email))
            self.assertEqual(resp.status, 200)
            data = yield from resp.json()
            self.assertEqual(set(data.keys()), set(['success', 'user']))
            self.assertTrue(data['success'])
            self.assertEqual(data['user']['email'], email)
            self.assertEqual(data['user']['name'], 'Volker Braun')
            self.assertFalse(data['user']['email_validated'])
            self.assertFalse(data['user']['recovery_requested'])
            resp.close()
        self.loop.run_until_complete(go())
