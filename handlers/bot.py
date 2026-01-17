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
            # UNA MEJOR PRESENTACION
            await message.reply_text("""Hola, Soy Mael.
            \n\nGuardo imagenes del cielo y puedo mostrartelas cuando lo necesites.\n\nCuando quieras empezamos.
            \n\nSi quieres saber como funciona mis comandos, escribí /info y te lo cuento""") 
            
            user_id = message.from_user.id
            self.user_states[user_id] = 'iniciado'
        
        # para buscar una ft
        @self.bot.on_message(filters.command('buscar'))
        async def buscar_foto(client, message):
            # MEJORES INSTRUCCIONES
            await message.reply_text('Para mostrarte una foto del cielo, necesito que me pases la fecha.\n\nEs importante que uses el formato *dia/mes/año*, con la barra exacta.')
            
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
                # PROBAR CON MANDAR EL DIA MES AÑO SIN EL COMANDO BUSCAR
                # MEJORAR LAS INSTRUCCIONES
                await message.reply_text('tienes que usar el comando buscar y seguir los pasos')
                return
            
            mael = MaelDB()
            # se busca la foto
            foto = mael.foto(fecha) 
            
            if foto is None:
                # HACER UNA MEJOR RESPUESTA
                await message.reply_text(f'Parece que no tengo ninguna foto del cielo con la fecha {fecha}.\nMandame otra fecha en dia/mes/año y lo intento de nuevo.')
            
            else:
                # ETAPA FINAL
                await client.send_photo(
                    chat_id = message.from_user.id,
                    photo = foto,
                    # MEJORAR EL CAPTION (QUIZAS CON LA FECHA Y EL NUMERO DE FOTO, ID O NUM DE FOTOS CON ESA FECHA)
                    caption = 'Listo, encontré la foto del cielo. Mirala y decime si quieres buscar otra.'
                )
            
            self.user_states[user_id] = 'iniciado'
            
        # comando para añadir fotos
        @self.bot.on_message(filters.command('agg'))
        async def añadir_foto(client, message):
            user_id = message.from_user.id
            self.user_states[user_id] = 'esperando foto'
            self.user_data.pop(user_id, None)
            # MEJORES INSTRUCCIONES
            await message.reply_text('Listo para guardar una foto del cielo. Mandamela y la agrego a la coleción.')
            # await message.reply_text('manda la foto')
            
        # para filtrar la foto
        @self.bot.on_message(filters.photo)
        async def foto(client,message):
            user_id = message.from_user.id
            if self.user_states.get(user_id) != 'esperando foto':
                # MEJORAR LAS INSTRUCCIONES
                await message.reply_text('Si quieres agregar una foto primero tines que usar /add y seguir los pasos')
                return
            
            file_path = await client.download_media(message, self.path)
            self.user_data[user_id] = {'foto' : file_path}
            
            self.user_states[user_id] = 'esperando datos'
            
            # MEJORAR ESTE MENSAJE
            await message.reply_text('Listo, ahora pasame en un solo mensaje el país donde se sacó la foto y después la fecha en formato día/mes/año, con la barra exacta.')
        
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
                # MEJORAR LAS INSTRUCCIONES
                # PROBAR CUANDO SALE ESTE MENSAJE PORQUE ME PARECE QUE YA NO SE NECESITA
                await message.reply_text('tienes que usar el comando add y seguir los pasos')
                return
            self.user_data[user_id]['pais_fecha'] = text

            img = LinkImage()
            link = img.link_image()
            
            db = MaelDB()
            
            db.insertar_dato(foto=link, fecha=fecha, pais=pais, user_id=user_id)
            
            self.user_states[user_id] = 'iniciado'
            self.user_data.pop(user_id)
            
            # MEJORAR ESTE MENSAJE
            # AGREGAR ESOS DATOS ADICIONALES 
            # await message.reply_text(f'Listo, ya guarde tu foto. Gracias por tu contribución. \n\n foto numero: \nfecha: {fecha}\npais: {pais}')
            await message.reply_text(f'Ya está, guardé la foto tomada en {pais} el {fecha}. Gracias por compartirla conmigo.')
        
        @self.bot.on_message(filters.command('info'))
        async def help_command(client, message):
            await message.reply_text("""Acá están los comandos que podés usar:
            \n\n/buscar – escribí primero este comando, y después pasame la fecha en formato día/mes/año para que te muestre la foto del cielo.
            \n\n/agg – escribí primero este comando. Luego mandame la foto, y después el país y la fecha en un solo mensaje (día/mes/año) para guardarla.
            \n\n/misaportes – para ver los aportes que hiciste
            \n\nUsalos como quieras, y yo estoy acá para acompañarte.""")
        
        # un mensajito de prueba
        # MEJORAR ESTO, PUEDE SERVIR COMO UN MINI EASTEREGG  
        @self.bot.on_message(filters.text & ~filters.regex(r'^/'))
        async def saludo(client, message):
            text = message.text.strip()
            
            await message.reply_text('holaa, gracias por usar mi proyecto y contribuir con tus fotos del cielo :D \n\n-Snex')
        
        # comando para ver todas fotos aportadas por el usuario que usa el comando
        @self.bot.on_message(filters.command('misaportes'))
        async def fotos_aportadas(client, message):
            # id del usuario
            user_id = message.from_user.id
            
            db = MaelDB()
            
            # fechas de las fotos que aportó el usuario
            fotos = db.fotos_aportadas(id=user_id)
            if not fotos:
                # si no hay fotos...
                await message.reply('no tenes fotos aportadas')
                return
            else:
                # si hay fotos (o sea, fehcas) le digo la cantidad y las fechas
                texto = f'has aportado {len(fotos)} foto/s:\n\n'
                for i, fecha in enumerate(fotos, start=1):
                    texto += f'{i}. {fecha}\n'
            await message.reply_text(texto)
            
    def run(self):
        self.bot.run()