from flask import Blueprint, make_response

system_bp = Blueprint("system", __name__, url_prefix="/api/")

@system_bp.route("/heartbeat", methods=["GET"])
def fetch_heartbeat():
    return make_response({"message": "OK"})