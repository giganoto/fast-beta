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

    with app.app_context():
        from .models.admin import Admin
        from .models.blog import Blog, BlogCategory, BlogTag  # noqa: F401

        db.create_all()

        name, email = app.config["ADMIN_NAME"], app.config["ADMIN_EMAIL"]
        if not Admin.get(email):
            admin = Admin.create_instance(name=name, email=email)
            db.session.add(admin)
            db.session.commit()

    from .views.auth import auth
    from .views.blogs import blog

    app.register_blueprint(auth)
    app.register_blueprint(blog)

    return app
