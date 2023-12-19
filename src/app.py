# app.py
from flask import Flask, jsonify
from os import environ
from config import db, ma, bcrypt, jwt
import logging
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound, BadRequest
# Import blueprints
from blueprints.auth_bp import *
from blueprints.cli_bp import cli_bp
from blueprints.smartwatches_bp import smartwatch_bp
from blueprints.user_smartwatches_bp import user_smartwatches_bp

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask application instance
app = Flask(__name__)

# Configure application with environment variables
app.config['JWT_SECRET_KEY'] = environ.get('JWT_KEY')
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('DB_URI')

# Initialize extensions with app context
db.init_app(app)
ma.init_app(app)
jwt.init_app(app)
bcrypt.init_app(app)

# Error handling for various exceptions
@app.errorhandler(401)
def unauthorized_error_handler(error):
    # Unauthorized access error
    return jsonify({'error': 'Unauthorized access'}), 401

@app.errorhandler(ValidationError)
def validation_error_handler(error):
    # Data validation error
    return jsonify({'error': error.messages}), 400

@app.errorhandler(IntegrityError)
def integrity_error_handler(error):
    # Database integrity error
    db.session.rollback() 
    return jsonify({'error': 'Database integrity error'}), 400

@app.errorhandler(NotFound)
def not_found_error_handler(error):
    # Resource not found error
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(BadRequest)
def bad_request_error_handler(error):
    # Bad request error
    return jsonify({'error': 'Bad request'}), 400

@app.errorhandler(Exception)
def general_error_handler(error):
    # General error handler for unexpected exceptions
    logging.error(f'Unexpected error: {error}', exc_info=True)
    return jsonify({'error': 'An unexpected error occurred'}), 500

# Register blueprints with the application
app.register_blueprint(cli_bp)
app.register_blueprint(auth_blueprint)
app.register_blueprint(smartwatch_bp)
app.register_blueprint(user_smartwatches_bp)







