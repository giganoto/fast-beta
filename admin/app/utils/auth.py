import datetime
from functools import wraps

import jwt
from flask import abort, current_app as app, request, g

from app.models.admin import Admin, InvalidTokens


JWT_ALGORITHM = "HS256"


def generate_jwt_token(user_info):
    try:
        payload = {
            "exp": (
                datetime.datetime.utcnow()
                + datetime.timedelta(hours=app.config["JWT_EXP_HOURS"])
            ),
            "iat": datetime.datetime.utcnow(),
            "sub": user_info["email"],
        }
        return jwt.encode(payload, app.config["SECRET_KEY"], algorithm=JWT_ALGORITHM)
    except Exception as e:
        return e


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token:
            abort(403, "Token is missing")
        if InvalidTokens.exists(token):
            abort(403, "Invalid token")
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=JWT_ALGORITHM)
            current_admin = Admin.query.filter_by(email=data["sub"]).first()
            if not current_admin:
                abort(403, "Admin not found")
            g.current_admin = current_admin
            g.token = token
        except Exception as err:
            abort(403, str(err))

        return f(*args, **kwargs)

    return decorated
