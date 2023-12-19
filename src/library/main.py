import yaml

from flask import Flask

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/libraries'
app.json.ensure_ascii = False

from db.models import db

db.init_app(app)

from routes.library_routes import library_app
from routes.healthcheck import healthcheck_app

app.register_blueprint(library_app)
app.register_blueprint(healthcheck_app)


def config_load(config_path: str):
    config_yaml = yaml.safe_load(open(config_path))
    app.config["port"] = config_yaml["server"]["port"]
    app.config["host"] = config_yaml["server"].get("host") or "0.0.0.0"


if __name__ == '__main__':
    config_load("config_local.yaml")
    app.run(host=app.config.get("host"), port=app.config.get("port"))
