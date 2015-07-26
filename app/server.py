import logging
log = logging.getLogger()

import asyncio
from aiohttp import web

from app.config import config
from app.route import application
from app.database import database, all_database_models




def main_loop():
    loop = asyncio.get_event_loop()
    handler = application.make_handler()
    f = loop.create_server(handler, 'localhost', 8080)
    srv = loop.run_until_complete(f)
    database.connect()
    database.create_tables(all_database_models())
    print('serving on', srv.sockets[0].getsockname())
    if config.debug:
        loop.set_debug(enabled=True)
        import app.debug.setup
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
    database.close()


if __name__ == '__main__':
    main_loop()
