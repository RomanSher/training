from flask_sqlalchemy import SQLAlchemy


SQLALCHEMY_DATABASE_URI = 'sqlite:///payments.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

db = SQLAlchemy()
