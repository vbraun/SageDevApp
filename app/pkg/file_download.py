
import logging
log = logging.getLogger()

import os
import io
import json
import asyncio
import aiohttp
from aiohttp import web

from app.config import config


class FileDownloadHandler(object):

    CHUNK_SIZE = 0x10000
    
    def get(self, request):
        sha1 = request.match_info['sha1']
        filename = os.path.join(config.data_files.uploads, sha1)
        if not os.path.isfile(filename):
            return self.error_not_found('no file with that sha1')
        statinfo = os.stat(filename)
        response = web.StreamResponse()
        response.enable_chunked_encoding()
        response.content_length = statinfo.st_size
        response.content_type = 'application/octet-stream'
        response.start(request)
        with open(filename, 'rb') as f:
            while True:
                chunk = f.read(self.CHUNK_SIZE)
                if not chunk:
                    return response
                response.write(chunk)
                yield from response.drain()

    def error_forbidden(self, message):
        reply = dict(
            success=False,
            reason=str(message),
        )
        return web.HTTPNotFound(body=json.dumps(reply).encode('utf-8'))
            
