from app import db
from app.models.admin import Admin, InvalidTokens
from app.utils.error import handle_exception


def create_admin(name: str, email: str) -> Admin:
    """Create a new admin instance.

    Args:
        name (str): The name of the admin.
        email (str): The email address of the admin.

    Returns:
        Admin: A new instance of Admin.
    """
    try:
        admin = Admin.create_instance(name=name, email=email)
        db.session.add(admin)
        db.session.commit()
        return admin
    except Exception as e:
        handle_exception(e, "Admin already exists")


def get_admin_by_email(email: str) -> Admin:
    """Get an admin by email.

    Args:
        email (str): The email address of the admin.

    Returns:
        Admin: The admin instance.
    """
    admin = Admin.get(email)
    if admin is None:
        raise Exception("Admin does not exist")
    return admin


def create_invalid_token(token: str) -> InvalidTokens:
    """Create a new instance of InvalidTokens.

    Args:
        token (str): The token to mark as invalid.

    Returns:
        InvalidTokens: A new instance of InvalidTokens.
    """
    try:
        invalid_token = InvalidTokens.create_instance(token=token)
        db.session.add(invalid_token)
        db.session.commit()
        return invalid_token
    except Exception as e:
        handle_exception(e, "Invalid token already exists")
