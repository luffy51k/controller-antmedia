# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present EVG
"""

from importlib import import_module

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from apps.config import config_dict
from apps.flask_celery import make_celery

db = SQLAlchemy()


# migrate = Migrate()


def register_extensions(app):
    db.init_app(app)
    # migrate.init_app(app, db)


def register_blueprints(app):
    for module_name in ["antmedia"]:
        module = import_module("apps.{}.routes".format(module_name))
        app.register_blueprint(module.blueprint)


def configure_database(app):
    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    swagger = Swagger(app)
    register_extensions(app)
    # register_blueprints(app)
    # configure_database(app)
    return app


def create_app_after(app):
    register_blueprints(app)
    # configure_database(app)
    return app


# WARNING: Don't run with debug turned on in production!
# DEBUG = config("DEBUG", default=True, cast=bool)
DEBUG = True

# The configuration
get_config_mode = "Debug" if DEBUG else "Production"

try:

    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit("Error: Invalid <config_mode>. Expected values [Debug, Production] ")

app = create_app(app_config)

celery_app = make_celery(app)

# Load blueprints after Celery instance loaded
app = create_app_after(app)

# Migrate(app, db)
