from flask import Flask
import os
from handlers.claves import config as cg
from server.routes import routes_bp
from server.auth import auth_bp

app = Flask(
    __name__,
    template_folder="templates",  
    static_folder="static"
)

app.secret_key = cg.flask_secret

app.register_blueprint(auth_bp)
app.register_blueprint(routes_bp)

@app.route("/")
def home():
    return "Mael activo"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
