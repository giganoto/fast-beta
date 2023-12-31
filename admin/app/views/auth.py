import requests
from flask import (
    blueprints,
    redirect,
    request,
    current_app as app,
    jsonify,
    g,
)

from app.utils.auth import generate_jwt_token, token_required
from app.controllers.admin import create_invalid_token, get_admin_by_email


auth = blueprints.Blueprint("auth", __name__, url_prefix="/api/auth")


@auth.route("/login")
def login():
    # OAUTH2 Step 1: Redirect to Google's OAuth 2.0 Server
    client_id = app.config["GOOGLE_CLIENT_ID"]
    redirect_uri = app.config["REDIRECT_URI"]
    google_login_url = (
        "https://accounts.google.com/o/oauth2/v2/auth?response_type=code&"
        f"client_id={client_id}&redirect_uri={redirect_uri}"
        "&scope=openid%20email%20profile"
    )
    return redirect(google_login_url)


@auth.route("/login/callback")
def callback():
    try:
        # OAUTH2 Step 2: Handle the OAuth 2.0 Server's response
        client_id = app.config["GOOGLE_CLIENT_ID"]
        client_secret = app.config["GOOGLE_CLIENT_SECRET"]
        redirect_uri = app.config["REDIRECT_URI"]
        auth_code = request.args.get("code")
        token_request_playload = {
            "code": auth_code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
            "client_id": client_id,
            "client_secret": client_secret,
        }
        token_request = requests.post(
            "https://oauth2.googleapis.com/token", data=token_request_playload
        )
        token_request_data = token_request.json()
        access_token = token_request_data["access_token"]

        # OAUTH2 Step 3: Use the access token to access Google's API
        user_info_res = requests.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        user_info = user_info_res.json()
        email = user_info["email"]
        if not get_admin_by_email(email):
            raise Exception("You are not authorized to access this resource")
        token = generate_jwt_token(user_info)
        return jsonify({"token": token})
    except KeyError as e:
        if "access_token" in e.args:
            return (
                jsonify(
                    {
                        "message": "Something went wrong",
                        "error": "Invalid code",
                    }
                ),
                400,
            )
    except Exception as e:
        return (
            jsonify(
                {
                    "message": "Something went wrong",
                    "error": str(e),
                }
            ),
            400,
        )


@auth.route("/logout", methods=["POST"])
@token_required
def logout():
    try:
        create_invalid_token(g.token)
        return jsonify({"message": "Logged out successfully"}), 200
    except Exception as e:
        return (
            jsonify(
                {
                    "message": "Something went wrong",
                    "error": str(e),
                }
            ),
            400,
        )


@auth.route("/secure-ping")
@token_required
def secure_ping():
    return jsonify({"message": "Secure Ping"}), 200
