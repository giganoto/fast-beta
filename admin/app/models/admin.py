from sqlalchemy import Column, Integer, String

from app import db


class Admin(db.Model):
    __tablename__ = "admins"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    created_at = Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f"<Admin {self.name}>"

    @staticmethod
    def exists(email):
        return Admin.query.filter_by(email=email).first() is not None

    @staticmethod
    def add(name, email):
        db.session.add(Admin(name=name, email=email))
        db.session.commit()


class InvalidTokens(db.Model):
    __tablename__ = "invalid_tokens"

    # assuming our JWT payload will always include only iat, email, and exp
    # this length should be more than enough, at the time of writing this
    # length are under 200 characters
    token = Column(String(256), primary_key=True)
    created_at = Column(db.DateTime, server_default=db.func.now())

    @staticmethod
    def exists(token):
        return InvalidTokens.query.filter_by(token=token).first() is not None

    @staticmethod
    def add(token):
        db.session.add(InvalidTokens(token=token))
        db.session.commit()
