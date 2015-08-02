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


class TestPackage(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)
        self.session = aiohttp.ClientSession(loop=self.loop)
        def cron():
            resp = yield from self.session.get('http://localhost:8080/cron/daily')
            self.assertEqual(resp.status, 200)
            resp.close()
        self.loop.run_until_complete(cron())

    def tearDown(self):
        self.session.close()
        self.loop.close()

    def test_list_packages(self):
        def go():
            resp = yield from self.session.get('http://localhost:8080/api/v1/pkg/list')
            self.assertEqual(resp.status, 200)
            data = yield from resp.json()
            self.assertTrue(data['success'])
            self.assertIn('gap', data['packages'])
            resp.close()
        self.loop.run_until_complete(go())

    def test_view_package(self):
        def go():
            resp = yield from self.session.get('http://localhost:8080/api/v1/pkg/view/gap')
            self.assertEqual(resp.status, 200)
            data = yield from resp.json()
            self.assertTrue(data['success'])
            self.assertEqual(data['package']['name'], 'gap')
            resp.close()
        self.loop.run_until_complete(go())
