import yaml

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/ratings'

from repository.models import db
db.init_app(app)

from routes.rating_routes import rating_app

app.register_blueprint(rating_app)

def config_load():
    config_yaml = yaml.safe_load(open("config.yaml"))
    app.config["port"] = config_yaml["server"]["port"]

if __name__ == '__main__':
    config_load()
    app.run(host='localhost', port=app.config.get("port"))
