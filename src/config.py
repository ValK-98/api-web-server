# config.py
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# Initialize database instance
db = SQLAlchemy()

# Initialize Marshmallow for data serialization and deserialization
ma = Marshmallow()

# Initialize Bcrypt for password hashing
bcrypt = Bcrypt()

# Initialize JWT Manager for handling JSON Web Tokens
jwt = JWTManager()
