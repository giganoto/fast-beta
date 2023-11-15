import sqlalchemy

from app import db


def handle_exception(e: Exception, msg: str = None):
    """Handle exceptions by rolling back the session and raising the exception.

    Args:
        e (Exception): The exception to handle.

    Raises:
        Exception: The exception that was handled.
    """
    db.session.rollback()
    if isinstance(e, sqlalchemy.exc.IntegrityError):
        raise ValueError(msg) from e
    else:
        raise e
