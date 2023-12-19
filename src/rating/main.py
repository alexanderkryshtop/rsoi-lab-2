import yaml
from flask import Flask

from repository.models import db
from routes.healthcheck import healthcheck_app
from routes.rating_routes import rating_app


def load_config(app: Flask, config_path: str):
    with open(config_path, "r") as config_file:
        config_yaml = yaml.safe_load(config_file)
    app.config.update(
        port=config_yaml["server"]["port"],
        host=config_yaml["server"].get("host", "0.0.0.0"),
        SQLALCHEMY_DATABASE_URI=(
            f"postgresql+psycopg2://{config_yaml['postgres']['username']}:{config_yaml['postgres']['password']}"
            f"@{config_yaml['postgres']['host']}:{config_yaml['postgres']['port']}/{config_yaml['postgres']['database']}"
        )
    )


def create_app(config_filename):
    app = Flask(__name__)

    load_config(app, config_filename)
    app.json.sort_keys = False

    db.init_app(app)

    app.register_blueprint(rating_app)
    app.register_blueprint(healthcheck_app)

    return app


if __name__ == '__main__':
    app = create_app("config_local.yaml")
    app.run(host=app.config.get("host"), port=app.config.get("port"))
