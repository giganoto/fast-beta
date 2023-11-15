from typing import Optional

from sqlalchemy import Column, Integer, String
from sqlalchemy.sql import func
from datetime import datetime

from app import db


class Admin(db.Model):
    """Represents an administrator in the database.

    Attributes:
        id (int): The unique identifier for the admin.
        name (str): The name of the admin.
        email (str): The email address of the admin.
        created_at (datetime): The date and time when the admin was created.
    """

    __tablename__ = "admins"
    id: int = Column(Integer, autoincrement=True, primary_key=True)
    name: str = Column(String(128), nullable=False)
    email: str = Column(String(128), nullable=False)
    created_at: datetime = Column(db.DateTime, server_default=func.now())

    def __repr__(self) -> str:
        """Represent the Admin instance as a string."""
        return f"<Admin {self.name}>"

    @classmethod
    def get(cls, email: str) -> Optional["Admin"]:
        """Get an admin with the given email.

        Args:
            email (str): The email to check.

        Returns:
            bool: True if an admin with email exists, False otherwise.
        """
        return cls.query.filter_by(email=email).first()

    @classmethod
    def create_instance(cls, name: str, email: str) -> "Admin":
        """Create a new instance of Admin.

        Args:
            name (str): The name of the admin.
            email (str): The email address of the admin.

        Returns:
            Admin: A new instance of Admin.
        """
        return cls(name=name, email=email)


class InvalidTokens(db.Model):
    """Represents a record of invalid tokens in the database.

    Attributes:
        token (str): The JWT token marked as invalid.
        created_at (datetime): The datetime when the token was marked invalid.
    """

    __tablename__ = "invalid_tokens"

    token: str = Column(String(256), primary_key=True)
    created_at: datetime = Column(db.DateTime, server_default=func.now())

    @classmethod
    def exists(cls, token: str) -> bool:
        """Check if a token is marked as invalid.

        Args:
            token (str): The token to check.

        Returns:
            bool: True if the token is marked as invalid, False otherwise.
        """
        return cls.query.filter_by(token=token).first() is not None

    @classmethod
    def create_instance(cls, token: str) -> "InvalidTokens":
        """Create a new instance of Invalid token.

        Args:
            token (str): The token to mark as invalid.

        Returns:
            InvalidTokens: A new instance of InvalidTokens.
        """
        return cls(token=token)
