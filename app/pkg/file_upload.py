
import logging
log = logging.getLogger()

import os
import io
import json
import asyncio
import aiohttp
from aiohttp import web
import tempfile

from app.config import config
from app.auth.require_login import require_login


class FileUploadHandler(object):

    def sha1(self, filename):
        create = asyncio.create_subprocess_exec(
            'sha1sum', filename,
            stdin=None,
            stdout=asyncio.subprocess.PIPE)
        proc = yield from create
        # Read one line of output
        data = yield from proc.stdout.readline()
        line = data.decode('ascii')[:40]
        # Wait for the subprocess exit
        yield from proc.wait()
        return line


    def save_to_tmpfile(self, request):
        chunk_size = 4096 ** 16
        # Make temporary file
        os.makedirs(config.data_files.tmp, exist_ok=True)
        fd, filename = tempfile.mkstemp(dir=config.data_files.tmp)
        os.close(fd)
        # Read
        reader = aiohttp.MultipartReader.from_response(request)
        first_part = yield from reader.next()
        with open(filename, 'wb') as f:
            while True:
                chunk = yield from first_part.readline()
                if not chunk:
                    return f.name
                f.write(chunk)

    def move(self, filename, sha1):
        os.makedirs(config.data_files.uploads, exist_ok=True)
        destination = os.path.join(config.data_files.uploads, sha1)
        os.rename(filename, destination)
                
    @asyncio.coroutine
    def post(self, request):
        require_login(request)
        filename = yield from self.save_to_tmpfile(request)
        sha1 = yield from self.sha1(filename)
        self.move(filename, sha1)
        return web.Response(body=sha1.encode('ascii'))
