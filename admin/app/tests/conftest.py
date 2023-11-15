import pytest
from dataclasses import dataclass

from app import create_app, db
from app.config import TestingConfig
from app.models.admin import Admin
from app.utils.auth import generate_jwt_token


@pytest.fixture(scope="function")
def app():
    """
    Create and configure a new app instance for each test session.
    """
    app = create_app(TestingConfig)

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.drop_all()  # Clean up and drop all tables


@pytest.fixture(scope="function")
def client(app):
    return app.test_client()


@pytest.fixture(scope="function")
def init_database(app):
    with app.app_context():
        admin = Admin.create_instance(name=app.config["ADMIN_NAME"], email=app.config["ADMIN_EMAIL"])
        db.session.add(admin)
        db.session.commit()

    yield  # this is where the testing happens!

    with app.app_context():
        db.session.remove()
        db.drop_all()


@dataclass
class TestAdmin:
    name: str
    email: str
    token: str = None

    def __post_init__(self):
        self.token = generate_jwt_token({"email": self.email})


@pytest.fixture(scope="function")
def test_admin(app):
    with app.app_context():
        yield TestAdmin(
            name=app.config["ADMIN_NAME"],
            email=app.config["ADMIN_EMAIL"],
        )
