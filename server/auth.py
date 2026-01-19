from flask import Blueprint, render_template, request, redirect, session
from handlers.claves import config as cg
auth_bp = Blueprint("auth", __name__)


ADMIN_PASSWRD = cg.ADMIN_PASSWRD
KEY_SECRET = cg.KEY_SECRET

@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        password = request.form.get("password")

        #comprueba si la contraseña coincide
        if password == ADMIN_PASSWRD:
            session["admin"] = True
            return redirect("/admin")

    #si no es POST o falla el login
    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

#función para proteger rutas adm
def check_admin():
    if not session.get("admin"):
        return redirect("/login")


#el que lea esto es gay
#solo pongo el msj para re subir y confirmar cambios