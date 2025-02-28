#!/usr/bin/env python3
"""
Flask application entry point
"""
from flask import Flask
from flask_cors import CORS
from config import Config
from models.engine.db_storage import DBStorage


def create_app(config_class=Config, db_engine=None):
    """Application Factory

    Args:
        config_class (_type_, optional):Gets variables from the config class. Defaults to Config.
        db_engine (_type_, optional): Database Engine to use
    """
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config.from_object(Config)

    app.db_storage = DBStorage(db_engine=db_engine)
    app.db_storage.reload()

    from Routes import bp
    app.register_blueprint(bp)

    return app
