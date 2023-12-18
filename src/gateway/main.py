import yaml

from flask import Flask

app = Flask(__name__)

from routes.library_routes import library_app
from routes.rating_routes import rating_app
from routes.reservation_routes import reservation_app
from routes.gateway_routes import gateway_app

app.json.ensure_ascii = False

app.register_blueprint(library_app)
app.register_blueprint(rating_app)
app.register_blueprint(reservation_app)
app.register_blueprint(gateway_app)


def config_load():
    config_yaml = yaml.safe_load(open("config.yaml"))
    app.config["port"] = config_yaml["server"]["port"]
    for service in config_yaml["services"]:
        for key in service.keys():
            service_name = key
            hostname = service[key]["hostname"]
            port = service[key]["port"]
            url = f"http://{hostname}:{port}"
            app.config[service_name] = url


if __name__ == '__main__':
    config_load()
    app.run(host='0.0.0.0', port=app.config.get("port"))
