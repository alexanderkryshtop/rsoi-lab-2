import yaml

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/libraries'
app.json.ensure_ascii = False

from repository.models import db
db.init_app(app)

from routes.library_routes import library_app
from routes.healthcheck import healthcheck_app

app.register_blueprint(library_app)
app.register_blueprint(healthcheck_app)

def config_load():
    config_yaml = yaml.safe_load(open("config.yaml"))
    app.config["port"] = config_yaml["server"]["port"]

if __name__ == '__main__':
    config_load()
    app.run(host='0.0.0.0', port=app.config.get("port"))
