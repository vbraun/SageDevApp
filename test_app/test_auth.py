import logging
log = logging.getLogger()

import json
import asyncio
import unittest
import jwt
import aiohttp

from app.auth.token import jwt_decode


class TestAuthentication(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)
        self.session = aiohttp.ClientSession(loop=self.loop)

    def tearDown(self):
        self.session.close()
        self.loop.close()

    def test_root(self):
        def go():
            resp = yield from self.session.get('http://localhost:8080')
            self.assertEqual(resp.status, 200)
            data = yield from resp.read()
            self.assertEqual(data, b'Hello, world')
        self.loop.run_until_complete(go())

    def test_login(self):
        def go():
            logindata = json.dumps(dict(
                email='vbraun.name@gmail.com',
                password='s3kr1t'
            ))
            resp = yield from self.session.post('http://localhost:8080/api/v1/login', data=logindata)
            self.assertEqual(resp.status, 200)
            data = yield from resp.read()
            self.assertTrue(data.startswith(b'{'))
            data = yield from resp.json()
            self.assertEqual(set(data.keys()), set(['success', 'jwt']))
            self.assertTrue(data['success'])
            jwt = jwt_decode(data['jwt'])
            self.assertEqual(jwt['iss'], 'http://www.sagemath.org')
            self.assertEqual(jwt['sub'], 'vbraun.name@gmail.com')
        self.loop.run_until_complete(go())
        
