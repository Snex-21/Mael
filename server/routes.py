from flask import Blueprint, render_template
from server.auth import check_admin
import psycopg2
from handlers.claves.config import db_url

routes_bp = Blueprint("routes", __name__)

@routes_bp.route("/admin")
def dashboard():
    protect = check_admin()
    if protect:
        return protect
    return render_template("dashboard.html")

@routes_bp.route("/admin/fotos")
def ver_fotos():
    protect = check_admin()
    if protect:
        return protect

    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    cur.execute("SELECT id, pais, fecha, link_foto, user_id FROM fotos ORDER BY id DESC;")
    rows = cur.fetchall()
    conn.close()

    fotos = [
        {
            "id": r[0],
            "pais": r[1],
            "fecha": r[2],
            "link_foto": r[3],
            "user_id": r[4]
        }
        for r in rows
    ]

    return render_template("fotos.html", fotos=fotos)
