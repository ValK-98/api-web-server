from flask import Blueprint
from app import db, bcrypt
from models.user import User


cli_bp = Blueprint('db', __name__)

@cli_bp.cli.command("create")
def db_create():
    db.drop_all()
    db.create_all()
    print("Created tables")


@cli_bp.cli.command("seed")
def db_seed():
    users = [
        User(
            username = "admin",
            email="admin@admin.com",
            password=bcrypt.generate_password_hash("adminadmin").decode("utf8"),
            is_admin=True,
        ),
        User(
            name="Not Admin",
            email="notadmin@notadmin.com",
            password=bcrypt.generate_password_hash("defnotanadmin").decode("utf8"),
        ),
    ]

    db.session.add_all(users)
    db.session.commit()