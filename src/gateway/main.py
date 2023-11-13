import yaml

from flask import Flask

app = Flask(__name__)

from routes.library_routes import library_app

app.register_blueprint(library_app)

def config_load():
    config_yaml = yaml.safe_load(open("config.yaml"))
    app.config["port"] = config_yaml["server"]["port"]

if __name__ == '__main__':
    config_load()
    app.run(host='localhost', port=app.config.get("port"))
