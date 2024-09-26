"""Initialize Flask app."""
import sys
import os

import flask
import flask_login
from flask import Flask, g, flash, redirect, url_for
from flask_login import LoginManager, current_user
from sqlalchemy import select, update
from sqlalchemy.sql import func

from .flask_util_js import FlaskUtilJs

# from .auth import auth



if '/app' not in sys.path:
    sys.path.append('/app')


def create_app():
    os.chdir('/app')
    app = Flask(__name__, instance_relative_config=False)
   
    env = os.getenv('FLASK_ENV', 'production')

    # Load the appropriate configuration
    if env == 'development':
        from .configs.dev import DevConfig as Config
    else:  # Defaults to production
        from .configs.config import Config    
    
    try:
        app.config.from_object(Config)
    except Exception as e:
        print(f"Failed to load configuration: {e}")
        raise

    # Initialize image paths
    image_paths = Config.initialize_image_paths()
    for path in image_paths:
        Config.setup_image_paths(path)
            
    with app.app_context():

        g.user = current_user

        from .models import Users
        from .frontend.routes import frontend
        from .api.routes import api
        from .auth.auth import auth

        app.register_blueprint(api)
        app.register_blueprint(frontend)
        app.register_blueprint(auth)

        fujs = FlaskUtilJs(app)

        from .database import session
        
        
            # Initialize the LoginManager
        # from .auth.auth import login_manager
        # login_manager.init_app(app)

        login_manager = LoginManager(app)
        login_manager.login_view = "login"

        @login_manager.user_loader
        def load_user(user_id):
            if user_id == 'None':
                current_user = flask_login.AnonymousUserMixin
                return current_user
            stmt = select(Users).where(Users.id == int(user_id))
            result = session.execute(stmt)
            for user_obj in result.scalars():
                #  Update last login value
                stmt = update(Users).where(Users.id == int(user_id)).values(
                    last_login=func.now())
                result = session.execute(stmt)
                session.commit()
                return user_obj

        @login_manager.unauthorized_handler
        def unauthorized():
            """Redirect unauthorized users to Login page."""
            flash('You must be logged in to view that page.')

            return flask.redirect(
                flask.url_for('auth.login', user=current_user))


        @app.teardown_appcontext
        def shutdown_session(exception=None):
            if exception:
                session.rollback()
            session.remove()

        return app
