# Mael — Telegram Bot

Mael es un bot de Telegram que guarda y muestra imágenes del cielo, como fotos de nubes, atardeceres, lunas o cielos nocturnos.

Los usuarios pueden enviar imágenes o solicitar que Mael muestre fotos guardadas previamente, todo a través de comandos simples y directos.

---

## Comandos disponibles

| Comando | Descripción |
|------|-----------|
| `/start` | Inicia el bot |
| `/info` | Muestra información general y ayuda |
| `/buscar` | Busca y muestra imágenes del cielo según lo indicado |
| `/agg` | Agrega nuevas imágenes del cielo al sistema |

---

## Tecnologías utilizadas
- **Python** como lenguaje principal.
- **[Pyrogram](https://docs.pyrogram.org/) + [tgcrypto](https://github.com/pyrogram/tgcrypto)**: para la gestión del bot en Telegram.
- **PostgreSQL + [psycopg2](https://www.psycopg.org/docs/)**: PostgreSQL es la base de datos donde se guarda la información (imágenes, datos asociados, etc.). 
psycopg2 es la librería que permite a Python conectarse y comunicarse con PostgreSQL.
- **[Cloudinary](https://cloudinary.com/)**: Servicio en la nube utilizado para almacenar las imágenes del cielo.
Se usa junto con su librería oficial (**[pycloudinary](https://github.com/cloudinary/pycloudinary)**) para subir, organizar y manejar automáticamente las fotos.
- **[Flask](https://flask.palletsprojects.com/)**: Para exponer el bot en la web y permitir alojarlo en un servidor, gestionando solicitudes HTTP si decides integrarlo o desplegarlo online.

---

## Instalación (modo desarrollo)

1. Clonar el repositorio:
   ```sh
   git clone https://github.com/Snex-21/Mael.git
   ```
1.5 **(Recomendado) Crea un entorno virtual**
   ```sh
   python -m venv venv
   ```
   ```sh
   source venv/bin/activate  # En Linux/Mac
   ```
   ```sh
   .\venv\Scripts\activate     # En Windows
   ```

2. **Instala las dependencias**
   ```sh
   pip install -r requirements.txt
   ```

3. **configurar variables de entorno**
   - Renombra `.env.exemple` a `.env`
   - Completa con tus datos

4. **ejecuta el bot**
    ```sh
    python main.py
    ```

---

## futuras implementaciones

- [ ] panel de control (para admin):
    - [ ] poder autorizar o no que foto se sube a la bd y al cloudinary
    - [ ] poder ver la cantidad de fotos que hay, con sus fechas y paises
        - [ ] poder el ver la cantidad de fotos con cierta fecha o pais (de ser posible ordenados del mayor al menor)
    - [ ] poder ver la persona que mas aportó 
    - [ ] poder eliminar una foto de la bd y del cloudinary
    - [ ] poder agg comentarios privado
    - [ ] detección de imágenes duplicadas
        - [ ] descarte automatico de imágenes duplicadas
<<<<<<< HEAD
- [ ] que se guarde en la bd el id del usuario que agregó la foto
    - [ ] que el usuario pueda ver las fotos que aportó
=======
- [x] que se guarde en la bd el id del usuario que agregó la foto
    - [x] que el usuario pueda ver las fotos que aportó
>>>>>>> c2c387293b8b974d619f636b203e48af2ea9dfce
    - [ ] agregar una forma de que el usuario que mando una foto pueda borrarla si quiere (por id)
- [ ] mejor manejo de las fechas
- [ ] mejora de errores y excepciones provocadas por el usuario
- [ ] mejorar los mensajes de Mael
- [ ] comando para ver la ultima foto agg
- [ ] si un usuario probó con 5 fechas y ninguna tiene foto, que el bot le mande 5 fechas que tengan foto al azar
- [ ] poner en alguna parte la cantidad de fotos que hay disponibles (se va actualizando cada que se consulte)
- [ ] que el bot pueda obtener el arroba del usuario y si esta disponible (si no con su ID) preuntarle si quiere que esa información aparezca con su foto
---

## Licencia

Este proyecto está licenciado bajo la licencia **[MIT License](LICENSE)**.

## ¿Preguntas, sugerencias o bugs?

Abre un [issue](https://github.com/Snex-21/Lazarus/issues) en el repositorio.

---

>**Hecho con gusto y dedicación por Snex**

Colaborador: Mik0-T3ch
