import logging
log = logging.getLogger()

import asyncio
from aiohttp import web

from app.route import application





def main_loop():
    loop = asyncio.get_event_loop()
    handler = application.make_handler()
    f = loop.create_server(handler, 'localhost', 8080)
    srv = loop.run_until_complete(f)
    print('serving on', srv.sockets[0].getsockname())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(handler.finish_connections(1.0))
        srv.close()
        loop.run_until_complete(srv.wait_closed())
        loop.run_until_complete(application.finish())
    loop.close()


if __name__ == '__main__':
    main_loop()
