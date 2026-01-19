from flask import Blueprint, render_template, request, redirect, session
from handlers.claves import config as cg

auth_bp = Blueprint("auth", __name__)

ADM_PASSWRD = cg.admin_password

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        pwd = request.form.get("password")

        if pwd == ADM_PASSWRD:
            session["admin"] = True
            return redirect("/admin")

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

def check_admin():
    if not session.get("admin"):
        return redirect("/login")
