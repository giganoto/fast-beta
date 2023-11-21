import pytest
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
    assert response.status_code == 401
    assert "Missing auth token" in response.json["message"]


def test_create_blog_tag_failure_with_invalid_token(client):
    data = {
        "name": fake.word(),
        "description": fake.sentence(),
    }
    response = client.post(
        url_for("blog.create_tag"),
        headers={"Authorization": f"Bearer {fake.sha256()}"},
        json=data,
    )
    assert response.status_code == 401
    assert "Invalid token" in response.json["message"]


@pytest.mark.parametrize("data, expected_error_message", [
    ({"description": fake.sentence()}, "Tag name cannot be empty"),
    ({"name": fake.word()}, "Tag description cannot be empty")
])
def test_create_blog_tag_failure_with_invalid_data(client, init_database, test_admin, data, expected_error_message):
    response = client.post(
        url_for("blog.create_tag"),
        headers={"Authorization": f"Bearer {test_admin.token}"},
        json=data,
    )
    assert response.status_code == 400
    assert expected_error_message in response.json["message"]


@pytest.mark.parametrize("new_value, un_updated_field", [
    ({"name": fake.word()}, "description"),
    ({"description": fake.sentence()}, "name"),
])
def test_update_blog_tag_success(client, init_database, test_admin, existing_blog_tag, new_value, un_updated_field):
    old_db_data = existing_blog_tag.to_dict()

    tag_id = existing_blog_tag.id
    data = new_value
    response = client.patch(
        url_for("blog.update_tag", tag_id=tag_id),
        headers={"Authorization": f"Bearer {test_admin.token}"},
        json=data,
    )

    updated_field = tuple(new_value.keys())[0]

    assert response.status_code == 200
    assert response.json[updated_field] == data[updated_field]
    assert response.json[updated_field] != old_db_data[updated_field]
    assert response.json[un_updated_field] == old_db_data[un_updated_field]
    assert response.json["id"] == existing_blog_tag.id


def test_update_blog_tag_failure_without_token(client, init_database, existing_blog_tag):
    tag_id = existing_blog_tag.id
    data = {
        "name": fake.word(),
        "description": fake.sentence(),
    }
    response = client.patch(
        url_for("blog.update_tag", tag_id=tag_id),
        json=data,
    )
    assert response.status_code == 401
    assert "Missing auth token" in response.json["message"]


def test_update_blog_tag_failure_with_invalid_token(client, init_database, existing_blog_tag):
    tag_id = existing_blog_tag.id
    data = {
        "name": fake.word(),
        "description": fake.sentence(),
    }
    response = client.patch(
        url_for("blog.update_tag", tag_id=tag_id),
        headers={"Authorization": f"Bearer {fake.sha256()}"},
        json=data,
    )
    assert response.status_code == 401
    assert "Invalid token" in response.json["message"]


def test_update_blog_tag_failure_with_invalid_tag_id(client, init_database, test_admin):
    tag_id = fake.random_int()
    data = {
        "name": fake.word(),
        "description": fake.sentence(),
    }
    response = client.patch(
        url_for("blog.update_tag", tag_id=tag_id),
        headers={"Authorization": f"Bearer {test_admin.token}"},
        json=data,
    )
    assert response.status_code == 404
    assert "Tag does not exist" in response.json["message"]


@pytest.mark.parametrize("data, expected_error_message", [
    ({"description": ""}, "Tag description cannot be empty"),
    ({"name": ""}, "Tag name cannot be empty")
])
def test_update_blog_tag_failure_with_invalid_data(
    client,
    init_database,
    test_admin,
    existing_blog_tag,
    data,
    expected_error_message
):
    tag_id = existing_blog_tag.id
    response = client.patch(
        url_for("blog.update_tag", tag_id=tag_id),
        headers={"Authorization": f"Bearer {test_admin.token}"},
        json=data,
    )

    assert response.status_code == 400
    assert expected_error_message in response.json["message"]


def test_delete_blog_tag_success(client, init_database, test_admin, existing_blog_tag):
    tag_id = existing_blog_tag.id
    response = client.delete(
        url_for("blog.delete_tag", tag_id=tag_id),
        headers={"Authorization": f"Bearer {test_admin.token}"},
    )
    assert response.status_code == 200
    assert response.json["message"] == "Tag deleted successfully"


def test_delete_blog_tag_failure_without_token(client, init_database, existing_blog_tag):
    tag_id = existing_blog_tag.id
    response = client.delete(
        url_for("blog.delete_tag", tag_id=tag_id),
    )
    assert response.status_code == 401
    assert "Missing auth token" in response.json["message"]


def test_delete_blog_tag_failure_with_invalid_token(client, init_database, existing_blog_tag):
    tag_id = existing_blog_tag.id
    response = client.delete(
        url_for("blog.delete_tag", tag_id=tag_id),
        headers={"Authorization": f"Bearer {fake.sha256()}"},
    )
    assert response.status_code == 401
    assert "Invalid token" in response.json["message"]


def test_delete_blog_tag_failure_with_invalid_tag_id(client, init_database, test_admin):
    tag_id = fake.random_int()
    response = client.delete(
        url_for("blog.delete_tag", tag_id=tag_id),
        headers={"Authorization": f"Bearer {test_admin.token}"},
    )
    assert response.status_code == 404
    assert "Tag does not exist" in response.json["message"]
