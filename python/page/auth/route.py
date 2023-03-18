from flask import Blueprint, render_template

auth_page_bp = Blueprint("auth_page_bp", __name__)


@auth_page_bp.route("/login", methods=["GET"])
def login_route():
    return render_template("login.html", **locals())


@auth_page_bp.route("/register", methods=["GET"])
def register_route():
    return render_template("register.html", **locals())


@auth_page_bp.route("/handle_setup", methods=["GET"])
def handle_setup():
    return render_template("handle_setup.html", **locals())


@auth_page_bp.route("/verify_mail", methods=["GET"])
def verify_mail():
    return render_template("verify_mail.html", **locals())
