from flask import Flask
import os

app = Flask('__name__')

@app.route('/', methods=['GET'])
def home():
    return 'Mael activo', 200

port = int(os.environ.get("PORT", 10000))

def run_flask():
    app.run(host='0.0.0.0', port=port)