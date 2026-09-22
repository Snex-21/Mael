from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta
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
        
    # filtros personalizados por estado
    def esperando_fecha(self):
        async def funcion(flt, _, message):
            user_id = message.from_user.id
            return self.user_states.get(user_id) == 'esperando fecha'
        return filters.create(funcion)

    def esperando_pais_texto(self):
        async def func(flt, _, message):
            user_id = message.from_user.id
            return self.user_states.get(user_id) == 'esperando_pais_texto'
        return filters.create(func)

    def esperando_fecha_texto(self):
        async def func(flt, _, message):
            user_id = message.from_user.id
            return self.user_states.get(user_id) == 'esperando_fecha_texto'
        return filters.create(func)

    # los comandos del bot
    def comandos(self):
        
        self.user_states = {}
        self.user_data = {}
        
        # ruta de la ultima imagen que pasó el usuario
        self.path = config.root_dir / 'downloads' / 'ultima_imagen.jpg'

        # Teclado de selección de país (dinámico desde la BD)
        def obtener_teclado_paises():
            db = MaelDB()
            paises_existentes = db.obtener_paises_unicos()
            
            botones = []
            # Agrupamos los países existentes de a 2 por fila
            for i in range(0, len(paises_existentes), 2):
                par = paises_existentes[i:i+2]
                fila_botones = [InlineKeyboardButton(p, callback_data=f"pais_{p}") for p in par]
                botones.append(fila_botones)
            
            # Siempre agregamos al final la opción de escribir otro país
            botones.append([InlineKeyboardButton("Otro país", callback_data="pais_OTRO")])
            return InlineKeyboardMarkup(botones)

        # Nombres de meses para el selector
        MESES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]

        # Teclado de selección de fecha (rápida o interactiva por calendario)
        def obtener_teclado_fechas():
            hoy_dt = datetime.now()
            hoy_str = hoy_dt.strftime('%d/%m/%Y')
            ayer_str = (hoy_dt - timedelta(days=1)).strftime('%d/%m/%Y')
            
            botones = [
                [InlineKeyboardButton(f"Hoy ({hoy_str})", callback_data=f"fecha_{hoy_str}")],
                [InlineKeyboardButton(f"Ayer ({ayer_str})", callback_data=f"fecha_{ayer_str}")],
                [InlineKeyboardButton("Elegir fecha con botones", callback_data="cal_año_init")],
                [InlineKeyboardButton("Escribir otra fecha", callback_data="fecha_OTRA")]
            ]
            return InlineKeyboardMarkup(botones)

        # Selector de Año interactivo
        def obtener_teclado_años():
            año_actual = datetime.now().year
            años = range(año_actual, año_actual - 6, -1)  # últimos 6 años
            botones = []
            for i in range(0, len(años), 3):
                fila = [InlineKeyboardButton(str(a), callback_data=f"cal_año_{a}") for a in años[i:i+3]]
                botones.append(fila)
            botones.append([InlineKeyboardButton("⬅ Volver a opciones", callback_data="cal_volver_inicio")])
            return InlineKeyboardMarkup(botones)

        # Selector de Mes interactivo
        def obtener_teclado_meses(año):
            botones = []
            for i in range(0, 12, 4):
                fila = [
                    InlineKeyboardButton(MESES[m], callback_data=f"cal_mes_{año}_{m+1}")
                    for m in range(i, i+4)
                ]
                botones.append(fila)
            botones.append([InlineKeyboardButton("⬅ Cambiar año", callback_data="cal_año_init")])
            return InlineKeyboardMarkup(botones)

        # Selector de Día interactivo
        def obtener_teclado_dias(año, mes):
            import calendar
            num_dias = calendar.monthrange(año, mes)[1]
            botones = []
            fila = []
            for d in range(1, num_dias + 1):
                fila.append(InlineKeyboardButton(str(d), callback_data=f"cal_dia_{año}_{mes}_{d}"))
                if len(fila) == 7:
                    botones.append(fila)
                    fila = []
            if fila:
                botones.append(fila)
            botones.append([InlineKeyboardButton("⬅ Cambiar mes", callback_data=f"cal_año_{año}")])
            return InlineKeyboardMarkup(botones)

        @self.bot.on_message(filters.command('start'))
        async def start_command(client, message):
            await message.reply_text("Hola, soy Mael :) guardo fotos del cielo y puedo mostrártelas cuando quieras.\n\nSi querés saber cómo usar mis comandos, escribí /info y te cuento todo.") 
            
            user_id = message.from_user.id
            self.user_states[user_id] = 'iniciado'
        
        # para buscar una ft
        @self.bot.on_message(filters.command('buscar'))
        async def buscar_foto(client, message):
            await message.reply_text('Para buscar una foto del cielo en mi colección, por favor envíame la fecha en formato dia/mes/año (por ejemplo: 2/6/2024) :)') #v
            
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
            foto, pais = mael.foto(fecha) 
            
            if foto is None:
                await message.reply_text(f'No encontré ninguna foto guardada para el {fecha} :/\nProbá enviándome otra fecha en formato dia/mes/año.')
            
            else:
                await client.send_photo(
                    chat_id = message.from_user.id,
                    photo = foto,
                    caption = f'Acá tenés la foto del cielo del {fecha} tomada en {pais} :D'
                )
            
            self.user_states[user_id] = 'iniciado'
            
        # comando para añadir fotos
        @self.bot.on_message(filters.command('agg'))
        async def añadir_foto(client, message):
            user_id = message.from_user.id
            self.user_states[user_id] = 'esperando foto'
            self.user_data.pop(user_id, None)
            await message.reply_text('Genial! Mandame la foto del cielo que querés agregar :D')
            
        # para filtrar la foto
        @self.bot.on_message(filters.photo)
        async def foto(client, message):
            user_id = message.from_user.id
            if self.user_states.get(user_id) != 'esperando foto':
                await message.reply_text('Si querés agregar una foto a la colección, primero usá el comando /agg :)')
                return
            
            file_path = await client.download_media(message, self.path)
            self.user_data[user_id] = {'foto': file_path}
            self.user_states[user_id] = 'esperando_seleccion_pais'
            
            await message.reply_text(
                'Qué linda foto! Seleccioná el país donde fue tomada o elegí "Otro país" para escribirlo :)',
                reply_markup=obtener_teclado_paises()
            )

        # Manejador de botones inline (Callback Query)
        @self.bot.on_callback_query()
        async def callback_handler(client, callback_query):
            user_id = callback_query.from_user.id
            data = callback_query.data

            if user_id not in self.user_data:
                await callback_query.answer("Por favor iniciá de nuevo con /agg :)", show_alert=True)
                return

            # Manejo de selección de País
            if data.startswith("pais_"):
                pais = data.replace("pais_", "")
                if pais == "OTRO":
                    self.user_states[user_id] = 'esperando_pais_texto'
                    await callback_query.message.edit_text("Por favor escribí el nombre del país donde sacaste la foto :)")
                else:
                    self.user_data[user_id]['pais'] = pais
                    self.user_states[user_id] = 'esperando_seleccion_fecha'
                    await callback_query.message.edit_text(
                        f"País seleccionado: {pais} :D\nAhora seleccioná la fecha de la foto:",
                        reply_markup=obtener_teclado_fechas()
                    )
                await callback_query.answer()

            # Manejo de fecha rápida (Hoy / Ayer) o Escribir otra
            elif data.startswith("fecha_"):
                fecha = data.replace("fecha_", "")
                if fecha == "OTRA":
                    self.user_states[user_id] = 'esperando_fecha_texto'
                    await callback_query.message.edit_text("Por favor enviame la fecha en formato dia/mes/año (ejemplo: 21/9/2026) :)") #v
                else:
                    self.user_data[user_id]['fecha'] = fecha
                    await callback_query.message.edit_text(f"Fecha seleccionada: {fecha} :) Guardando foto...")
                    await finalizar_guardado(client, callback_query.message, user_id)
                await callback_query.answer()

            # Calendario Interactivo: Paso 1 - Seleccionar Año
            elif data == "cal_año_init":
                await callback_query.message.edit_text(
                    "Seleccioná el año:",
                    reply_markup=obtener_teclado_años()
                )
                await callback_query.answer()

            # Calendario Interactivo: Volver al menú principal de fechas
            elif data == "cal_volver_inicio":
                pais = self.user_data.get(user_id, {}).get('pais', '')
                await callback_query.message.edit_text(
                    f"País seleccionado: {pais} :D\nAhora seleccioná la fecha de la foto:",
                    reply_markup=obtener_teclado_fechas()
                )
                await callback_query.answer()

            # Calendario Interactivo: Paso 2 - Seleccionar Mes
            elif data.startswith("cal_año_"):
                año = int(data.replace("cal_año_", ""))
                self.user_data[user_id]['temp_año'] = año
                await callback_query.message.edit_text(
                    f"Año: {año} :D\nSeleccioná el mes:",
                    reply_markup=obtener_teclado_meses(año)
                )
                await callback_query.answer()

            # Calendario Interactivo: Paso 3 - Seleccionar Día
            elif data.startswith("cal_mes_"):
                _, _, año_str, mes_str = data.split("_")
                año, mes = int(año_str), int(mes_str)
                self.user_data[user_id]['temp_mes'] = mes
                nombre_mes = MESES[mes - 1]
                await callback_query.message.edit_text(
                    f"Año: {año} | Mes: {nombre_mes} :D\nSeleccioná el día del mes:",
                    reply_markup=obtener_teclado_dias(año, mes)
                )
                await callback_query.answer()

            # Calendario Interactivo: Confirmación de Día seleccionado
            elif data.startswith("cal_dia_"):
                _, _, año_str, mes_str, dia_str = data.split("_")
                fecha = f"{int(dia_str)}/{int(mes_str)}/{año_str}"
                self.user_data[user_id]['fecha'] = fecha
                await callback_query.message.edit_text(f"Fecha seleccionada: {fecha} :) Guardando foto...")
                await finalizar_guardado(client, callback_query.message, user_id)
                await callback_query.answer()

        # Si el usuario eligió escribir el país manualmente
        @self.bot.on_message(filters.text & self.esperando_pais_texto())
        async def pais_texto(client, message):
            user_id = message.from_user.id
            if message.text.startswith('/'):
                return
            pais = message.text.strip().capitalize()
            self.user_data[user_id]['pais'] = pais
            self.user_states[user_id] = 'esperando_seleccion_fecha'
            await message.reply_text(
                f"País guardado: {pais} :D\nAhora seleccioná la fecha de la foto:",
                reply_markup=obtener_teclado_fechas()
            )

        # Si el usuario eligió escribir la fecha manualmente
        @self.bot.on_message(filters.text & self.esperando_fecha_texto())
        async def fecha_texto(client, message):
            user_id = message.from_user.id
            if message.text.startswith('/'):
                return
            fecha = message.text.strip()
            self.user_data[user_id]['fecha'] = fecha
            await message.reply_text(f"Fecha guardada: {fecha} :) Guardando foto...")
            await finalizar_guardado(client, message, user_id)

        # Función auxiliar para subida y guardado final en BD
        async def finalizar_guardado(client, message, user_id):
            datos = self.user_data.get(user_id, {})
            pais = datos.get('pais')
            fecha = datos.get('fecha')
            
            img = LinkImage()
            link = img.link_image()
            
            db = MaelDB()
            db.insertar_dato(foto=link, fecha=fecha, pais=pais, user_id=user_id)
            
            self.user_states[user_id] = 'iniciado'
            self.user_data.pop(user_id, None)
            
            await message.reply_text(f'Listo! Guardé la foto tomada en {pais} el {fecha}. Muchas gracias por compartirla con la colección :D')
        
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