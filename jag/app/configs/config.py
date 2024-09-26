"""Class-based Flask app configuration."""
import os
from os import environ, path
import logging
import sys
import yaml

import flask
import dotenv

from dotenv import load_dotenv


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


class Config:
    """Configuration from environment variables."""

    load_dotenv(path.join(BASE_DIR, ".env"))

    CONFIGDIR = path.abspath(path.dirname(__file__))

    SECRET_KEY = environ.get("SECRET_KEY")
    FLASK_ENV = environ.get("FLASK_ENV")
    
    IDE = environ.get("IDE")

    APP_DIR = environ.get('APP_DIR', 'app')
    # Static Assets
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = environ.get('TEMPLATES_FOLDER', 'templates')
    COMPRESSOR_DEBUG = environ.get("COMPRESSOR_DEBUG")
    # file uploads
    UPLOADS_DEFAULT_DEST = environ.get("UPLOADS_DEFAULT_DEST", f'{APP_DIR}/{STATIC_FOLDER}') 
    UPLOAD_FOLDER = environ.get("UPLOAD_FOLDER", UPLOADS_DEFAULT_DEST) 
    UPLOADED_IMAGES_DEST = environ.get("UPLOADED_IMAGES_DEST", UPLOADS_DEFAULT_DEST) 
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'svg'}
    CROPPED_IMAGES_FOLDER = environ.get('CROPPED_IMAGES_FOLDER', UPLOADS_DEFAULT_DEST)

     
    # is this even needed?
    PORT = environ.get("PORT")

    # database
    DB_PORT = environ.get("DB_PORT")
    DB_HOST = environ.get("DB_HOST")
    DB_NAME = environ.get("JAG_POSTGRES_DB")
    DB_USERNAME = environ.get("JAG_POSTGRES_USER")
    DB_PASSWORD = environ.get("JAG_POSTGRES_PASSWORD")

    # AI APIs  --- refactor these into DB
    # Google/Vertex AI:
    GOOGLE_APPLICATION_CREDENTIALS_API_KEY_PATH = environ.get("GOOGLE_APPLICATION_CREDENTIALS_API_KEY_PATH")
    
    # LIKELY CIRCULAR LOGIC....SEE IF IT WORKS STILL!!
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS_API_KEY_PATH
    
    VERTEX_PROJECT_ID = environ.get("VERTEX_PROJECT_ID")
    VERTEX_PROJECT_LOCATION = environ.get("VERTEX_PROJECT_LOCATION")

    OPENAI_API_KEY = environ.get("OPENAI_API_KEY")

    CAPTURE_URL = environ.get("CAPTURE_URL")
    CAPTURE_IMAGE_DESTINATION = environ.get("CAPTURE_IMAGE_DESTINATION", UPLOADS_DEFAULT_DEST)
        # YAML Configs
    # stream config (make sure the file exists in the right folder!)
    STREAM_CONFIG = None
    STREAM_CONFIG_PATH = path.join(CONFIGDIR, "stream_config.yml")

    if path.exists(STREAM_CONFIG_PATH):
        with open(STREAM_CONFIG_PATH, 'r') as stream:
            try:
                STREAM_CONFIG = yaml.safe_load(stream)
            except yaml.YAMLError as e:
                logging.error(f"Error loading Stream YAML config: {e}")
                STREAM_CONFIG = {}
    else:
        logging.warning(f"YAML config file not found at {STREAM_CONFIG_PATH}.")
        STREAM_CONFIG = {}

    # site config.
    SITE_CONFIG = None
    SITE_CONFIG_PATH = path.join(CONFIGDIR, "site_config.yml")

    if path.exists(SITE_CONFIG_PATH):
        with open(SITE_CONFIG_PATH, 'r') as stream:
            try:
                SITE_CONFIG = yaml.safe_load(stream)
            except yaml.YAMLError as e:
                logging.error(f"Error loading Site YAML config: {e}")
                SITE_CONFIG = {}
    else:
        logging.warning(f"YAML config file not found at {SITE_CONFIG_PATH}.")
        SITE_CONFIG = {}

    API_PATH = SITE_CONFIG['api_base'] + SITE_CONFIG['api_version']
        
    @staticmethod
    def setup_image_paths(path):
        """Define the output directory for images & set permissions."""
        if not os.path.exists(path):
            os.makedirs(path)
            os.chmod(path, 0o775)

    @classmethod
    def initialize_image_paths(cls):
        image_paths = set(filter(None, [
            cls.CAPTURE_IMAGE_DESTINATION, 
            cls.UPLOADED_IMAGES_DEST, 
            cls.UPLOAD_FOLDER, 
            cls.CROPPED_IMAGES_FOLDER
        ]))
        
        return image_paths
