from flask import Blueprint, render_template

auth_page =  Blueprint('auth_page', __name__)

@auth_page.route("/login", methods=["GET"])
def login_route():
    return render_template("login.html", **locals())

@auth_page.route("/register", methods=["GET"])
def register_route():
    return render_template("register.html", **locals())
