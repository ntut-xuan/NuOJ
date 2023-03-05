from flask import Blueprint, render_template

problem_page_bp = Blueprint("problem_page", __name__)


@problem_page_bp.route("/problem", methods=["GET"])
def fetch_problem_list_page_route():
    return render_template("problem_list.html", **locals())


@problem_page_bp.route("/problem/<int:id>", methods=["GET"])
def fetch_problem_info_page_route(id: int):
    return render_template("problem_info.html", **locals())
