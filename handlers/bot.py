from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta
from .img import LinkImage
from .db import MaelDB
from .claves import config
from .i18n import get_text, get_months
from .countries import get_country_name, parse_country_to_code

# el bot en cuestion
class Mael:
    def __init__(self, api_tg, api_id, api_hash, nombre='Mael'):
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

        # Teclado de selección de país (dinámico desde la BD traducido al idioma del usuario)
        def obtener_teclado_paises(lang_code):
            db = MaelDB()
            codigos_existentes = db.obtener_paises_unicos()
            
            botones = []
            # Agrupamos los países existentes de a 2 por fila
            for i in range(0, len(codigos_existentes), 2):
                par = codigos_existentes[i:i+2]
                fila_botones = [
                    InlineKeyboardButton(get_country_name(c, lang_code), callback_data=f"pais_{c}")
                    for c in par
                ]
                botones.append(fila_botones)
            
            # Siempre agregamos al final la opción de escribir otro país
            botones.append([InlineKeyboardButton(get_text(lang_code, 'btn_otro_pais'), callback_data="pais_OTRO")])
            return InlineKeyboardMarkup(botones)

        # Teclado de selección de fecha (rápida o interactiva por calendario)
        def obtener_teclado_fechas(lang_code):
            hoy_dt = datetime.now()
            hoy_str = hoy_dt.strftime('%d/%m/%Y')
            ayer_str = (hoy_dt - timedelta(days=1)).strftime('%d/%m/%Y')
            
            botones = [
                [InlineKeyboardButton(get_text(lang_code, 'btn_hoy', fecha=hoy_str), callback_data=f"fecha_{hoy_str}")],
                [InlineKeyboardButton(get_text(lang_code, 'btn_ayer', fecha=ayer_str), callback_data=f"fecha_{ayer_str}")],
                [InlineKeyboardButton(get_text(lang_code, 'btn_elegir_calendario'), callback_data="cal_año_init")],
                [InlineKeyboardButton(get_text(lang_code, 'btn_escribir_otra_fecha'), callback_data="fecha_OTRA")]
            ]
            return InlineKeyboardMarkup(botones)

        # Selector de Año interactivo
        def obtener_teclado_años(lang_code):
            año_actual = datetime.now().year
            años = range(año_actual, año_actual - 6, -1)  # últimos 6 años
            botones = []
            for i in range(0, len(años), 3):
                fila = [InlineKeyboardButton(str(a), callback_data=f"cal_año_{a}") for a in años[i:i+3]]
                botones.append(fila)
            botones.append([InlineKeyboardButton(get_text(lang_code, 'btn_volver_opciones'), callback_data="cal_volver_inicio")])
            return InlineKeyboardMarkup(botones)

        # Selector de Mes interactivo
        def obtener_teclado_meses(año, lang_code):
            meses_nombres = get_months(lang_code)
            botones = []
            for i in range(0, 12, 4):
                fila = [
                    InlineKeyboardButton(meses_nombres[m], callback_data=f"cal_mes_{año}_{m+1}")
                    for m in range(i, i+4)
                ]
                botones.append(fila)
            botones.append([InlineKeyboardButton(get_text(lang_code, 'btn_cambiar_ano'), callback_data="cal_año_init")])
            return InlineKeyboardMarkup(botones)

        # Selector de Día interactivo
        def obtener_teclado_dias(año, mes, lang_code):
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
            botones.append([InlineKeyboardButton(get_text(lang_code, 'btn_cambiar_mes'), callback_data=f"cal_año_{año}")])
            return InlineKeyboardMarkup(botones)

        @self.bot.on_message(filters.command('start'))
        async def start_command(client, message):
            lang = message.from_user.language_code
            await message.reply_text(get_text(lang, 'start'))
            
            user_id = message.from_user.id
            self.user_states[user_id] = 'iniciado'
        
        # para buscar una ft
        @self.bot.on_message(filters.command('buscar'))
        async def buscar_foto(client, message):
            lang = message.from_user.language_code
            await message.reply_text(get_text(lang, 'buscar_prompt'))
            
            user_id = message.from_user.id
            self.user_states[user_id] = 'esperando fecha'
        
        # obtiene el dia/mes/año del mensaje del usuario
        @self.bot.on_message(filters.text & self.esperando_fecha())
        async def mandar_foto(client, message):
            user_id = message.from_user.id
            lang = message.from_user.language_code
            
            text = message.text.strip()
            texto = text.split()
            fecha = str(texto[0])
            
            if self.user_states.get(user_id) != 'esperando fecha':
                await message.reply_text(get_text(lang, 'buscar_error_estado'))
                return
            
            mael = MaelDB()
            # se busca la foto
            foto, pais_codigo = mael.foto(fecha) 
            
            if foto is None:
                await message.reply_text(get_text(lang, 'buscar_no_encontrada', fecha=fecha))
            else:
                pais_nombre = get_country_name(pais_codigo, lang)
                caption = get_text(lang, 'buscar_exito_caption', fecha=fecha)
                if pais_nombre:
                    caption += f" ({pais_nombre})"
                
                await client.send_photo(
                    chat_id = message.from_user.id,
                    photo = foto,
                    caption = caption
                )
            
            self.user_states[user_id] = 'iniciado'
            
        # comando para añadir fotos
        @self.bot.on_message(filters.command('agg'))
        async def añadir_foto(client, message):
            user_id = message.from_user.id
            lang = message.from_user.language_code
            self.user_states[user_id] = 'esperando foto'
            self.user_data[user_id] = {'lang': lang}
            await message.reply_text(get_text(lang, 'agg_inicio'))
            
        # para filtrar la foto
        @self.bot.on_message(filters.photo)
        async def foto(client, message):
            user_id = message.from_user.id
            lang = message.from_user.language_code
            if self.user_states.get(user_id) != 'esperando foto':
                await message.reply_text(get_text(lang, 'agg_error_estado_foto'))
                return
            
            file_path = await client.download_media(message, self.path)
            self.user_data[user_id] = {'foto': file_path, 'lang': lang}
            self.user_states[user_id] = 'esperando_seleccion_pais'
            
            await message.reply_text(
                get_text(lang, 'agg_foto_recibida'),
                reply_markup=obtener_teclado_paises(lang)
            )

        # Manejador de botones inline (Callback Query)
        @self.bot.on_callback_query()
        async def callback_handler(client, callback_query):
            user_id = callback_query.from_user.id
            lang = callback_query.from_user.language_code
            data = callback_query.data

            if user_id not in self.user_data:
                await callback_query.answer(get_text(lang, 'agg_sesion_expirada'), show_alert=True)
                return

            self.user_data[user_id]['lang'] = lang

            # Manejo de selección de País
            if data.startswith("pais_"):
                codigo_pais = data.replace("pais_", "")
                if codigo_pais == "OTRO":
                    self.user_states[user_id] = 'esperando_pais_texto'
                    await callback_query.message.edit_text(get_text(lang, 'agg_pedir_pais_texto'))
                else:
                    self.user_data[user_id]['pais'] = codigo_pais
                    self.user_states[user_id] = 'esperando_seleccion_fecha'
                    pais_nombre = get_country_name(codigo_pais, lang)
                    await callback_query.message.edit_text(
                        get_text(lang, 'agg_pais_seleccionado', pais=pais_nombre),
                        reply_markup=obtener_teclado_fechas(lang)
                    )
                await callback_query.answer()

            # Manejo de fecha rápida (Hoy / Ayer) o Escribir otra
            elif data.startswith("fecha_"):
                fecha = data.replace("fecha_", "")
                if fecha == "OTRA":
                    self.user_states[user_id] = 'esperando_fecha_texto'
                    await callback_query.message.edit_text(get_text(lang, 'agg_pedir_fecha_texto'))
                else:
                    self.user_data[user_id]['fecha'] = fecha
                    await callback_query.message.edit_text(get_text(lang, 'agg_guardando', fecha=fecha))
                    await finalizar_guardado(client, callback_query.message, user_id, lang)
                await callback_query.answer()

            # Calendario Interactivo: Paso 1 - Seleccionar Año
            elif data == "cal_año_init":
                await callback_query.message.edit_text(
                    get_text(lang, 'cal_seleccionar_ano'),
                    reply_markup=obtener_teclado_años(lang)
                )
                await callback_query.answer()

            # Calendario Interactivo: Volver al menú principal de fechas
            elif data == "cal_volver_inicio":
                codigo_pais = self.user_data.get(user_id, {}).get('pais', '')
                pais_nombre = get_country_name(codigo_pais, lang)
                await callback_query.message.edit_text(
                    get_text(lang, 'agg_pais_seleccionado', pais=pais_nombre),
                    reply_markup=obtener_teclado_fechas(lang)
                )
                await callback_query.answer()

            # Calendario Interactivo: Paso 2 - Seleccionar Mes
            elif data.startswith("cal_año_"):
                año = int(data.replace("cal_año_", ""))
                self.user_data[user_id]['temp_año'] = año
                await callback_query.message.edit_text(
                    get_text(lang, 'cal_seleccionar_mes', ano=año),
                    reply_markup=obtener_teclado_meses(año, lang)
                )
                await callback_query.answer()

            # Calendario Interactivo: Paso 3 - Seleccionar Día
            elif data.startswith("cal_mes_"):
                _, _, año_str, mes_str = data.split("_")
                año, mes = int(año_str), int(mes_str)
                self.user_data[user_id]['temp_mes'] = mes
                nombre_mes = get_months(lang)[mes - 1]
                await callback_query.message.edit_text(
                    get_text(lang, 'cal_seleccionar_dia', ano=año, mes=nombre_mes),
                    reply_markup=obtener_teclado_dias(año, mes, lang)
                )
                await callback_query.answer()

            # Calendario Interactivo: Confirmación de Día seleccionado
            elif data.startswith("cal_dia_"):
                _, _, año_str, mes_str, dia_str = data.split("_")
                fecha = f"{int(dia_str)}/{int(mes_str)}/{año_str}"
                self.user_data[user_id]['fecha'] = fecha
                await callback_query.message.edit_text(get_text(lang, 'agg_guardando', fecha=fecha))
                await finalizar_guardado(client, callback_query.message, user_id, lang)
                await callback_query.answer()

        # Si el usuario eligió escribir el país manualmente
        @self.bot.on_message(filters.text & self.esperando_pais_texto())
        async def pais_texto(client, message):
            user_id = message.from_user.id
            lang = message.from_user.language_code
            if message.text.startswith('/'):
                return
            pais_input = message.text.strip()
            codigo_iso = parse_country_to_code(pais_input)
            
            self.user_data[user_id]['pais'] = codigo_iso
            self.user_states[user_id] = 'esperando_seleccion_fecha'
            
            pais_nombre = get_country_name(codigo_iso, lang)
            await message.reply_text(
                get_text(lang, 'agg_pais_seleccionado', pais=pais_nombre),
                reply_markup=obtener_teclado_fechas(lang)
            )

        # Si el usuario eligió escribir la fecha manualmente
        @self.bot.on_message(filters.text & self.esperando_fecha_texto())
        async def fecha_texto(client, message):
            user_id = message.from_user.id
            lang = message.from_user.language_code
            if message.text.startswith('/'):
                return
            fecha = message.text.strip()
            self.user_data[user_id]['fecha'] = fecha
            await message.reply_text(get_text(lang, 'agg_guardando', fecha=fecha))
            await finalizar_guardado(client, message, user_id, lang)

        # Función auxiliar para subida y guardado final en BD
        async def finalizar_guardado(client, message, user_id, lang_code=None):
            datos = self.user_data.get(user_id, {})
            codigo_pais = datos.get('pais')
            fecha = datos.get('fecha')
            lang = lang_code or datos.get('lang')
            
            img = LinkImage()
            link = img.link_image()
            
            db = MaelDB()
            db.insertar_dato(foto=link, fecha=fecha, pais=codigo_pais, user_id=user_id)
            
            self.user_states[user_id] = 'iniciado'
            self.user_data.pop(user_id, None)
            
            pais_nombre = get_country_name(codigo_pais, lang)
            await message.reply_text(get_text(lang, 'agg_exito', pais=pais_nombre, fecha=fecha))
        
        @self.bot.on_message(filters.command('ultima'))
        async def ultima_foto(client, message):
            lang = message.from_user.language_code
            db = MaelDB()
            datos = db.obtener_ultima_foto()
            if not datos:
                await message.reply_text(get_text(lang, 'ultima_vacia'))
                return
            
            pais_codigo, fecha, link_foto = datos
            fecha_str = fecha.strftime('%d/%m/%Y') if hasattr(fecha, 'strftime') else str(fecha)
            pais_nombre = get_country_name(pais_codigo, lang)
            
            await client.send_photo(
                chat_id=message.chat.id,
                photo=link_foto,
                caption=get_text(lang, 'ultima_caption', pais=pais_nombre, fecha=fecha_str)
            )

        @self.bot.on_message(filters.command('info'))
        async def help_command(client, message):
            lang = message.from_user.language_code
            await message.reply_text(get_text(lang, 'info'))
        
        # un mensajito de prueba
        @self.bot.on_message(filters.text & ~filters.regex(r'^/'))
        async def saludo(client, message):
            lang = message.from_user.language_code
            await message.reply_text(get_text(lang, 'saludo'))
        
        # comando para ver todas fotos aportadas por el usuario que usa el comando
        @self.bot.on_message(filters.command('misaportes'))
        async def fotos_aportadas(client, message):
            user_id = message.from_user.id
            lang = message.from_user.language_code
            db = MaelDB()
            fotos = db.fotos_aportadas(id=user_id)
            if not fotos:
                await message.reply(get_text(lang, 'misaportes_vacio'))
                return
            else:
                texto = get_text(lang, 'misaportes_header', cantidad=len(fotos))
                for i, fecha in enumerate(fotos, start=1):
                    texto += f'{i}. {fecha}\n'
            await message.reply_text(texto)
            
    def run(self):
        self.bot.run()