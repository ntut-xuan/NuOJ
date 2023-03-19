from flask import Blueprint, render_template


submission_page_bp = Blueprint("submission_page", __name__)

@submission_page_bp.route("/submission")
def get_submission_list_page():
    return render_template("submission_list.html", **locals())

