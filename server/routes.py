from flask import Blueprint, render_template
from server.auth import check_admin
from handlers.db import MaelDB

# BLUEPRINT DEL PANEL
routes_bp = Blueprint("routes", __name__)

@routes_bp.route("/admin")
def dashboard():

    r = check_admin()
    if r:
        return r

    return render_template("dashboard.html")

@routes_bp.route("/admin/fotos")
def ver_fotos():

    #proteccion al admin
    r = check_admin()
    if r:
        return r

    #conecta la BD
    db = MaelDB()
    conn = db.conexion_db()
    cur = conn.cursor()

    #obitiene un reg
    cur.execute("""
        SELECT id, pais, fecha, link_foto, user_id
        FROM fotos
        ORDER BY id DESC
    """)

    fotos = cur.fetchall()

    #aca cierra la conexión
    cur.close()
    conn.close()

    #aca envia al template
    return render_template("fotos.html", fotos=fotos)
