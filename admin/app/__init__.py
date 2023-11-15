import sentry_sdk
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .config import Config


db = SQLAlchemy()


def create_app(config_class: Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    if not app.config["TESTING"]:
        sentry_sdk.init(
            dsn=app.config.SENTRY_DSN,
            traces_sample_rate=1.0,
            profiles_sample_rate=1.0,
        )

    from .views.auth import auth
    from .views.blogs import blog

    app.register_blueprint(auth)
    app.register_blueprint(blog)

    return app
