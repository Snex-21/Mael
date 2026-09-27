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

    # elimina una imagen de Cloudinary a partir de su URL
    def borrar_foto(self, url):
        try:
            # extraer el public_id de la URL de Cloudinary
            # Ej URL: https://res.cloudinary.com/demo/image/upload/v1234567/folder/public_id.jpg
            # public_id con carpeta: folder/public_id
            partes = url.split(f"/{cg.cloudinary_folder}/")
            if len(partes) > 1:
                filename = partes[1].split('.')[0] # Quita la extensión (.jpg, .png)
                public_id = f"{cg.cloudinary_folder}/{filename}"
            else:
                filename = url.split('/')[-1].split('.')[0]
                public_id = filename
                
            resultado = clup.destroy(public_id)
            return resultado.get("result") == "ok"
        except Exception as e:
            print(f"Error al borrar foto de Cloudinary: {e}")
            return False