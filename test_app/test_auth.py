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


class TestAuthentication(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)
        self.session = aiohttp.ClientSession(loop=self.loop)

    def tearDown(self):
        self.session.close()
        self.loop.close()

    def test_hello(self):
        def go():
            resp = yield from self.session.get('http://localhost:8080/api/v1/hello')
            self.assertEqual(resp.status, 200)
            data = yield from resp.read()
            self.assertEqual(data, b'Hello, world')
            resp.close()
        self.loop.run_until_complete(go())

    def test_login(self):
        def go():
            email = 'vbraun.name+{0}@gmail.com'.format(Identifier.new_random())
            registrationdata = json.dumps(dict(
                name='Volker Braun',
                email=email,
                password='s3kr1t'
            ))
            logindata = json.dumps(dict(
                email=email,
                password='s3kr1t'
            ))
            # Try to login without account
            resp = yield from self.session.post('http://localhost:8080/api/v1/auth/login', data=logindata)
            self.assertEqual(resp.status, 403)
            data = yield from resp.json()
            self.assertFalse(data['success'])
            self.assertEqual(data['reason'], 'no account with this email')
            # Create account
            resp = yield from self.session.post('http://localhost:8080/api/v1/auth/register', data=registrationdata)
            self.assertEqual(resp.status, 200)
            # Try to login without validating email
            resp = yield from self.session.post('http://localhost:8080/api/v1/auth/login', data=logindata)
            self.assertEqual(resp.status, 403)
            data = yield from resp.json()
            self.assertEqual(set(data.keys()), set(['success', 'reason']))
            self.assertFalse(data['success'])
            self.assertEqual(data['reason'], 'email not verified')
            # Use debug api to get the email verification secret
            resp = yield from self.session.get('http://localhost:8080/api/v1/debug/user/{0}'.format(email))
            self.assertEqual(resp.status, 200)
            data = yield from resp.json()
            self.assertEqual(set(data.keys()), set(['success', 'user']))
            user = data['user']
            # Verify the email
            validationdata = json.dumps(dict(
                secret=user['email_validation_secret'],
            ))
            resp = yield from self.session.post('http://localhost:8080/api/v1/auth/validate', data=validationdata)
            self.assertEqual(resp.status, 200)
            data = yield from resp.json()
            self.assertEqual(set(data.keys()), set(['success', 'name', 'email']))
            self.assertTrue(data['success'])
            self.assertEqual(data['name'], 'Volker Braun')
            self.assertEqual(data['email'], email)
            # Log into the new account
            resp = yield from self.session.post('http://localhost:8080/api/v1/auth/login', data=logindata)
            data = yield from resp.read()
            self.assertEqual(resp.status, 200)
            self.assertTrue(data.startswith(b'{'))
            data = yield from resp.json()
            self.assertEqual(set(data.keys()), set(['success', 'jwt']))
            self.assertTrue(data['success'])
            jwt = jwt_decode(data['jwt'])
            self.assertEqual(jwt['iss'], config.baseurl)
            self.assertEqual(jwt['sub'], email)
            resp.close()
        self.loop.run_until_complete(go())
        

    def test_registration(self):
        def go():
            email = 'vbraun.name+{0}@gmail.com'.format(Identifier.new_random())
            registrationdata = json.dumps(dict(
                name='Volker Braun',
                email=email,
                password='s3kr1t'
            ))
            resp = yield from self.session.post('http://localhost:8080/api/v1/auth/register', data=registrationdata)
            self.assertEqual(resp.status, 200)
            data = yield from resp.read()
            self.assertTrue(data.startswith(b'{'))
            data = yield from resp.json()
            self.assertEqual(set(data.keys()), set(['success', 'name', 'email']))
            self.assertTrue(data['success'])
            self.assertEqual(data['name'], 'Volker Braun')
            self.assertEqual(data['email'], email)
            resp.close()
        self.loop.run_until_complete(go())
        

    def test_duplicate_registration(self):
        def go():
            registrationdata = json.dumps(dict(
                name='Duplicate Email',
                email='duplicate@sagemath.org',
                password='s3kr1t'
            ))
            # First might succeed or fail, depending on whether the email exists
            resp = yield from self.session.post('http://localhost:8080/api/v1/auth/register', data=registrationdata)
            # Second definitely fails
            resp = yield from self.session.post('http://localhost:8080/api/v1/auth/register', data=registrationdata)
            self.assertEqual(resp.status, 403)
            data = yield from resp.json()
            self.assertFalse(data['success'])
            self.assertEqual(data['reason'], 'account with given email already exists')
            resp.close()
        self.loop.run_until_complete(go())
