from flask import Blueprint
from app import db, bcrypt
from models.user import User
from models.smartwatch import Smartwatch
from models.user_smartwatch import UserSmartwatch


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
            username = "admin2",
            email="admin2@admin.com",
            password=bcrypt.generate_password_hash("adminadmin").decode("utf8"),
            is_admin=True,
        ),
        User(
            username="Not Admin",
            email="notadmin@notadmin.com",
            password=bcrypt.generate_password_hash("defnotanadmin").decode("utf8"),
        ),
        User(
            username="PlaceH1",
            email="PlaceH1@notadmin.com",
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
        battery_life=18,
        main_feature="Health Features"
    ),
    Smartwatch(
        name="Galaxy Watch 5",
        brand="Samsung",
        year_released=2023,
        budget="High",
        battery_life=50,
        main_feature="Connectivity"
    ),
    Smartwatch(
        name="FitPro Flex",
        brand="FitPro",
        year_released=2022,
        budget="Economy",
        battery_life=96,
        main_feature="Long Battery Life"
    ),
    Smartwatch(
        name="Xiaomi Mi Band 6",
        brand="Xiaomi",
        year_released=2021,
        budget="Low",
        battery_life=14,
        main_feature="Sleep Tracking"
    ),
    Smartwatch(
        name="Garmin Forerunner 55",
        brand="Garmin",
        year_released=2021,
        budget="Premium",
        battery_life=20,
        main_feature="GPS Tracking"
    ),
]

    db.session.add_all(smartwatches)
    db.session.commit()

    
    user_smartwatches = [
        UserSmartwatch(user_id=1, smartwatch_id=1),  
        UserSmartwatch(user_id=2, smartwatch_id=2),
        
    ]
    db.session.add_all(user_smartwatches)
    db.session.commit()

