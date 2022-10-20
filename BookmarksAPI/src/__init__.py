from flask import Flask
import os
from src.database import db

def create_app(testing_config=None):
    app = Flask(__name__,instance_relative_config=True)

    if testing_config is None:
        app.config.from_mapping(
            SECRET_key = os.environ.get('SECRET_KEY'),
            SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DB_URI'))
    else:
        app.config.from_mapping(testing_config)

    @app.get("/")
    def index():
        return "initial route" 

    
    db.app = app
    db.init_app(app)

    return app
