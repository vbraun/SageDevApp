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


class TestPackageUpload(unittest.TestCase):

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

    def test_upload_package(self):
        def go():
            data = 'The quick brown fox jumps over the lazy bird'
            resp = yield from self.session.post('http://localhost:8080/api/v1/pkg/upload', data=data)
            self.assertEqual(resp.status, 200)
            data = yield from resp.read()
            print(data)
            self.assertEqual(data, b'8e209ebdf91eb7d75e313c199e887ef4fbdf3b9e')
            resp.close()
        self.loop.run_until_complete(go())
        
