from dotenv import load_dotenv
import os

# cargo todas las variables de entorno
load_dotenv()

# las guardo y despues las importo
# de Tg
tg_api = os.getenv('telegram_api')
api_id = os.getenv('api_id')
api_hash = os.getenv('api_hash')
# URL de la bd
db_url = os.getenv('db_url')
# de Cloudinary
cloud_name = os.getenv('cloud_name')
api_key = os.getenv('api_key')
api_secret = os.getenv('api_secret')
cloudinary_carpeta = os.getenv('cloudinary_folder')

from pathlib import Path

# ruta relativa para la carpeta raiz del proyecto
root_dir = Path(__file__).resolve().parent.parent.parent