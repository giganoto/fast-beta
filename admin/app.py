import os

from app import create_app, db
from app.config import DevConfig


app = create_app(DevConfig)


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "app": app}


if __name__ == "__main__":
    with app.app_context():
        from app.models.admin import Admin
        from app.models.blog import Blog, BlogCategory, BlogTag  # noqa: F401

        db.create_all()

        name, email = app.config["ADMIN_NAME"], app.config["ADMIN_EMAIL"]
        if not Admin.get(email):
            admin = Admin.create_instance(name=name, email=email)
            db.session.add(admin)
            db.session.commit()

    debug = True if os.getenv("environment") in ("development", "testing") else False
    app.run(debug=debug, host="0.0.0.0", port=8080)
