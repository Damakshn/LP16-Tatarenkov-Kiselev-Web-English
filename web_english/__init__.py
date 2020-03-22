from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    migrate.init_app(app, db)
    import web_english.models as models
    from web_english.main import bp as main_bp
    from web_english.text import bp as text_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(text_bp, url_prefix="/text")

    return app
