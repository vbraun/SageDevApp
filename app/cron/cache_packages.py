
import os
import sys

import logging
log = logging.getLogger()

import asyncio
from aiohttp import web

from pprint import pformat

from app.config import config

import app.sage_repo
from sage_bootstrap.package import Package

from app.pkg.package_model import Package as PackageModel

import peewee
from app.database import database


def gracefully_read(pkg, filename):
    fqn = os.path.join(pkg.path, filename)
    try:
        with open(fqn, encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        log.critical('{0} is not valid UTF_8'.format(fqn))
        return 'Not valid UTF-8'
    except FileNotFoundError:
        log.critical('{0} not found'.format(fqn))
        return('{0} not found'.format(filename))

    
def cache_packages():
    preexisting = set([model.name for model in PackageModel.select()])
    output = []
    for pkg in Package.all():
        pkg_data = dict(
            name =  pkg.name,
            sha1 = pkg.sha1,
            version = pkg.version,
            patchlevel = pkg.patchlevel,
            filename = pkg.tarball_filename,
            description = gracefully_read(pkg, 'SPKG.txt'),
            pkgtype = gracefully_read(pkg, 'type'),
        )
        try:
            with database.atomic():
                model = PackageModel.create(**pkg_data)
        except peewee.IntegrityError:
            PackageModel.update(
                **pkg_data
            ).where(
                PackageModel.name == pkg.name
            ).execute()
        output.append(pformat(pkg_data))
        preexisting.discard(pkg.name)
    for pkg_name in preexisting:
        PackageModel.delete().where(PackageModel.name == pkg_name)
    return '\n'.join(output)



@asyncio.coroutine
def cache_packages_handler(request):
    log.debug(request)
    output = cache_packages()
    return web.Response(body=output.encode('utf-8'))


