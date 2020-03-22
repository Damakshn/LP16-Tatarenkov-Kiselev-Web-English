from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    import web_english.models as models
    from web_english.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app
