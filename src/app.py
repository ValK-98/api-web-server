from flask import Flask
from os import environ
from config import db, ma, bcrypt, jwt
from marshmallow.exceptions import ValidationError
# from flask_migrate import Migrate




app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = environ.get('JWT_KEY')

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = environ.get('DB_URI')


db.init_app(app)
ma.init_app(app)
jwt.init_app(app)
bcrypt.init_app(app)

# migrate = Migrate(app, db)

@app.errorhandler(401)
def unauthorized(err):
    return {'error': 'You are not authorized to access this resource'}

@app.errorhandler(ValidationError)
def validation_error(err):
    return {'error': err.messages}



from blueprints.auth_bp import *
from blueprints.cli_bp import cli_bp
app.register_blueprint(cli_bp)
app.register_blueprint(auth_blueprint)







