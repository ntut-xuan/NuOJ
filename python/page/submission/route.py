from flask import Blueprint, render_template

submission_page_bp = Blueprint("submission_page", __name__)


@submission_page_bp.route("/submission", methods=["GET"])
def fetch_problem_list_page_route():
    return render_template("problem_list.html", **locals())
