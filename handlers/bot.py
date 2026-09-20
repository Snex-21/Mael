from pyrogram import Client, filters
from .img import LinkImage
from .db import MaelDB
from .claves import config

# el bot en cuestion
class Mael:
    def __init__(self, api_tg , api_id, api_hash, nombre = 'Mael'):
        self.nombre = nombre
        self.api_tg = api_tg
        self.api_id = api_id
        self.api_hash = api_hash
        
        # conexion con el bot
        self.bot = Client(
            name = self.nombre,
            bot_token = self.api_tg,
            api_hash = self.api_hash,
            api_id = self.api_id,
        )
        
        self.comandos()
        
        carpeta_dowloands = config.root_dir / 'downloads'
        carpeta_dowloands.mkdir(parents=True, exist_ok=True)
        
    # un atributo que filtra el mensaje del usuario en un estado en especifico
    def esperando_datos(self):
        async def func(flt, _, message):
            user_id = message.from_user.id
            return self.user_states.get(user_id) == 'esperando datos'
        return filters.create(func)
    
    # otro atributo que filtra el mensaje del usuario en un estado en especifico
    def esperando_fecha(self):
        async def funcion(flt, _, message):
            user_id = message.from_user.id
            return self.user_states.get(user_id) == 'esperando fecha'
        return filters.create(funcion)
        
    # los comandos del bot
    def comandos(self):
        
        self.user_states = {}
        self.user_data = {}
        
        # ruta de la ultima imagen que pasó el usuario
        self.path = config.root_dir / 'downloads' / 'ultima_imagen.jpg'

        @self.bot.on_message(filters.command('start'))
        async def start_command(client, message):
            await message.reply_text("Hola, soy Mael :) guardo fotos del cielo y puedo mostrártelas cuando quieras.\n\nSi querés saber cómo usar mis comandos, escribí /info y te cuento todo.") 
            
            user_id = message.from_user.id
            self.user_states[user_id] = 'iniciado'
        
        # para buscar una ft
        @self.bot.on_message(filters.command('buscar'))
        async def buscar_foto(client, message):
            await message.reply_text('Para buscar una foto del cielo en mi colección, por favor envíame la fecha en formato dia/mes/año (por ejemplo: 2/6/2024) :)')
            
            user_id = message.from_user.id
            self.user_states[user_id] = 'esperando fecha'
        
        # obtiene el dia/mes/año del mensaje del usuario
        @self.bot.on_message(filters.text & self.esperando_fecha())
        async def mandar_foto(client, message):
            user_id = message.from_user.id
            
            text = message.text.strip()
            texto = text.split()
            fecha = str(texto[0])
            
            if self.user_states.get(user_id) != 'esperando fecha':
                await message.reply_text('Para buscar una foto, recordá usar primero el comando /buscar :)')
                return
            
            mael = MaelDB()
            # se busca la foto
            foto = mael.foto(fecha) 
            
            if foto is None:
                await message.reply_text(f'No encontré ninguna foto guardada para el {fecha} :/\nProbá enviándome otra fecha en formato dia/mes/año.')
            
            else:
                await client.send_photo(
                    chat_id = message.from_user.id,
                    photo = foto,
                    caption = f'¡Acá tenés la foto del cielo del {fecha} :D'
                )
            
            self.user_states[user_id] = 'iniciado'
            
        # comando para añadir fotos
        @self.bot.on_message(filters.command('agg'))
        async def añadir_foto(client, message):
            user_id = message.from_user.id
            self.user_states[user_id] = 'esperando foto'
            self.user_data.pop(user_id, None)
            await message.reply_text('¡Genial! Mandame la foto del cielo que querés agregar :D')
            
        # para filtrar la foto
        @self.bot.on_message(filters.photo)
        async def foto(client,message):
            user_id = message.from_user.id
            if self.user_states.get(user_id) != 'esperando foto':
                await message.reply_text('Si querés agregar una foto a la colección, primero usá el comando /agg :)')
                return
            
            file_path = await client.download_media(message, self.path)
            self.user_data[user_id] = {'foto' : file_path}
            
            self.user_states[user_id] = 'esperando datos'
            
            await message.reply_text('Qué linda foto! Ahora enviame en un solo mensaje el país y la fecha en formato dia/mes/año (ejemplo: Colombia 26/8/2024) :)')
        
        # para filtrar el pais y la fecha sacandolo del mensaje de usuario DESPUES de usar add y mandar la  ft
        @self.bot.on_message(filters.text & self.esperando_datos()) 
        async def pais_fecha(client, message):
            
            user_id = message.from_user.id
            
            text = message.text.strip()
            texto = text.split()
            pais = texto[0]
            fecha = texto[1]
            
            if text.startswith('/'):
                return
            
            if self.user_states.get(user_id) != 'esperando datos':
                await message.reply_text('Recordá que para guardar una foto primero tenés que usar /agg y enviármela :)')
                return
            self.user_data[user_id]['pais_fecha'] = text

            img = LinkImage()
            link = img.link_image()
            
            db = MaelDB()
            
            db.insertar_dato(foto=link, fecha=fecha, pais=pais, user_id=user_id)
            
            self.user_states[user_id] = 'iniciado'
            self.user_data.pop(user_id)
            
            await message.reply_text(f'¡Listo! Guardé la foto tomada en {pais} el {fecha}. Muchas gracias por compartirla con la colección :D')
        
        @self.bot.on_message(filters.command('ultima'))
        async def ultima_foto(client, message):
            db = MaelDB()
            datos = db.obtener_ultima_foto()
            if not datos:
                await message.reply_text('Todavía no hay ninguna foto en la colección :/')
                return
            
            pais, fecha, link_foto = datos
            fecha_str = fecha.strftime('%d/%m/%Y') if hasattr(fecha, 'strftime') else str(fecha)
            
            await client.send_photo(
                chat_id=message.chat.id,
                photo=link_foto,
                caption=f"Última foto agregada\nPaís: {pais}\nFecha: {fecha_str} :D"
            )

        @self.bot.on_message(filters.command('info'))
        async def help_command(client, message):
            await message.reply_text("""Acá tenés los comandos disponibles :)

/buscar - Te muestro una foto del cielo según la fecha que me indiques (dia/mes/año).
/agg - Guardamos una nueva foto del cielo en la colección.
/ultima - Te muestro la última foto que se agregó al sistema.
/misaportes - Te muestro todas las fotos que aportaste hasta ahora.

Cualquier cosa que necesites, acá estoy :D""")
        
        # un mensajito de prueba
        @self.bot.on_message(filters.text & ~filters.regex(r'^/'))
        async def saludo(client, message):
            await message.reply_text('holaa, gracias por usar mi proyecto y contribuir con tus fotos del cielo :D \n\n-Snex')
        
        # comando para ver todas fotos aportadas por el usuario que usa el comando
        @self.bot.on_message(filters.command('misaportes'))
        async def fotos_aportadas(client, message):
            user_id = message.from_user.id
            db = MaelDB()
            fotos = db.fotos_aportadas(id=user_id)
            if not fotos:
                await message.reply('Aún no tenés fotos aportadas :/\nPodés agregar una cuando quieras con el comando /agg!')
                return
            else:
                texto = f'Hasta ahora aportaste {len(fotos)} foto/s a la colección :D\n\n'
                for i, fecha in enumerate(fotos, start=1):
                    texto += f'{i}. {fecha}\n'
            await message.reply_text(texto)
            
    def run(self):
        self.bot.run()