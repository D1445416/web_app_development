import os
from flask import Flask
from .models import db
from .routes import init_app as init_routes

def create_app(test_config=None):
    """Create and configure the Flask application."""
    # instance_relative_config=True tells the app that configuration files
    # are relative to the instance folder.
    app = Flask(__name__, instance_relative_config=True)
    
    # Load default configuration
    app.config.from_object('config.Config')

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize SQLAlchemy with this app context
    db.init_app(app)

    # Register all Blueprints from the routes package
    init_routes(app)

    return app

def init_db():
    from . import models
    app = create_app()
    with app.app_context():
        db.create_all()
        print("Initialized the SQLite database at instance/database.db")
