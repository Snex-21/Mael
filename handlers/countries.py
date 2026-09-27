import unicodedata

# Mapeo ISO 3166-1 alpha-2 para los principales países del mundo
# (América, Europa, Asia, África, Oceanía)
COUNTRIES = {
    # América del Sur
    "AR": {"es": "Argentina", "en": "Argentina"},
    "BO": {"es": "Bolivia", "en": "Bolivia"},
    "BR": {"es": "Brasil", "en": "Brazil"},
    "CL": {"es": "Chile", "en": "Chile"},
    "CO": {"es": "Colombia", "en": "Colombia"},
    "EC": {"es": "Ecuador", "en": "Ecuador"},
    "GY": {"es": "Guyana", "en": "Guyana"},
    "PY": {"es": "Paraguay", "en": "Paraguay"},
    "PE": {"es": "Perú", "en": "Peru"},
    "SR": {"es": "Surinam", "en": "Suriname"},
    "UY": {"es": "Uruguay", "en": "Uruguay"},
    "VE": {"es": "Venezuela", "en": "Venezuela"},

    # América del Norte y Central / Caribe
    "US": {"es": "Estados Unidos", "en": "United States"},
    "CA": {"es": "Canadá", "en": "Canada"},
    "MX": {"es": "México", "en": "Mexico"},
    "CR": {"es": "Costa Rica", "en": "Costa Rica"},
    "CU": {"es": "Cuba", "en": "Cuba"},
    "DO": {"es": "República Dominicana", "en": "Dominican Republic"},
    "SV": {"es": "El Salvador", "en": "El Salvador"},
    "GT": {"es": "Guatemala", "en": "Guatemala"},
    "HN": {"es": "Honduras", "en": "Honduras"},
    "NI": {"es": "Nicaragua", "en": "Nicaragua"},
    "PA": {"es": "Panamá", "en": "Panama"},
    "PR": {"es": "Puerto Rico", "en": "Puerto Rico"},
    "JM": {"es": "Jamaica", "en": "Jamaica"},

    # Europa
    "ES": {"es": "España", "en": "Spain"},
    "FR": {"es": "Francia", "en": "France"},
    "IT": {"es": "Italia", "en": "Italy"},
    "DE": {"es": "Alemania", "en": "Germany"},
    "GB": {"es": "Reino Unido", "en": "United Kingdom"},
    "PT": {"es": "Portugal", "en": "Portugal"},
    "NL": {"es": "Países Bajos", "en": "Netherlands"},
    "BE": {"es": "Bélgica", "en": "Belgium"},
    "CH": {"es": "Suiza", "en": "Switzerland"},
    "AT": {"es": "Austria", "en": "Austria"},
    "SE": {"es": "Suecia", "en": "Sweden"},
    "NO": {"es": "Noruega", "en": "Norway"},
    "DK": {"es": "Dinamarca", "en": "Denmark"},
    "FI": {"es": "Finlandia", "en": "Finland"},
    "IE": {"es": "Irlanda", "en": "Ireland"},
    "PL": {"es": "Polonia", "en": "Poland"},
    "GR": {"es": "Grecia", "en": "Greece"},
    "CZ": {"es": "República Checa", "en": "Czech Republic"},
    "RO": {"es": "Rumania", "en": "Romania"},
    "UA": {"es": "Ucrania", "en": "Ukraine"},
    "RU": {"es": "Rusia", "en": "Russia"},
    "TR": {"es": "Turquía", "en": "Turkey"},

    # Asia y Medio Oriente
    "JP": {"es": "Japón", "en": "Japan"},
    "CN": {"es": "China", "en": "China"},
    "KR": {"es": "Corea del Sur", "en": "South Korea"},
    "IN": {"es": "India", "en": "India"},
    "ID": {"es": "Indonesia", "en": "Indonesia"},
    "PH": {"es": "Filipinas", "en": "Philippines"},
    "VN": {"es": "Vietnam", "en": "Vietnam"},
    "TH": {"es": "Tailandia", "en": "Thailand"},
    "MY": {"es": "Malasia", "en": "Malaysia"},
    "SG": {"es": "Singapur", "en": "Singapore"},
    "IL": {"es": "Israel", "en": "Israel"},
    "SA": {"es": "Arabia Saudita", "en": "Saudi Arabia"},
    "AE": {"es": "Emiratos Árabes Unidos", "en": "United Arab Emirates"},

    # África y Oceanía
    "EG": {"es": "Egipto", "en": "Egypt"},
    "ZA": {"es": "Sudáfrica", "en": "South Africa"},
    "MA": {"es": "Marruecos", "en": "Morocco"},
    "NG": {"es": "Nigeria", "en": "Nigeria"},
    "KE": {"es": "Kenia", "en": "Kenya"},
    "AU": {"es": "Australia", "en": "Australia"},
    "NZ": {"es": "Nueva Zelanda", "en": "New Zealand"},
}

def normalizar_texto(texto: str) -> str:
    """Elimina acentos y pasa a minúsculas para comparaciones flexibles."""
    if not texto:
        return ""
    texto_limpio = unicodedata.normalize('NFD', texto.strip().lower())
    return ''.join(c for c in texto_limpio if unicodedata.category(c) != 'Mn')

# Generamos un mapa de búsqueda inverso para normalización rápida
_LOOKUP_MAP = {}
for code, names in COUNTRIES.items():
    _LOOKUP_MAP[code.lower()] = code
    _LOOKUP_MAP[normalizar_texto(names["es"])] = code
    _LOOKUP_MAP[normalizar_texto(names["en"])] = code

# Sinónimos y nombres comunes alternativos
_SINONIMOS = {
    "usa": "US",
    "eeuu": "US",
    "ee.uu": "US",
    "united states of america": "US",
    "uk": "GB",
    "england": "GB",
    "inglaterra": "GB",
    "gran bretana": "GB",
    "great britain": "GB",
    "holanda": "NL",
    "holland": "NL",
    "south korea": "KR",
    "corea": "KR",
}
for sinonimo, code in _SINONIMOS.items():
    _LOOKUP_MAP[normalizar_texto(sinonimo)] = code

def parse_country_to_code(user_input: str) -> str:
    """
    Convierte el texto ingresado por el usuario (o código ISO) al código ISO 3166-1 alpha-2.
    Si no se encuentra en el diccionario, guarda el texto original capitalizado.
    """
    if not user_input:
        return ""
    
    limpio = normalizar_texto(user_input)
    if limpio in _LOOKUP_MAP:
        return _LOOKUP_MAP[limpio]
    
    # Si ingresó ya un código de 2 letras en mayúsculas
    if len(user_input.strip()) == 2:
        return user_input.strip().upper()
    
    # Si es un país exótico fuera del catálogo
    return user_input.strip().capitalize()

def get_country_name(country_code: str, lang_code: str | None = 'es') -> str:
    """
    Traduce un código ISO de 2 letras al nombre del país en el idioma indicado.
    Si no es un código ISO reconocido, devuelve el texto tal cual.
    """
    if not country_code:
        return ""
    
    lang = 'es' if lang_code and lang_code.lower().startswith('es') else 'en'
    code_upper = country_code.strip().upper()
    
    if code_upper in COUNTRIES:
        return COUNTRIES[code_upper].get(lang, COUNTRIES[code_upper]['es'])
    
    return country_code.strip().capitalize()
