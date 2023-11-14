from flask import Blueprint, request, current_app

gateway_app = Blueprint("gateway", __name__, url_prefix="/")

@gateway_app.route("/manage/health")
def get_libraries():
    return "", 200