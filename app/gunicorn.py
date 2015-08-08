"""
Use this module as the gunicorn worker

EXAMPLE::

    gunicorn app.gunicorn:main -k aiohttp.worker.GunicornWebWorker -b localhost:8080
"""


import logging
log = logging.getLogger()

import asyncio
from aiohttp import web

from app.config import config
from app.database import database, all_database_models

database.connect()
database.create_tables(all_database_models())


from app.route import application as main

