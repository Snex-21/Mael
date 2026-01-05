import cloudinary
import cloudinary.uploader as clup
from .claves import config as cg

class LinkImage():
    
    # me conecto a la cuenta de cloudinary
    def __init__(self):
        self.cloudi = cloudinary.config(
            cloud_name = cg.cloud_name,
            api_key = cg.api_key,
            api_secret = cg.api_secret,
        )
        
    # subo la ft a cloudinary
    def link_image(self, ruta= cg.root_dir / 'downloads' / 'ultima_imagen.jpg'):
        self.ruta = ruta
        resultado = clup.upload(
            self.ruta,
            folder = cg.cloudinary_folder,
        )
        # retorna el link de la ft
        return resultado['secure_url']