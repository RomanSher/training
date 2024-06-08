from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate

from config import db
from services import app_route


app = Flask(__name__)
api = Api(app)
app.config.from_pyfile('config.py')
app.register_blueprint(app_route)

db.init_app(app)
migrate = Migrate(app, db)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0')
