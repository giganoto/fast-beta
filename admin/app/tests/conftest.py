import pytest
from dataclasses import dataclass

from faker import Faker

from app import create_app, db
from app.config import TestingConfig
from app.controllers.admin import create_admin
from app.controllers.blogs import (
    create_blog_tag,
    create_blog_category,
    create_blog,
    get_blog
)
from app.models.blog import BlogTag, BlogCategory


from app.utils.auth import generate_jwt_token


fake = Faker()

TOTAL_BLOGS = 20
TOTAL_BLOG_TAGS = 10
TOTAL_BLOG_CATEGORIES = 10


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
        create_admin(
            name=app.config["ADMIN_NAME"],
            email=app.config["ADMIN_EMAIL"],
        )

        for idx in range(TOTAL_BLOG_TAGS):
            fake.seed_instance(idx)
            create_blog_tag(name=fake.word(), description=fake.sentence())

        for idx in range(TOTAL_BLOG_CATEGORIES):
            fake.seed_instance(idx)
            create_blog_category(name=fake.word(), description=fake.sentence())

        for idx in range(TOTAL_BLOGS):
            fake.seed_instance(idx)
            category_id = (
                (idx % TOTAL_BLOG_CATEGORIES) + 1
                if idx < TOTAL_BLOGS//2
                else fake.random_int(min=1, max=TOTAL_BLOG_CATEGORIES)
            )
            create_blog(
                title=fake.sentence(),
                description=fake.sentence(),
                content=fake.text(),
                is_draft=fake.boolean(),
                category_id=category_id,
                tags=[fake.random_int(min=1, max=TOTAL_BLOG_TAGS) for _ in range(min(TOTAL_BLOG_TAGS, 3))],
            )

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


@pytest.fixture(scope="function")
def existing_blog_tag(app):
    with app.app_context():
        return db.session.get(BlogTag, fake.random_int(min=1, max=TOTAL_BLOG_TAGS))


@pytest.fixture(scope="function")
def existing_blog_category(app):
    with app.app_context():
        return db.session.get(BlogCategory, fake.random_int(min=1, max=TOTAL_BLOG_CATEGORIES))


@pytest.fixture(scope="function")
def existing_blog(app):
    with app.app_context():
        return get_blog(blog_id=fake.random_int(min=1, max=TOTAL_BLOGS))
