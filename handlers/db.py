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
        
        cursor.execute('SELECT pais, fecha, link_foto FROM fotos WHERE fecha = %s;', (self.fecha,))
        registros = cursor.fetchall()
        
        # si no hay foto de esa fecha retorna nada (proximamente le tengo que poner algo)
        if not registros:
            cursor.close()
            conexion.close()
            return None, None
        
        # si hay mas de una foto con esa fecha elije una random
        if len(registros) > 1:
            registro = random.choice(registros)
            pais = registro[0]
            url = registro[2]
        else:
            # si solo hay una, la selecciona (toma el link y el pais)
            pais = registros[0][0]
            url = registros[0][2]
        
        cursor.close()
        conexion.close()
        
        # retorna el link y el pais
        return url, pais
    
    # para borrar toda la bd
    def borrar_todo(self):
        conexion = self.conexion_db()
        cursor = conexion.cursor()
        cursor.execute('TRUNCATE TABLE fotos RESTART IDENTITY;')
        conexion.commit()
        cursor.close()
        conexion.close()
    
    # para borrar una foto en específico (por ID) borrando la fila y reordenando IDs
    def borrar_por_id(self, id):
        conexion = self.conexion_db()
        cursor = conexion.cursor()
        
        # 1. Obtener la URL de la foto antes de borrar para eliminar de Cloudinary
        cursor.execute('SELECT link_foto FROM fotos WHERE id = %s;', (id,))
        registro = cursor.fetchone()
        link_foto = registro[0] if registro else None
        
        if link_foto:
            # 2. Borrar el registro
            cursor.execute('DELETE FROM fotos WHERE id = %s;', (id,))
            conexion.commit()
            
            # 3. Reordenar los IDs y reiniciar el contador de la secuencia
            self.reordenar_ids(cursor, conexion)
            
        cursor.close()
        conexion.close()
        return link_foto

    # Reordena secuencialmente los IDs de 1 a N y reinicia la secuencia SERIAL de PostgreSQL
    def reordenar_ids(self, cursor=None, conexion=None):
        cerrar_conexion = False
        if cursor is None:
            conexion = self.conexion_db()
            cursor = conexion.cursor()
            cerrar_conexion = True

        try:
            # Reasignar IDs en orden continuo
            cursor.execute('''
                WITH reordered AS (
                    SELECT id, ROW_NUMBER() OVER (ORDER BY id) AS new_id
                    FROM fotos
                )
                UPDATE fotos
                SET id = reordered.new_id
                FROM reordered
                WHERE fotos.id = reordered.id;
            ''')
            
            # Reiniciar la secuencia al máximo ID actual + 1
            cursor.execute('''
                SELECT setval(pg_get_serial_sequence('fotos', 'id'), COALESCE(MAX(id), 0) + 1, false) FROM fotos;
            ''')
            conexion.commit()
        except Exception as e:
            print(f"Error al reordenar IDs: {e}")

        if cerrar_conexion:
            cursor.close()
            conexion.close()
    
    # obtener la última foto agregada
    def obtener_ultima_foto(self):
        conexion = self.conexion_db()
        cursor = conexion.cursor()
        cursor.execute('SELECT pais, fecha, link_foto FROM fotos ORDER BY id DESC LIMIT 1;')
        registro = cursor.fetchone()
        cursor.close()
        conexion.close()
        return registro
    
    # atributo para descargar la foto
    def foto(self, photo):
        self.photo = photo
        url, pais = self.obtener_dato(self.photo)
        if url is None:
            return None, None
        else:
            estado = requests.get(url)
            
            # ruta relativa de la ultima imagen descargada para posteriormente mandarsela al usuario
            ruta = config.root_dir / 'downloads' / 'imagen.jpg'
            
            if estado.status_code == 200:
                with open(ruta, 'wb') as f:
                    f.write(estado.content)
            
            # retorna la ruta donde se descargo la ft y el codigo de pais
            return ruta, pais
    
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
            if resultado is None:
                return fechas
            for i in resultado:
                # guardo las fechas en una tupla y despues la retorno
                fechas.append(i[0])
            return fechas

    # obtener lista de países únicos registrados en la base de datos (códigos ISO)
    def obtener_paises_unicos(self):
        conexion = self.conexion_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT DISTINCT pais FROM fotos WHERE pais IS NOT NULL AND pais != '' ORDER BY pais ASC;")
        registros = cursor.fetchall()
        cursor.close()
        conexion.close()
        paises_unicos = []
        for r in registros:
            if r[0]:
                p = r[0].strip().upper()
                if p not in paises_unicos:
                    paises_unicos.append(p)
        return paises_unicos
    
    # Atributo para ver las fotos con su pais y ID
    def ver_datos(self):
        try:
            conexion = self.conexion_db()
            cursor = conexion.cursor()
            cursor.execute("SELECT id, pais, fecha FROM fotos ORDER BY id;")
            registros = cursor.fetchall()
            print(f"Total registros en la base de datos: {len(registros)}")
            for foto_id, pais, fecha in registros:
                print(f"ID {foto_id}: {pais} - {fecha}")
            cursor.close()
            conexion.close()
        except Exception as e:
            print(f"Error al ver los datos: {e}") 
    