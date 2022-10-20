from flask import Flask

def create_app(testing_config=None):
    app = Flask(__name__,instance_relative_config=True)

    if testing_config is None:
        app.config.from_mapping(
            SECRET_key = "dev"
        )
    else:
        app.config.from_mapping(testing_config)

    @app.get("/")
    def index():
        return "initial route" 

    return app
