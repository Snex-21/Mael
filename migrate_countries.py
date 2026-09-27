import psycopg2
from handlers.countries import parse_country_to_code
from handlers.claves.config import db_url
from handlers.db import MaelDB

def migrate_countries():
    if not db_url:
        print("Error: No se encontró 'db_url' en las variables de entorno.")
        return

    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        
        cur.execute("SELECT id, pais FROM fotos WHERE pais IS NOT NULL AND pais != '';")
        rows = cur.fetchall()
        
        print(f"Total registros a evaluar: {len(rows)}")
        modificados = 0
        
        for foto_id, pais_actual in rows:
            pais_actual_str = str(pais_actual).strip()
            codigo_iso = parse_country_to_code(pais_actual_str)
            
            if codigo_iso != pais_actual_str:
                cur.execute("UPDATE fotos SET pais = %s WHERE id = %s;", (codigo_iso, foto_id))
                modificados += 1
                print(f"ID {foto_id}: '{pais_actual_str}' -> '{codigo_iso}'")
        
        conn.commit()

        cur.execute("SELECT id, pais FROM fotos ORDER BY id;")
        print("\nTodos los IDs y países en la base de datos:")
        for foto_id, pais in cur.fetchall():
            print(f"ID {foto_id}: {pais}")

        cur.close()
        conn.close()
        print(f"Migración completada con éxito. Registros actualizados: {modificados}")
    except Exception as e:
        print(f"Error durante la migración: {e}")

if __name__ == '__main__':
    migrate_countries()
    # MaelB().borrar_y_reordenar(99)
    MaelDB().ver_datos()