import json
from unittest.mock import patch

from flask import url_for


def test_login_redirect(client):
    "Test the login redirect to Google's OAuth 2.0 server."

    response = client.get(url_for("auth.login"))
    assert response.status_code == 302
    assert "accounts.google.com" in response.headers["Location"]


def test_login_callback_success(client, init_database):
    "Test successful login callback handling with a mock OAuth response."

    with patch("requests.post") as mock_post, patch("requests.get") as mock_get:
        mock_post.return_value.json.return_value = {"access_token": "test_access_token"}
        mock_get.return_value.json.return_value = {"email": "test_admin@giganoto.com"}
        response = client.get(url_for("auth.callback", code="test_code"))
        assert response.status_code == 200
        assert "token" in response.json


def test_login_callback_failure(client):
    "Test login callback handling with failure (e.g., invalid code)."

    with patch("requests.post") as mock_post:
        mock_post.return_value.json.return_value = {"error": "invalid_grant"}
        response = client.get(url_for("auth.callback", code="invalid_code"))
        assert response.status_code == 400
        assert "error" in response.json


def test_logout_success(client, init_database, test_admin):
    "Test successful logout."

    valid_token = test_admin.token
    response = client.post(
        url_for("auth.logout"), headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert response.status_code == 200
    assert response.json["message"] == "Logged out successfully"


def test_logout_failure(client):
    "Test logout with invalid token."

    invalid_token = "some_invalid_token"
    response = client.post(
        url_for("auth.logout"),
        headers={"Authorization": f"Bearer {invalid_token}"},
    )
    assert response.status_code == 401
    assert "error" in json.loads(response.data)


def test_secure_ping_access(client, init_database, test_admin):
    "Test access to secure endpoint with valid token."

    valid_token = test_admin.token
    response = client.get(
        url_for("auth.secure_ping"),
        headers={"Authorization": f"Bearer {valid_token}"},
    )
    assert response.status_code == 200
    assert json.loads(response.data)["message"] == "Secure Ping"


def test_secure_ping_access_denied(client):
    "Test access to secure endpoint without valid token."

    response = client.get(url_for("auth.secure_ping"))
    assert response.status_code == 401
    assert "Forbidden" in json.loads(response.data)["message"]


def test_secure_ping_access_invalid_token(client, init_database, test_admin):
    "Test access to secure endpoint with invalid token, e.g., after logout."

    valid_token = test_admin.token
    response = client.post(
        url_for("auth.logout"),
        headers={"Authorization": f"Bearer {valid_token}"},
    )

    should_be_invalid_token = valid_token

    response = client.get(
        url_for("auth.secure_ping"),
        headers={"Authorization": f"Bearer {should_be_invalid_token}"},
    )
    assert response.status_code == 401
    assert "Invalid token" in json.loads(response.data)["error"]
