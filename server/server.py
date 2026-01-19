from flask import Flask, redirect
import os
from handlers.claves import config as cg
from server.routes import routes_bp
from server.auth import auth_bp

UPLOAD_FOLDER = "uploads"

app = Flask(
    __name__,
    template_folder="templates",   
    static_folder="static"
)

app.secret_key = cg.flask_secret

app.register_blueprint(auth_bp)
app.register_blueprint(routes_bp)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def home():
    return redirect("/login")

port = int(os.environ.get("PORT", 10000))

def run_flask():
    app.run(host="0.0.0.0", port=port)
