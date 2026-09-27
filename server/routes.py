from flask import Blueprint, render_template
from server.auth import check_admin
import psycopg2
from handlers.claves.config import db_url
from handlers.countries import get_country_name

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
            "pais": get_country_name(r[1], 'es') if r[1] else '',
            "fecha": r[2],
            "link_foto": r[3],
            "user_id": r[4]
        }
        for r in rows
    ]

    return render_template("fotos.html", fotos=fotos)

@routes_bp.route("/admin/fotos/eliminar/<int:foto_id>", methods=["POST", "GET"])
def eliminar_foto(foto_id):
    protect = check_admin()
    if protect:
        return protect

    from handlers.db import MaelDB
    from handlers.img import LinkImage

    db = MaelDB()
    # Borra de la BD y nos retorna el link de la foto
    link_foto = db.borrar_por_id(foto_id)

    if link_foto:
        # Borra la imagen en Cloudinary
        img = LinkImage()
        img.borrar_foto(link_foto)

    from flask import redirect, url_for
    return redirect(url_for("routes.ver_fotos"))
