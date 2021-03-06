# -*- coding: utf-8 -*-
"""
    init app
"""
import os
import logging
from flask import Flask
import flask_migrate
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()
migrate = flask_migrate.Migrate()
app = None

def create_app():
    """ create application
    """
    global app
    app = Flask(__name__, static_url_path='', static_folder='../web/static/', template_folder='../web/templates/')
    app.config.from_object(Config)
    # Configure logging
    formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
    handler = logging.FileHandler(app.config['LOGGING_LOCATION'], encoding="utf-8")
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(app.config['LOGGING_LEVEL'])

    db.app = app
    db.init_app(app)
    migrate.init_app(app, db)

    if os.path.exists(app.config['SQLALCHEMY_DATABASE_URI']):
        with app.app_context():
            flask_migrate.upgrade()
    else:
        # init alembic version
        with app.app_context():
            flask_migrate.stamp()

    from . import controller
    from . import model
    from . import task
    controller.register(app)
    model.load_models()
    db.create_all()
    task.init_task(app)

    return app
