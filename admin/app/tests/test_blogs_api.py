from faker import Faker
from flask import url_for

from app.controllers.blogs import get_all_tags


fake = Faker()


def test_get_blog_tag_success(client, init_database, test_admin):
    response = client.get(
        url_for("blog.get_all_tags"),
        headers={"Authorization": f"Bearer {test_admin.token}"},
    )
    assert response.status_code == 200

    all_tags_in_db = get_all_tags()
    assert len(response.json) == len(all_tags_in_db)

    assert response.json[0]["name"] == all_tags_in_db[0]["name"]


def test_create_blog_tag_success(client, init_database, test_admin):
    data = {
        "name": fake.word(),
        "description": fake.sentence(),
    }
    response = client.post(
        url_for("blog.create_tag"),
        headers={"Authorization": f"Bearer {test_admin.token}"},
        json=data,
    )
    assert response.status_code == 200
    assert response.json["name"] == data["name"]


def test_create_blog_tag_failure_without_token(client):
    data = {
        "name": fake.word(),
        "description": fake.sentence(),
    }
    response = client.post(
        url_for("blog.create_tag"),
        json=data,
    )
    assert response.status_code == 403
    assert "Forbidden" in response.json["message"]