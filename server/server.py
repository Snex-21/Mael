from flask import Flask
import os
from handlers.claves import config as cg

app = Flask(__name__)

app.secret_key = cg.KEY_SECRET

@app.route('/', methods=['GET'])
def home():
    return 'Mael activo', 200

port = int(os.environ.get("PORT", 10000))

def run_flask():
    app.run(host='0.0.0.0', port=port)
