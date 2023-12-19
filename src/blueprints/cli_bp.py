from flask import Blueprint
from app import db, bcrypt
from models.user import User
from models.smartwatch import Smartwatch


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
            username="Not Admin",
            email="notadmin@notadmin.com",
            password=bcrypt.generate_password_hash("defnotanadmin").decode("utf8"),
        ),
    ]

    db.session.add_all(users)
    db.session.commit()

    smartwatches = [
        Smartwatch(
            name="Apple Watch Series 9",
            brand="Apple",
            year_released=2023,
            budget="Mid Range",
            battery_life=8,
            main_feature="Health Features"

        ),
    ]

    db.session.add_all(smartwatches)
    db.session.commit()

