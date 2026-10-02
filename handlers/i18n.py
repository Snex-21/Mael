# Módulo de internacionalización (i18n) para Mael

TEXTS = {
    'es': {
        # Comandos generales
        'start': "Hola, soy Mael :) guardo fotos del cielo y puedo mostrártelas cuando quieras.\n\nSi querés saber cómo usar mis comandos, escribí /info y te cuento todo.",
        'info': """Acá tenés los comandos disponibles :)

/buscar - Te muestro una foto del cielo según la fecha que me indiques (dia/mes/año).
/agg - Guardamos una nueva foto del cielo en la colección.
/ultima - Te muestro la última foto que se agregó al sistema.
/misaportes - Te muestro todas las fotos que aportaste hasta ahora.

Cualquier cosa que necesites, acá estoy :D""",
        'saludo': "Holaa :) muchas gracias por estar acá y compartir fotos del cielo! :D",
        
        # Flujo /buscar
        'buscar_prompt': "Para buscar una foto del cielo en mi colección, por favor envíame la fecha en formato dia/mes/año (por ejemplo: 2/6/2024) :)", #v
        'buscar_error_estado': "Para buscar una foto, recordá usar primero el comando /buscar :)",
        'buscar_no_encontrada': "No encontré ninguna foto guardada para el {fecha} :/\nProbá enviándome otra fecha en formato dia/mes/año.",
        'buscar_exito_caption': "Acá tenés la foto del cielo del {fecha} :D",
        
        # Flujo /agg
        'agg_inicio': "Genial! Mandame la foto del cielo que querés agregar :D",
        'agg_error_estado_foto': "Si querés agregar una foto a la colección, primero usá el comando /agg :)",
        'agg_foto_recibida': "Qué linda foto! Seleccioná el país donde fue tomada o elegí \"Otro país\" para escribirlo :)",
        'agg_sesion_expirada': "Por favor iniciá de nuevo con /agg :)",
        'agg_pedir_pais_texto': "Por favor escribí el nombre del país donde sacaste la foto :)",
        'agg_pais_seleccionado': "País seleccionado: {pais} :D\nAhora seleccioná la fecha de la foto:",
        'agg_pedir_fecha_texto': "Por favor enviame la fecha en formato dia/mes/año (ejemplo: 26/8/2026) :)", #v
        'agg_guardando': "Fecha seleccionada: {fecha} :) Guardando foto...",
        'agg_error_estado_datos': "Recordá que para guardar una foto primero tenés que usar /agg y enviármela :)",
        'agg_exito': "¡Listo! Guardé la foto tomada en {pais} el {fecha}. Muchas gracias por compartirla con la colección :D",
        
        # Flujo /ultima
        'ultima_vacia': "Todavía no hay ninguna foto en la colección :/",
        'ultima_caption': "Última foto agregada\nPaís: {pais}\nFecha: {fecha} :D",
        
        # Flujo /misaportes
        'misaportes_vacio': "Aún no tenés fotos aportadas :/\nPodés agregar una cuando quieras con el comando /agg!",
        'misaportes_caption': "Aporte {actual} de {total} (ID: #{foto_id})\nPaís: {pais}\nFecha: {fecha} :D",
        'misaportes_confirmar_borrar': "¿Seguro que querés borrar la foto #{foto_id} tomada en {pais} el {fecha}? :/\nSe eliminará de la colección.",
        'misaportes_borrado_exito': "La foto #{foto_id} fue eliminada con éxito :/",
        
        # Botones y Calendario
        'btn_anterior': "← Anterior",
        'btn_siguiente': "→ Siguiente",
        'btn_eliminar_aporte': "Eliminar foto",
        'btn_confirmar_si': "Sí, eliminar",
        'btn_confirmar_no': "Cancelar",
        'btn_otro_pais': "Otro país",
        'btn_hoy': "Hoy ({fecha})",
        'btn_ayer': "Ayer ({fecha})",
        'btn_hace_2_dias': "Hace 2 días ({fecha})",
        'btn_elegir_calendario': "Elegir fecha con botones",
        'btn_escribir_otra_fecha': "Escribir otra fecha",
        'btn_volver_opciones': "← Volver a opciones",
        'btn_cambiar_ano': "← Cambiar año",
        'btn_cambiar_mes': "← Cambiar mes",
        'cal_seleccionar_ano': "Seleccioná el año:",
        'cal_seleccionar_mes': "Año: {ano} :D\nSeleccioná el mes:",
        'cal_seleccionar_dia': "Año: {ano} | Mes: {mes} :D\nSeleccioná el día del mes:",
        
        # Nombres de los meses
        'meses': ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
    },
    'en': {
        # General commands
        'start': "Hello, I'm Mael :) I store sky photos and I can show them to you whenever you want.\n\nIf you want to learn how my commands work, type /info and I'll tell you all about it.",
        'info': """Here are the available commands :)

/buscar - I'll show you a sky photo based on the date you provide (day/month/year).
/agg - Save a new sky photo to the collection.
/ultima - See the latest photo added to the system.
/misaportes - See all the photos you have contributed so far.

Whatever you need, I'm right here :D""",
        'saludo': "Hello :) Thank you so much for being here and sharing sky photos! :D",
        
        # /buscar flow
        'buscar_prompt': "To search for a sky photo in my collection, please send me the date in day/month/year format (e.g. 2/6/2024) :)", #v
        'buscar_error_estado': "To search for a photo, remember to first use the /buscar command :)",
        'buscar_no_encontrada': "I couldn't find any photo saved for {fecha} :/\nTry sending another date in day/month/year format.",
        'buscar_exito_caption': "Here is the sky photo from {fecha} :D",
        
        # /agg flow
        'agg_inicio': "Awesome! Send me the sky photo you'd like to add :D",
        'agg_error_estado_foto': "If you want to add a photo to the collection, first use the /agg command :)",
        'agg_foto_recibida': "What a lovely photo! Select the country where it was taken or choose \"Other country\" to type it in :)",
        'agg_sesion_expirada': "Please start over by typing /agg :)",
        'agg_pedir_pais_texto': "Please type the name of the country where you took the photo :)",
        'agg_pais_seleccionado': "Selected country: {pais} :D\nNow select the date of the photo:",
        'agg_pedir_fecha_texto': "Please send me the date in day/month/year format (e.g. 26/8/2026) :)", #v
        'agg_guardando': "Selected date: {fecha} :) Saving photo...",
        'agg_error_estado_datos': "Remember that to save a photo you must first use /agg and send it to me :)",
        'agg_exito': "All set! I saved the photo taken in {pais} on {fecha}. Thank you so much for sharing it with the collection :D",
        
        # /ultima flow
        'ultima_vacia': "There are no photos in the collection yet :/",
        'ultima_caption': "Latest photo added\nCountry: {pais}\nDate: {fecha} :D",
        
        # /misaportes flow
        'misaportes_vacio': "You don't have any contributed photos yet :/\nYou can add one anytime using the /agg command!",
        'misaportes_caption': "Contribution {actual} of {total} (ID: #{foto_id})\nCountry: {pais}\nDate: {fecha} :D",
        'misaportes_confirmar_borrar': "Are you sure you want to delete photo #{foto_id} taken in {pais} on {fecha}? :/\nIt will be removed from the collection.",
        'misaportes_borrado_exito': "Photo #{foto_id} has been deleted successfully :/",
        
        # Buttons and Calendar
        'btn_anterior': "← Previous",
        'btn_siguiente': "→ Next",
        'btn_eliminar_aporte': "Delete photo",
        'btn_confirmar_si': "Yes, delete",
        'btn_confirmar_no': "Cancel",
        'btn_otro_pais': "Other country",
        'btn_hoy': "Today ({fecha})",
        'btn_ayer': "Yesterday ({fecha})",
        'btn_hace_2_dias': "2 days ago ({fecha})",
        'btn_elegir_calendario': "Pick date with buttons",
        'btn_escribir_otra_fecha': "Type another date",
        'btn_volver_opciones': "← Back to options",
        'btn_cambiar_ano': "← Change year",
        'btn_cambiar_mes': "← Change month",
        'cal_seleccionar_ano': "Select the year:",
        'cal_seleccionar_mes': "Year: {ano} :D\nSelect the month:",
        'cal_seleccionar_dia': "Year: {ano} | Month: {mes} :D\nSelect the day of the month:",
        
        # Month names
        'meses': ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    }
}

def resolve_lang(lang_code: str | None) -> str:
    """Devuelve 'es' si el idioma empieza con 'es', de lo contrario devuelve 'en'."""
    if lang_code and lang_code.lower().startswith('es'):
        return 'es'
    return 'en'

def get_text(lang_code: str | None, key: str, **kwargs) -> str:
    """Obtiene el texto traducido según el código de idioma del usuario."""
    lang = resolve_lang(lang_code)
    text = TEXTS.get(lang, {}).get(key, TEXTS['es'].get(key, ''))
    if isinstance(text, str) and kwargs:
        return text.format(**kwargs)
    return text

def get_months(lang_code: str | None) -> list[str]:
    """Devuelve la lista de meses según el idioma."""
    lang = resolve_lang(lang_code)
    return TEXTS[lang]['meses']
