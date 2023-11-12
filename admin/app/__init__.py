import sentry_sdk
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .config import Config


db = SQLAlchemy()
sentry_sdk.init(
    dsn=Config.SENTRY_DSN,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from . import auth

    app.register_blueprint(auth.auth)

    return app
