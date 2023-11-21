import pytest
from faker import Faker
from flask import url_for

from app.controllers.blogs import get_all_blogs, get_all_blogs_by_category, get_all_blogs_by_tag


fake = Faker()


def test_get_all_blogs_success(client, init_database):
    response = client.get(url_for("blog.get_all"))
    assert response.status_code == 200

    all_blogs_in_db = get_all_blogs()
    assert len(response.json) == len(all_blogs_in_db)

    for index in range(len(all_blogs_in_db)):
        assert response.json[index]["title"] == all_blogs_in_db[index]["title"]
        assert response.json[index]["description"] == all_blogs_in_db[index]["description"]
        assert response.json[index]["content"] == all_blogs_in_db[index]["content"]
        assert response.json[index]["category"] == all_blogs_in_db[index]["category"]
        assert response.json[index]["tags"] == all_blogs_in_db[index]["tags"]
        assert response.json[index]["created_at"] == all_blogs_in_db[index]["created_at"]


def test_get_all_blogs_with_pagination(client, init_database):
    response = client.get(url_for("blog.get_all"), query_string={"limit": 3, "offset": 2})
    assert response.status_code == 200
    assert len(response.json) == 3
    assert response.json[0]["title"] == get_all_blogs()[2]["title"]
    assert response.json[1]["title"] == get_all_blogs()[3]["title"]
    assert response.json[2]["title"] == get_all_blogs()[4]["title"]


def test_get_all_blogs_by_category_success(client, init_database, existing_blog_category):
    response = client.get(url_for("blog.get_all_by_category", category_id=existing_blog_category.id))
    assert response.status_code == 200
    for blog in response.json:
        assert blog["category"]["id"] == existing_blog_category.id
