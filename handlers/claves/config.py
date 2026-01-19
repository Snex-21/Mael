from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

tg_api = os.getenv("telegram_api")
api_id = os.getenv("api_id")
api_hash = os.getenv("api_hash")
db_url = os.getenv("db_url")
cloud_name = os.getenv("cloud_name")
api_key = os.getenv("api_key")
api_secret = os.getenv("api_secret")
cloudinary_folder = os.getenv("cloudinary_folder")
admin_password = os.getenv("ADMIN_PASSWORD")
flask_secret = os.getenv("FLASK_SECRET_KEY")
root_dir = Path(__file__).resolve().parent.parent.parent
