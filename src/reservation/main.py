import yaml

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/reservations'

from repository.models import db
db.init_app(app)

from routes.reservation_routes import reservation_app
from routes.healthcheck import healthcheck_app

app.register_blueprint(reservation_app)
app.register_blueprint(healthcheck_app)

def config_load():
    config_yaml = yaml.safe_load(open("config.yaml"))
    app.config["port"] = config_yaml["server"]["port"]
    
    gateway_port = config_yaml["gateway"]["port"]
    gateway_hostname = config_yaml["gateway"]["hostname"]
    gateway_url = f"http://{gateway_hostname}:{gateway_port}"

    app.config["gateway"] = gateway_url

if __name__ == '__main__':
    config_load()
    app.run(host='0.0.0.0', port=app.config.get("port"))
