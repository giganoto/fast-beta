import sentry_sdk
import sqlalchemy
from flask import abort
from werkzeug.exceptions import HTTPException

from app import db


class GiganotoException(Exception):
    def __init__(self, error_message: str):
        self.error_message = error_message

    def __str__(self):
        return f"Model Validates Error: {self.error_message}"


def handle_exception(e: Exception, msg: str = None):
    """Handle exceptions by rolling back the session and returning a 400 response.

    Args:
        e (Exception): The exception to handle.
        msg (str, optional): The message to return. Defaults to None.

    Returns:
        Response: A 4XX response with an error message.
    """
    db.session.rollback()
    sentry_sdk.capture_exception(e)  # This will be ignored for testing environment
    if isinstance(e, sqlalchemy.exc.IntegrityError):
        msg = msg if msg else "DB Integrity Error"
    elif isinstance(e, HTTPException):
        return abort(e.code, e.description)
    else:
        msg = msg if msg else str(e)
    return abort(400, msg)
