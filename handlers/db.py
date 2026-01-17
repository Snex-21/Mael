import psycopg2 as psy
from .claves import config 
import requests
import random
from datetime import datetime 

class MaelDB:
    def __init__(self):
        # url de la bd 
        self.db_url = config.db_url
        self.conexion_db()
        
        carpeta_dowloands = config.root_dir / 'downloads'
        carpeta_dowloands.mkdir(parents=True, exist_ok=True)
    
    # conexion con la bd
    def conexion_db(self):
        conexion = psy.connect(
            dsn = self.db_url
        )
        return conexion
    
    # para añadir a la bd la foto con su fecha y pais
    def insertar_dato(self, pais, fecha, foto, user_id):
        self.pais = pais
        # pasando la fecha a formato dia/mes/año con los slash
        self.fecha = datetime.strptime(fecha, '%d/%m/%Y').date()
        # aca se le pasa el link de la foto
        self.foto = foto
        # id del usuario 
        self.user_id = user_id
        
        conexion = self.conexion_db()
        cursor = conexion.cursor()
        query = 'INSERT INTO fotos (pais, fecha, link_foto, user_id) VALUES (%s, %s,%s,%s)'
        
        cursor.execute(query, (self.pais, self.fecha, self.foto, self.user_id))
        conexion.commit()
        
        cursor.close()
        conexion.close()
        
    # obtener una foto buscandola por la fecha
    def obtener_dato(self, fecha):
        # pasando la fecha a formato dia/mes/año con los slash
        self.fecha = datetime.strptime(fecha, '%d/%m/%Y').date()
        conexion = self.conexion_db()
        cursor = conexion.cursor()
        
        cursor.execute('SELECT * FROM fotos WHERE fecha = %s;', (self.fecha,))
        registros = cursor.fetchall()
        
        # si no hay foto de esa fecha retorna nada (proximamente le tengo que poner algo)
        if not registros:
            return None
        
        # si hay mas de una foto de una foto con esaa foto elije una random
        if len(registros) > 1:
            url = random.choice(registros)[3]
        
        else:
            # si solo hay una, la selecciona (toma el link)
            url = registros[0][3]
        
        cursor.close()
        conexion.close()
        
        # retorna el link
        return url
    
    # para borrar toda la bd
    def borrar_todo(self):
        conexion = self.conexion_db()
        cursor = conexion.cursor()
        cursor.execute('TRUNCATE TABLE fotos RESTART IDENTITY;')
        conexion.commit()
        cursor.close()
        conexion.cursor()
    
    # para borrar un una foto en especifico (por ID)
    def borrar_por_id(self, id):
        conexion = self.conexion_db()
        cursor = conexion.cursor()
        cursor.execute('DELETE FROM fotos WHERE id = %s;', (id,))
        conexion.commit()
        cursor.close()
        conexion.close()
    
    # atributo para descargar la foto
    def foto(self,photo):
        self.photo = photo
        url = self.obtener_dato(self.photo)
        if url == None:
            return None
        else:
            estado = requests.get(url)
            
            # ruta relativa de la ultima imagen descargada para posteriormente mandarsela al usuario
            ruta = config.root_dir / 'downloads' / 'imagen.jpg'
            
            if estado.status_code == 200:
                with open(ruta, 'wb') as f:
                    f.write(estado.content)
            
            # retorna la ruta donde se descargo la ft
            return ruta
    
    # atributo para ver las fotos aportadas por un usuario
    def fotos_aportadas(self, id):
        
        # id del usuario
        self.id = id
        conexion = self.conexion_db()
        cursor = conexion.cursor()
        
        # busca todas las fechas que haya con el id del usuario
        query = 'SELECT fecha FROM fotos WHERE user_id = %s ORDER BY fecha ASC'
        
        with cursor:
            cursor.execute(query, (self.id,))
            resultado = cursor.fetchall()
            fechas = []
            if resultado == None:
                return fechas
            print(resultado)
            for i in resultado:
                # guardo las fechas en una tupla y despues la retorno
                fechas.append(i[0])
                print(i)
                print(fechas)
            return fechas