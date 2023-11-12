import os
from dotenv import load_dotenv


load_dotenv()


class Config:
    SECRET_KEY = os.getenv("secret_key", "secret-that-no-one-can-guess-ever")
    SENTRY_DSN = os.getenv("sentry_dsn")

    GOOGLE_CLIENT_ID = os.getenv("client_id")
    GOOGLE_CLIENT_SECRET = os.getenv("client_secret")

    REDIRECT_URI = "http://localhost:8080/"

    # keep this as single source of truth for cron job and token generation
    JWT_EXP_HOURS = 24

    host = "localhost" if os.getenv("environment") == "testing" else "postgres"
    DATABASE_URI = os.getenv(
        "DATABASE_URI", f"postgresql://admin:admin@{host}:5432/admin_db"
    )
    SQLALCHEMY_DATABASE_URI = DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
