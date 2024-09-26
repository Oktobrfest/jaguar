from .config import Config
import logging
import sys

from os import environ


class DevConfig(Config):
    
    # logging.basicConfig()
    logging.basicConfig(level=logging.DEBUG,
                        format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

    
    # DATABASE RELATED: (EXTREMELY VERBOSE)
    logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
    logging.getLogger('sqlalchemy.pool').setLevel(logging.DEBUG)
    logging.getLogger('sqlalchemy.orm').setLevel(logging.DEBUG)

    # Redirect SQLAlchemy logs to stdout
    logging.getLogger('sqlalchemy.engine').addHandler(
        logging.StreamHandler(sys.stdout))

    logging.getLogger('sqlalchemy.pool').addHandler(
        logging.StreamHandler(sys.stdout))
    logging.getLogger('sqlalchemy.orm').addHandler(
        logging.StreamHandler(sys.stdout))

    CACHE_TYPE = "null"
    
    IDE = environ.get("IDE", 'vscode')    
    
    TEMPLATES_AUTO_RELOAD = True
    # Helps debug tempaltes not loading
    EXPLAIN_TEMPLATE_LOADING = True

    # logging.basicConfig(level=logging.DEBUG)


    if IDE == "pycharm":
        from . import pycharm

    
    
    
    # included to be able to step into other modules
    # Part of Flasks Debug toolba. maybe irrellivent
    # set in docker-compose or .env DEBUG = True
    # DEBUG_TB_INTERCEPT_REDIRECTS = False