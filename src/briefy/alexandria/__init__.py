"""Initialization of briefy.alexandria package."""
from briefy import alexandria
from briefy.alexandria.db import get_db
from briefy.alexandria.db import get_engine
from briefy.alexandria.db import Session
from pyramid.config import Configurator
from zope.configuration.xmlconfig import XMLConfig

import briefy.common
import briefy.ws
import logging
import pkg_resources


__version__ = pkg_resources.get_distribution(__package__).version

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


XMLConfig('configure.zcml', briefy.common)()
XMLConfig('configure.zcml', alexandria)()


def includeme(config):
    """Include config to be included by other services."""
    config.registry['db_session_factory'] = Session
    config.add_request_method(get_db, 'db', reify=True)
    config.include('briefy.ws')
    briefy.ws.initialize(config, version=__version__, project_name=__name__)
    config.include('pyramid_zcml')
    config.load_zcml('configure.zcml')
    config.scan()


def main(global_config, debug=False, **settings):
    """Return a Pyramid WSGI application."""
    settings = briefy.ws.expandvars_dict(settings)
    engine = get_engine(settings)
    settings['config_file'] = (
        getattr(global_config, '__file__', None) or global_config.get('__file__', '')
    )
    from briefy.common.db.model import Base
    Session.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(
        settings=settings

    )
    config.registry['debug'] = debug
    includeme(config)
    logger.info('{name} is running'.format(name=__name__))
    return config.make_wsgi_app()
