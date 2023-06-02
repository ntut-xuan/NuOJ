from flask import Blueprint, render_template

profile_page_bp = Blueprint("profile_page", __name__)


@profile_page_bp.route("/profile/<string:name>", methods=["GET"])
def fetch_profile_page_route():
    return render_template("profile.html", **locals())