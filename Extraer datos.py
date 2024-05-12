from tkinter import ttk
import tkinter as tk
import json
import os

#Ruta directorio actual
directorio_actual = os.path.dirname(os.path.abspath(__file__))

# Ruta del archivo de texto
archivo_datos_liberty = os.path.join(directorio_actual, "..", "Datos", "datos_liberty.txt")
archivo_datos_rentanacional = os.path.join(directorio_actual, "..", "Datos", "datos_rentanacional.txt")
archivo_datos_reale = os.path.join(directorio_actual, "..", "Datos", "datos_reale.txt")
archivo_datos_ans   = os.path.join(directorio_actual, "..", "Datos", "datos_ans.txt")


# Función para obtener y guardar los datos
def obtener_datos():
    # Obtener la marca y modelo seleccionados
    marca_seleccionada = marca_var.get().strip()
    modelo_seleccionado = modelo_var.get().strip()
    tipo_vehiculo_seleccionado = tipo_vehiculo_var.get().strip()
    tipo_persona_seleccionado = tipo_persona_var.get().strip()
    rut_ingresado = rut_entry.get().strip()
    nombre_contratante = nombre_contratante_entry.get().strip()
    apellido_contratante = apellido_contratante_entry.get().strip()
    uso_vehiculo_seleccionado = uso_vehiculo_var.get().strip()
    patente_ingresada = patente_entry.get().strip()
    ano_ingresado = ano_var.get().strip()
    rubro_liberty = rubro_var.get().strip()
    estilo_ingresado = estilo_var.get().strip()
    comuna_ingresada = comuna_var.get().strip()

   
    # Crear un diccionario con los datos
    datos = {
        'tipo_vehiculo': tipo_vehiculo_seleccionado,
        'tipo_persona': tipo_persona_seleccionado,
        'rut': rut_ingresado,
        'nombre_contratante': nombre_contratante,
        'apellido_contratante': apellido_contratante,
        'uso_vehiculo': uso_vehiculo_seleccionado,
        'patente': patente_ingresada,
        'marca': marca_seleccionada,
        'modelo': modelo_seleccionado,
        'ano': ano_ingresado,
        'rubro' : rubro_liberty,
        'estilo_vehiculo' : estilo_ingresado,
        "comuna": comuna_ingresada
       }

    # Imprimir el diccionario de datos
    print(datos)

    #Datos Reale
 #Datos Reale
    # Datos Reale
    datos_reale = datos.copy()

    # Convierte la comuna a Unicode antes de guardarla
    datos_reale["comuna"] = comuna_var.get()
    datos_reale["marca"] = marcas_numericas.get(marca_seleccionada, {}).get("valor_reale", "")

    with open(archivo_datos_reale, 'w', encoding='utf-8') as archivo:
        json.dump(datos_reale, archivo, ensure_ascii=False)
    
    # Datos Liberty
    datos_liberty = datos.copy()
    datos_liberty["marca_liberty"] = marcas_numericas.get(marca_seleccionada, {}).get("valor_liberty", "")
    datos_liberty["rubro"] = valores_rubro.get(rubro_liberty, "")

    with open(archivo_datos_liberty, 'w') as archivo:
       json.dump(datos_liberty, archivo)
    
    # Datos Renta
    nuevo_dato = modelo_seleccionado
    datos_rentanacional = datos.copy()
    datos_rentanacional["modelo_rentanacional"] = nuevo_dato

    datos_rentanacional["marca_rentanacional"] = marcas_numericas.get(marca_seleccionada, {}).get("valor_liberty", "")

    with open(archivo_datos_rentanacional, "w") as archivo:
       json.dump(datos_rentanacional, archivo)

 #Datos ANS
    datos_ANS = datos.copy()

   # Convierte la comuna a Unicode antes de guardarla
    comuna_parte = comuna_var.get().split(" - ")[0]  # Obtener solo la primera parte de la comuna
    datos_ANS["comuna"] = comuna_parte
    datos_ANS["marca"] = marcas_numericas.get(marca_seleccionada, {}).get("valor_reale", "")

    with open(archivo_datos_ans, 'w', encoding='utf-8') as archivo:
       json.dump(datos_ANS, archivo, ensure_ascii=False)

def actualizar_modelos(*args):
    marca_seleccionada = marca_var.get()
    modelos_disponibles = marcas_numericas.get(marca_seleccionada, {}).get("modelos", [])
    modelo_combobox['values'] = modelos_disponibles



# Diccionario de marcas numericas
marcas_numericas = {
    "ABARTH": {"valor_reale":"ABARTH",
               "modelos":["695"]
               ,"valor_reale":"ABARTH"},

    "ALFA ROMEO": {
        "valor_rentanacional": 10001,
        "valor_liberty": "ALFA ROMEO",
        "valor_reale": "ABARTH",
        "modelos": ["145", "146", "147", "155", "156", "159", "164", "166", "GIULIETTA", "MITO", "STELVIO"],
    },

    "ASIA MOTORS":
       {"valor_rentanacional": "",
       "valor_liberty": "ASIA MOTORS",
       "valor_reale":"ASIA MOTORS",
       "modelos":[]},
    "AUDI":       
       {"valor_rentanacional": 10005,
       "valor_liberty": "AUDI",
       "valor_reale":"AUDI",
        "modelos": ["A1", "A3", "A4", "Q3", "Q5"]},
    "BAIC":       
       {"valor_rentanacional": 10833,
       "valor_liberty": "BAIC",
       "valor_reale":"BAIC",
       "modelos": ["BJ40P ELITE", "BJ40P LUXURY", "BJ40P PREMIUM", "PLUS", "UP", "X25", "X35", "X55"]},
    "BMW":        
       {"valor_rentanacional": 10006,
         "valor_liberty": "B.M.W.",
         "valor_reale":"BMW",
         "modelos": ["114", "116", "120", "125", "128 TI", "130", "135", "140", "235", "240",
                     "318", "320", "325", "330", "335", "420", "520", "525", "530", "540",
                     "545", "550", "745", "X1", "X2", "X3", "X4", "X5", "X6"]},
    "BRILLIANCE": 
       { "valor_rentanacional": 10720,
         "valor_liberty": "BRILLIANCE",
         "valor_reale":"BRILLIANCE",
         "modelos": ["EUPHORIA", "FRV", "FSV", "H220", "H230", "KONECT", "SPLENDOR",
                     "T30", "T32", "T50", "T52", "V3", "V5", "V5", "X30"]},
    "BYD":       
       {"valor_rentanacional": 10352,
       "valor_liberty": "BYD",
       "valor_reale":"BYD",
       "modelos": ["F0 GL 1 1.0", "F3", "G3", "S1", "S6"]},
    "CHANGAN":
       {"valor_rentanacional": 10266,
         "valor_liberty": "CHANGAN",
         "valor_reale":"CHANGAN",
         "modelos": ["A500", "ALSVIN", "BENNI", "CS 35", "CS 55", "CS1", "CS15", "CS75", 
                     "CV1", "CV2", "CX70", "EADO", "HUNTER", "M201", "MD 201", "MS 201", "S-100", "S-300", "UNI-T"]},
    "CHANGHE": 
        {"valor_rentanacional": 10749,
        "valor_liberty": "CHANGHE",
        "valor_reale":"CHANGHE",
        "modelos": ["SPLA"]},
    "CHERY": 
       {"valor_rentanacional": 10135,
        "valor_liberty": "CHERY",
        "valor_reale":"CHERY",
        "modelos": ["A 516", "ARRIZO 3", "ARRIZO 5", "ARRIZO 7", "BEAT", "DESTINY", "FACE", "FULWIN", "IQ", "K60", "S21",
                     "TIGGO", "TIGGO 2", "TIGGO 2 PRO", "TIGGO 3", "TIGGO 3 PRO", "TIGGO 4", "TIGGO 7", "TIGGO 7 PRO", "TIGGO 8", "TIGGO 8 PRO"]},
    "CHEVROLET": 
       {"valor_rentanacional": 10510,
        "valor_liberty": "CHEVROLET",
        "valor_reale": "CHEVROLET",
        "modelos": ["ASTRA", "ASTRO VAN", "AVALANCHE", "AVEO", "BLAZER", "CAPTIVA", "CAVALIER", "CHEVY URBAN", "COBALT", "COLORADO", "COMBO", "CORSA", 
                    "CRUZE", "D MAX", "EPICA", "EQUINOX", "EVOLUTION", "GRAND LUV", "GROOVE", "IMPALA", "LUMINA", "LUV", "MALIBU", "MONTANA", "N300 MAX",
                    "N400 MAX", "NEW PRISMA", "ONIX", "OPTRA", "ORLANDO", "PRISMA", "S-10", "SAIL", "SILVERADO", "SONIC", "SPARK", "SPARK GT II", "SPIN",
                    "SUBURBAN", "TAHOE", "TRACKER", "TRAILBLAZER", "TRAVERSE", "UPLANDER", "URBAN", "VECTRA", "VENTURE", "VIVANT", "ZAFIRA"]},
    "CHRYSLER": 
       {"valor_rentanacional": 10575,
        "valor_liberty": "CHRYSLER",
        "valor_reale":"CHRYSLER",
        "modelos": ["300 C", "CARAVAN", "GRAND CARAVAN", "GRAND TOWN COUNTRY", "NEON", "NEW SEBRING", "PACIFICA", "PT CRUISER", "SEBRING", "STRATUS", "TOWN COUNTRY"]},
    "CITROEN": 
       {"valor_rentanacional": 10543,
        "valor_liberty": "CITROEN",
        "valor_reale":"CITROEN",
        "modelos": ["BERLINGO", "C 1", "C 2", "C 3", "C 3 AIRCROSS", "C 4", "C 4 CACTUS", "C 5", "C 5 AIRCROSS", "C ELYSEE", "DS3", "DS4", "DS5", "JUMPER", "JUMPY", 
                    "NEMO", "SAXO", "SPACETOURER", "XANTIA", "XSARA", "ZX"]},
    "CUPRA": 
       {"valor_rentanacional": 10975,
        "valor_liberty": "CUPRA",
        "valor_reale":"CUPRA",
        "modelos": ["FORMENTOR"]},
    "DFLM":
    {"valor_reale": "DFLM",
     "modelos": ["JOYEAR", "T5 EVO", "T5L"]},
      "DAIHATSU":
         {"valor_rentanacional": 10236,
         "valor_liberty": "DAIHATSU",
         "valor_reale": "DAIHATSU",
         "modelos": ["APPLAUSE", "CUORE", "MIRA", "NEW TERIOS", "ROCKY", "SIRION", "TERIOS"]},
    "DFM": 
         {"valor_rentanacional": 10621,
         "valor_liberty": "DFM",
         "valor_reale": "DFM",
         "modelos": ["A30", "AX3", "AX4", "AX5", "DF 6", "JOYEAR CROSS", "K 14", "S50", "SX5", "SX6"]},
    "DFSK":
         {"valor_rentanacional": 10464,
         "valor_liberty": "DFSK",
         "valor_reale": "DFSK",
         "modelos": ["500", "560", "580", "CARGO BOX", "CARGO VAN", "D1", "REFRI TRUCK", "TRUCK"]},
      "DODGE": 
         {"valor_rentanacional": 10652,
         "valor_liberty": "DODGE",
         "valor_reale": "DODGE",
         "modelos": ["CALIBER", "CARAVAN", "DAKOTA", "DURANGO", "GRAND CARAVAN", "JOURNEY", "NITRO", "RAM", "RAM 2500"]},
      "DONGFENG": 
         {"valor_rentanacional": 10387,
         "valor_liberty": "DONGFENG",
         "valor_reale": "DONGFENG",
         "modelos": ["560", "A30", "AEOLUS", "AX3", "AX4", "AX5", "AX7", "CARGO BOX", "CARGO VAN", "DF 212",
                     "DF 6", "H30 CROSS", "JOYEAR", "MINISTAR", "MINITRUCK", "REFRITRUCK", "RICH", "S30",
                     "S50", "S500", "SUCCE", "SX5", "SX6", "T5 EVO", "T5 L", "YIXUAN", "YUMSUN"]},
      "DS": 
         {"valor_rentanacional": 10900,
         "valor_liberty": "DS",
         "valor_reale": "DS",
         "modelos": ["3", "4", "5", "7"]},
      "FAW": 
         {"valor_rentanacional": 10429,
         "valor_liberty": "FAW",
         "valor_reale": "FAW",
         "modelos": ["BESTURN B50", "BESTURN X80", "D 60", "MAMUT V80", "OLEY", "R7", "T80", "V2", "V5", "X7"]},
      "FIAT": 
         { "valor_rentanacional": 10200,
         "valor_liberty": "FIAT",
         "valor_reale": "FIAT",
         "modelos": ["500", "ARGO", "BRAVA", "BRAVO", "CRONOS", "DOBLO", "DUCATO", "FIORINO",
                     "FULLBACK", "GRANDE PUNTO", "IDEA", "LINEA", "MAREA", "MOBI", "PALIO",
                     "PANDA", "PULSE", "PUNTO", "QUBO", "SIENA", "STILO", "STRADA", "TIPO",
                     "UNO", "UNO WAY 1.4"]},
      "FORD": 
         {"valor_rentanacional": 10511,
         "valor_liberty": "FORD",
         "valor_reale": "FORD",
         "modelos": ["BRONCO", "ECOSPORT", "EDGE", "ESCAPE", "ESCORT", "EURO ESCORT",
                     "EXPEDITION", "EXPLORER", "F-150", "FIESTA", "FOCUS", "FUSION",
                     "KA", "KING RANCH", "MAVERICK", "MONDEO", "MUSTANG", "RANGER",
                     "TERRITORY", "TRANSIT", "WINDSTAR"]},
      "FOTON": 
         {"valor_rentanacional": 10582,
         "valor_liberty": "FOTON",
         "valor_reale": "FOTON",
         "modelos": ["FT BOX", "FT-500", "FT-CREW", "G7", "K1", "MIDI", "MIDI TRUCK",
                     "SAUVANA", "SUP", "TERRACOTA", "TM5"]},
      "GAC GONOW": 
         {"valor_rentanacional": 10790,
         "valor_liberty": "GAC GONOW",
         "valor_reale": "GAC MOTORS",
         "modelos": ["EMKOO", "EMZOOM", "GA-4", "GS-3", "GS-4", "GS-5",
                  "STARRY", "WAY CABINA DOBLE", "WAY CABINA SIMPLE",
                  "WAY CARGO", "WAY CARGO BOX", "WAY PASAJEROS"]},
      "GEELY": 
         {"valor_rentanacional": 10402,
         "valor_liberty": "GEELY",
         "valor_reale": "GEELY",
         "modelos": ["AZKARRA", "CK", "COOLRAY", "EC7", "EMGRAND", "EX7",
                     "GC7 GL 1.5", "GS", "LC", "MK", "SL", "X7"]},
      "G.M.C":
         {"valor_reale": "G.M.C",
      "modelos": ["SIERRA"]},

    "GREAT WALL": 
   {"valor_rentanacional": 10430,
    "valor_liberty": "GREAT WALL",
    "valor_reale": "GREAT WALL",
    "modelos": ["C30", "DEER", "FLORID", "GREAT WALL 3", "GREAT WALL 5", "GREAT WALL 6", "H6", "HAVAL", 
                "HOVER", "M4", "PERI", "POER", "SAFE", "SOCOOL", "VOLEEX", "VOLFEX C30", "VOLLEX C 10", 
                "VOLLEX C20", "VOLLEX C50", "WINGLE", "WINGLE 4", "WINGLE 5", "WINGLE 6", "WINGLE 7"]},
   "HAFEI": 
      {"valor_rentanacional": 10665,
      "valor_liberty": "HAFEI",
      "valor_reale": "HAFEI",
      "modelos": ["LOBO", "MINI VAN", "MINYI", "RUIYI", "ZHONGYI"]},
   "HAIMA": 
      {"valor_rentanacional": 10562, 
      "valor_liberty": "HAIMA", 
      "valor_reale": "HAIMA",
      "modelos": ["F-STAR", "HAIMA 2", "HAIMA 3", "HAIMA 7"]},
   "HAVAL": 
      {"valor_rentanacional": 10826, 
      "valor_liberty": "HAVAL", 
      "valor_reale": "HAVAL",
      "modelos": ["DARGO", "H6", "H7", "HAVAL 2", "JOLION"]},
   "HONDA": 
      {"valor_rentanacional": 10017, 
      "valor_liberty": "HONDA", 
      "valor_reale": "HONDA",
      "modelos": ["ACCORD", "CITY", "CIVIC", "CRV 2.4", "FIT", "HRV", "INTEGRA", "LEGEND", "ODYSSEY",
                  "PILOT", "RIDGELINE", "STREAM", "WR-V", "ZR-V"]},
   "HYUNDAI":
      {"valor_rentanacional": 10018,
      "valor_liberty": "HYUNDAI",
      "valor_reale": "HYUNDAI",
      "modelos": ["ACCENT", "ATOS", "AZERA", "CITY", "COUPE", "CRETA", "ELANTRA", "EON", 
                  "GALLOPER", "GETZ", "GRACE", "GRACE VAN", "GRAND I-10", "H-1", "H-350", 
                  "I 10", "I 30", "I20", "I40 GL 2.0", "IONIQ HYBRID", "MATRIX", "PALISADE", 
                  "SANTA FE", "SANTAMO", "SONATA", "STAREX", "STARIA", "TERRACAN", "TRAJET", 
                  "TUCSON", "VELOSTER", "VENUE", "VERACRUZ", "VERNA 1.4", "XG"]},
   "JAC": 
      {"valor_rentanacional": 10346, 
      "valor_liberty": "JAC", 
      "valor_reale": "JAC",
      "modelos": ["A 137", "B15", "GRAND S3", "J2", "J3", "J4", "J5 2.0", "J6", "JS 2", "JS 3", "JS 4",
                  "JS 6", "JS 8", "REFINE", "REIN", "S1", "S2", "S3", "S4", "S5", "SUNRAY", "T6", "T8", "TRIP", "X 200"]},
   "JEEP": 
      {"valor_rentanacional": 10021,
      "valor_liberty": "JEEP", 
      "valor_reale": "JEEP",
      "modelos": ["CHEROKEE SPORT", "COMMANDER", "COMPASS", "GLADIATOR", "GRAND CHEROKEE", "LIBERTY", "PATRIOT", "RENEGADE",
                  "RENEGADE SPORT", "WRANGLER RUBICON", "WRANGLER UNLIMITED"]},
   "JETOUR": 
      {"valor_rentanacional": 11036,
      "valor_liberty": "JETOUR", 
      "valor_reale": "JETOUR",
      "modelos": ["X70"]},
   "JINBEI": 
      {"valor_rentanacional": 10598, 
      "valor_liberty": "JINBEI", 
      "valor_reale": "JINBEI",
      "modelos": ["HAISE 2.0", "LOW ROOF"]},
   "JMC": 
      {"valor_rentanacional": 10617,
      "valor_liberty": "JMC", 
      "valor_reale": "JMC",
      "modelos": ["BOARDING", "GRAND AVENUE", "TOURING", "VIGUS"]},
   "KARRY":
      {"valor_rentanacional": 11068, 
      "valor_liberty": "KARRY",
      "valor_reale": "KARRY",
      "modelos": ["GRAN MAMUT", "T3", "X5"]},
   "KIA MOTORS":
      {"valor_rentanacional": 10022, 
      "valor_liberty": "KIA MOTORS", 
      "valor_reale": "KIA MOTORS",
      "modelos": ["SPORTAGE", "SOUL", "AVELLA", "BESTA", "CADENZA", "CARENS", "CARNIVAL", "CERATO", 
                   "CERATO 5", "CERES", "CLARUS", "GRAND CARNIVAL", "K 2400", "KOUP", 
                   "MAGENTIS", "MOHAVE", "MORNING", "NIRO", "OPIRUS", "OPTIMA", "PRIDE",
                     "RIO", "RIO 3", "RIO 4", "RIO 5", "RIO JB", "ROCSTA", "SELTOS", "SEPHIA", 
                     "SOLUTO", "SONET"]},
   "KYC": 
      {"valor_rentanacional": 11011, 
      "valor_liberty": "KYC", 
      "valor_reale": "KYC",
      "modelos": ["GRAN MAMUT", "T3", "X5"]},

   "KENBO":{"valor_reale":"KENBO",
            "modelos":["206","T205"]},
                     
   "LANDWIND":{"valor_reale" :"LANDWIND",
               "modelos":"LUX"},
   "LAND ROVER": 
      {"valor_rentanacional": 10025,
      "valor_liberty": "LAND ROVER", 
      "valor_reale": "LAND ROVER",
      "modelos": ["DEFENDER","DISCOVERY","EVOQUE","FRELANDER","RANGE ROVER","VELAR"]},
   "LIFAN": 
      {"valor_rentanacional": 10358, 
      "valor_liberty": "LIFAN", 
      "valor_reale": "LIFAN",
      "modelos": ["320", "330", "520", "530", "620", "FOISON", "TRUCK", "X50", "X60", "X7", "X70"]},
   "MAHINDRA": 
      {"valor_rentanacional": 10243,
      "valor_liberty": "MAHINDRA", 
      "valor_reale": "MAHINDRA",
      "modelos": ["320", "330", "520", "530", "620", "FOISON", "TRUCK", "X50", "X60", "X7", "X70"]},
   "MAPLE": {"valor_reale":"MAPLE",
             "modelos":["30X"]},
   "MAZDA": 
      {"valor_rentanacional": 10028, 
      "valor_liberty": "MAZDA", 
      "valor_reale": "MAZDA",
      "modelos": ["", "323", "626", "ARTIS", "B 2200", "B 2500", "B 2600", "B 2900", 
      "BT 50", "CX 30", "CX 60", "CX 90", "CX-3", "CX5", "CX-7", "CX-9", 
      "MAZDA 2", "MAZDA 3", "MAZDA 5", "MAZDA 6", "MPV", "TRIBUTE"]},
   "MITSUBISHI":
   {"valor_rentanacional": 10033, 
      "valor_liberty": "MITSUBISHI", 
      "valor_reale": "MITSUBISHI",
      "modelos": ["ASX", "COLT", "ECLIPSE CROSS", "GALANT", "L-200", "L-300", "LANCER", 
      "MIRAGE", "MONTERO", "MONTERO SPORT", "OUTLANDER", "XPANDER"]},
   "MERCEDES BENZ": 
      {"valor_rentanacional": 10029, 
      "valor_liberty": "MERCEDES BENZ", 
      "valor_reale": "MERCEDES BENZ",
      "modelos": ["DELIVER 9", "G 10", "T 60 4X2", "T 90", "V80", "V90"]},
   "MG": 
      {"valor_rentanacional": 10489, 
      "valor_liberty": "MG", 
      "valor_reale": "MG",
      "modelos": ["350", "360", "5", "550", "6", "750", "GS", "GT", "HS", "MG3", "ONE", "RX5", "ZS", "ZX"]},
   "MINI": 
      {"valor_rentanacional": 10032, 
      "valor_liberty": "MINI", 
      "valor_reale": "MINI",
      "modelos": ["COOPER", "COOPER S", "COUNTRYMAN", "PACEMAN"]},
   "NISSAN": 
      {"valor_rentanacional": 10035, 
      "valor_liberty": "NISSAN",
      "valor_reale": "NISSAN",
      "modelos": ["ALMERA", "ALTIMA", "D 21", "D-22 TERRANO", "JUKE", "KICKS", "LEAF", 
      "MARCH", "MAXIMA", "MURANO", "NAVARA", "NOTE", "NP300", "NV 350", "PATHFINDER", "PATROL", "PLATINA", "PRIMERA", "QASHQAI", "SENTRA", 
      "TEANA", "TERRANO", "TIIDA", "URVAN", "V16", "VERSA", "X TRAIL"]},
   "OPEL": 
      {"valor_rentanacional": "", 
      "valor_liberty": "OPEL", 
      "valor_reale": "OPEL",
      "modelos": ["ADAM","ASTRA","CORSA","INSIGNIA","MERIVA","MOKKA"]},
   "PEUGEOT": 
      {"valor_rentanacional": 10038, 
      "valor_liberty": "PEUGEOT", 
      "valor_reale": "PEUGEOT",
      "modelos": ["106", "107", "108", "2008", "205", "206", "207", "208", "3008", "301", "306", "307", "308", "4008", "405", "407", "5008", 
                  "508", "605", "BOXER", "EXPERT", "LANDTREK", "PARTNER", "RCZ", "RIFTER", "TEPEE OUTDOOR", "TRAVELLER"]},
   "PORSCHE": 
      {"valor_rentanacional": "", 
      "valor_liberty": "PORSCHE",
      "valor_reale": "PORSCHE",
      "modelos": []},
   "PRUEBA_PAROT": 
      {"valor_rentanacional": "", 
      "valor_liberty": "PRUEBA_PAROT", 
      "valor_reale": "PRUEBA_PAROT",
      "modelos": []},
    "RAM":
    {"valor_rentanacional": 10913,
     "valor_liberty": "RAM", 
     "valor_reale": "RAM",
     "modelos": ["RAM 1000", "RAM 1200", "RAM 1500", "RAM 700", "VAN 1000", "VAN 700"]},
"RENAULT": 
   {"valor_rentanacional": 10040, 
     "valor_liberty": "RENAULT", 
     "valor_reale": "RENAULT",
     "modelos": ["ALASKAN", "ARKANA", "CAPTUR", "CLIO", "DOKKER", "DUSTER", "EXPRESS", "FLUENCE", "KANGOO", "KOLEOS", 
                "KWID", "LAGUNA", "LATITUDE", "LOGAN", "MASTER", "MEGANE", "OROCH", "SANDERO", "SCENIC", "STEPWAY", "SYMBOL", "TRAFIC", "TWINGO"]},
"ROVER": 
   {"valor_rentanacional": "", 
    "valor_liberty": "ROVER", 
    "valor_reale": "ROVER",
    "modelos": []},
"SAMSUNG":
     {"valor_rentanacional": 10042, 
     "valor_liberty": "SAMSUNG", 
     "valor_reale": "SAMSUNG",
     "modelos": ["SM3", "SM5", "SM7", "SQ 5"]},
"SEAT": 
   {"valor_rentanacional": 10128,
     "valor_liberty": "SEAT", 
     "valor_reale": "SEAT",
     "modelos": ["ARONA", "ATECA", "IBIZA", "LEON", "TERRACO"]},
"SKODA": 
   {"valor_rentanacional": 10044, 
    "valor_liberty": "SKODA", 
    "valor_reale": "SKODA",
    "modelos": ["FABIA", "FELICIA", "KAMIQ", "KAROQ", "KODIAQ", "OCTAVIA", "PICK UP", "RAPID", "SCALA", "SCOUT", "SPACEBACK", "YETI"]},
"SSANGYONG": 
   {"valor_rentanacional": 10045, 
    "valor_liberty": "SSANGYONG", 
    "valor_reale": "SSANGYONG",
    "modelos": ["ACTYON SPORT", "GRAND MUSSO", "KORANDO", "KYRON", "MUSSO", "REXTON", "STAVIC", "TIVOLI", "TORRES", "XLV"]},
"SUBARU": 
   {"valor_rentanacional": 10046, 
    "valor_liberty": "SUBARU",
      "valor_reale": "SUBARU",
      "modelos": ["ALL NEW FORESTER", "ALL NEW LEGACY", "ALL NEW OUTBACK", "BAJA", "CROSSTREK", 
                   "EVOLTIS", "FORESTER", "IMPREZA", "LEGACY", "OUTBACK", "TRIBECA", "WRX", "XV"]},
"SUZUKI": 
   {"valor_rentanacional": 10047,
     "valor_liberty": "SUZUKI", 
     "valor_reale": "SUZUKI",
     "modelos": ["AERIO", "ALTO", "APV", "BALENO", "CARRY ALL", "CELERIO", "CIAZ", "DZIRE", "ERTIGA", "FRONX", "GRAND NOMADE", "GRAND VITARA", 
                 "IGNIS", "JIMNY", "KIZASHI", "LIANA", "MARUTI", "MASTERVAN", "NOMADE", "SAMURAI", "S-CROSS", "S-PRESSO 1.0 GLX AC", "SWIFT", 
                 "SX 4", "VITARA", "XL7"]},
"SHINERAY": 
   {"valor_rentanacional": "", 
    "valor_liberty": "SHINERAY",
    "valor_reale": "SHINERAY",
    "modelos": []},
"SMA": 
   {"valor_rentanacional": "",
     "valor_liberty": "SMA", 
     "valor_reale": "SMA",
     "modelos": []},
"SWM":
   {"valor_rentanacional": 10047, 
   "valor_liberty": "SWM",
   "valor_reale": "SWM",
   "modelos": []},
"TRAVIN TASKEN":{"valor_reale":"TRAVIN TASKEN",
                  "modelos":["695"]},
"TATA":
   {"valor_rentanacional": 10296, 
    "valor_liberty": "TATA", 
    "valor_reale": "TATA",
    "modelos": ["XENON"]},
"TOYOTA": 
   {"valor_rentanacional": 10048, 
    "valor_liberty": "TOYOTA", 
    "valor_reale": "TOYOTA",
    "modelos": ["4 RUNNER", "ADVANTAGE", "AURIS", "AVENSIS", "AYGO 1.0", "CAMRY", 
               "CH-R", "COROLLA", "COROLLA CROSS", "COROLLA CROSS HYBRID", "CORONA", 
               "FJ CRUISER", "FORTUNER", "HIACE", "HILUX", "LAND CRUISER PRADO", 
                "PRIUS", "PRIUS C", "RAIZE", "RAV 4", "RUSH", "SEQUOIA", "TACOMA", 
                "TERCEL", "URBAN CRUISER", "YARIS", "YARIS SPORT", "ZELAS"]},
"VOLKSWAGEN":
   {"valor_rentanacional": 10049,
   "valor_liberty": "VOLKSWAGEN",
    "valor_reale": "VOLKSWAGEN",
    "modelos": ["AMAROK", "ATLAS", "BEETLE", "BORA", "CROSSFOX", "FOX", "GOL", "GOLF", "JETTA",
                "MULTIVAN", "NIVUS", "PASSAT", "POLO", "SAVEIRO", "SCIROCCO", "SURAN", "TAOS", "T-CROSS",
                 "TIGUAN", "TOUAREG", "TRANSPORTER", "UP", "VENTO", "VIRTUS", "VOYAGE"]},
"VOLVO": 
   {"valor_rentanacional": 10050,
     "valor_liberty": "VOLVO", 
     "valor_reale": "VOLVO",
     "modelos": ["C 30", "C 70", "S 40", "S 60", 
                 "S 70", "S 80", "S 90", "V 40", "V60", "V70", "V90", "XC 40", "XC 70", "XC 90", "XC60"]},
"ZNA":
     {"valor_rentanacional": 10688, 
     "valor_liberty": "ZNA",
     "valor_reale": "ZNA",
     "modelos": ["MINISTAR", "MINITRUCK", "RICH 2.5", "SUCCE", "YUMSUN"]},
"ZOTYE": 
   {"valor_rentanacional": 10486, 
    "valor_liberty": "ZOTYE", 
    "valor_reale": "ZOTYE",
    "modelos": ["HUNTER"]},
"ZX AUTO":
  {"valor_rentanacional": 10380, 
   "valor_liberty": "ZX AUTO", 
   "valor_reale": "ZX AUTO",
   "modelos": ["ADMIRAL", "GRANDTIGER", "LANDMARK", "TERRALORD", "TUV"]}
}


marcas = list(marcas_numericas.keys())
print(marcas)


valores_rubro = {
    "Contenedores": 1,
    "Materiales de Construccion": 2,
    "Transporte rubro propio de la empresa": 3,
    "Telecomunicaciones": 4,
    "Transporte personal: Empresa/Institucion": 5,
    "Turismo": 6,
    "Taxi": 7,
    "Transporte Escolar": 8,
    "Transporte publico de pasajeros": 9,
    "Transporte privado de pasajeros": 10,
    "Seguridad Publica": 11
}

comunas = {
   "ALGARROBO - VALPARAÍSO",
"ALHUÉ - METROPOLITANA DE SANTIAGO",
"ALTO BIOBÍO - BIOBÍO",
"ALTO DEL CARMEN - ATACAMA",
"ALTO HOSPICIO - TARAPACÁ",
"ANCUD - LOS LAGOS",
"ANDACOLLO - COQUIMBO",
"ANGOL - ARAUCANÍA",
"ANTOFAGASTA - ANTOFAGASTA",
"ANTUCO - BIOBÍO",
"ANTÁRTICA - MAGALLANES Y DE LA ANTÁRTICA",
"ARAUCO - BIOBÍO",
"ARICA - ARICA Y PARINACOTA",
"AYSÉN - AYSÉN GRAL C. IBÁÑEZ DEL CAMPO",
"BUIN - METROPOLITANA DE SANTIAGO",
"BULNES - ÑUBLE",
"CABILDO - VALPARAÍSO",
"CABO DE HORNOS - MAGALLANES Y DE LA ANTÁRTICA",
"CABRERO - BIOBÍO",
"CALAMA - ANTOFAGASTA",
"CALBUCO - LOS LAGOS",
"CALDERA - ATACAMA",
"CALERA DE TANGO - METROPOLITANA DE SANTIAGO",
"CALLE LARGA - VALPARAÍSO",
"CAMARONES - ARICA Y PARINACOTA",
"CAMIÑA - TARAPACÁ",
"CANELA - COQUIMBO",
"CARAHUE - ARAUCANÍA",
"CARTAGENA - VALPARAÍSO",
"CASABLANCA - VALPARAÍSO",
"CASTRO - LOS LAGOS",
"CATEMU - VALPARAÍSO",
"CAUQUENES - MAULE",
"CAÑETE - BIOBÍO",
"CERRILLOS - METROPOLITANA DE SANTIAGO",
"CERRO NAVIA - METROPOLITANA DE SANTIAGO",
"CHAITÉN - LOS LAGOS",
"CHANCO - MAULE",
"CHAÑARAL - ATACAMA",
"CHIGUAYANTE - BIOBÍO",
"CHILE CHICO - AYSÉN GRAL C. IBÁÑEZ DEL CAMPO",
"CHILLÁN - ÑUBLE",
"CHILLÁN VIEJO - ÑUBLE",
"CHIMBARONGO - DEL LIBERTADOR BDO. O'HIGGINS",
"CHOLCHOL - ARAUCANÍA",
"CHONCHI - LOS LAGOS",
"CHÉPICA - DEL LIBERTADOR BDO. O'HIGGINS",
"CISNES - AYSÉN GRAL C. IBÁÑEZ DEL CAMPO",
"COBQUECURA - ÑUBLE",
"COCHAMÓ - LOS LAGOS",
"COCHRANE - AYSÉN GRAL C. IBÁÑEZ DEL CAMPO",
"CODEGUA - DEL LIBERTADOR BDO. O'HIGGINS",
"COELEMU - ÑUBLE",
"COIHUECO - ÑUBLE",
"COINCO - DEL LIBERTADOR BDO. O'HIGGINS",
"COLBÚN - MAULE",
"COLCHANE - TARAPACÁ",
"COLINA - METROPOLITANA DE SANTIAGO",
"COLLIPULLI - ARAUCANÍA",
"COLTAUCO - DEL LIBERTADOR BDO. O'HIGGINS",
"COMBARBALÁ - COQUIMBO",
"CONCEPCIÓN - BIOBÍO",
"CONCHALÍ - METROPOLITANA DE SANTIAGO",
"CONCÓN - VALPARAÍSO",
"CONSTITUCIÓN - MAULE",
"CONTULMO - BIOBÍO",
"COPIAPÓ - ATACAMA",
"COQUIMBO - COQUIMBO",
"CORONEL - BIOBÍO",
"CORRAL - LOS RÍOS",
"COYHAIQUE - AYSÉN GRAL C. IBÁÑEZ DEL CAMPO",
"CUNCO - ARAUCANÍA",
"CURACAUTÍN - ARAUCANÍA",
"CURACAVÍ - METROPOLITANA DE SANTIAGO",
"CURACO DE VÉLEZ - LOS LAGOS",
"CURANILAHUE - BIOBÍO",
"CURARREHUE - ARAUCANÍA",
"CURICÓ - MAULE",
"DALCAHUE - LOS LAGOS",
"DIEGO DE ALMAGRO - ATACAMA",
"DOÑIHUE - DEL LIBERTADOR BDO. O'HIGGINS",
"EL BOSQUE - METROPOLITANA DE SANTIAGO",
"EL CARMEN - ÑUBLE",
"EL MONTE - METROPOLITANA DE SANTIAGO",
"EL TABO - VALPARAÍSO",
"EMPEDRADO - MAULE",
"ENSENADA - LOS LAGOS",
"ESTACIÓN CENTRAL - METROPOLITANA DE SANTIAGO",
"FLORIDA - ÑUBLE",
"FREIRE - ARAUCANÍA",
"FREIRINA - ATACAMA",
"FRUTILLAR - LOS LAGOS",
"FUTALEUFÚ - LOS LAGOS",
"FUTRONO - LOS RÍOS",
"GALVARINO - ARAUCANÍA",
"GENERAL LAGOS - LOS RÍOS",
"GORBEA - ARAUCANÍA",
"GRANEROS - DEL LIBERTADOR BDO. O'HIGGINS",
"GUAITECAS - AYSÉN GRAL C. IBÁÑEZ DEL CAMPO",
"HIJUELAS - VALPARAÍSO",
"HUALAIHUÉ - LOS LAGOS",
"HUALAÑÉ - MAULE",
"HUALPÉN - BIOBÍO",
"HUALQUI - BIOBÍO",
"HUARA - TARAPACÁ",
"HUASCO - ATACAMA",
"HUECHURABA - METROPOLITANA DE SANTIAGO",
"ILLAPEL - COQUIMBO",
"INDEPENDENCIA - METROPOLITANA DE SANTIAGO",
"IQUIQUE - TARAPACÁ",
"ISLA DE MAIPO - METROPOLITANA DE SANTIAGO",
"ISLA DE PASCUA - VALPARAÍSO",
"JUAN FERNÁNDEZ - VALPARAÍSO",
"LA CISTERNA - METROPOLITANA DE SANTIAGO",
"LA CRUZ - VALPARAÍSO",
"LA ESTRELLA - DEL LIBERTADOR BDO. O'HIGGINS",
"LA FLORIDA - METROPOLITANA DE SANTIAGO",
"LA GRANJA - METROPOLITANA DE SANTIAGO",
"LA HIGUERA - COQUIMBO",
"LA LIGUA - VALPARAÍSO",
"LA PINTANA - METROPOLITANA DE SANTIAGO",
"LA REINA - METROPOLITANA DE SANTIAGO",
"LA SERENA - COQUIMBO",
"LA UNIÓN - LOS RÍOS",
"LAGO RANCO - LOS RÍOS",
"LAGO VERDE - AYSÉN GRAL C. IBÁÑEZ DEL CAMPO",
"LAGUNA BLANCA - MAGALLANES Y DE LA ANTÁRTICA",
"LAJA - BIOBÍO",
"LAMPA - METROPOLITANA DE SANTIAGO",
"LANCO - LOS RÍOS",
"LAS CABRAS - DEL LIBERTADOR BDO. O'HIGGINS",
"LAS CONDES - METROPOLITANA DE SANTIAGO",
"LAUTARO - ARAUCANÍA",
"LEBU - BIOBÍO",
"LICANTÉN - MAULE",
"LIHUEIMO - AYSÉN GRAL C. IBÁÑEZ DEL CAMPO",
"LIMACHE - VALPARAÍSO",
"LINARES - MAULE",
"LITUECHE - DEL LIBERTADOR BDO. O'HIGGINS",
"LLANQUIHUE - LOS LAGOS",
"LO BARNECHEA - METROPOLITANA DE SANTIAGO",
"LO ESPEJO - METROPOLITANA DE SANTIAGO",
"LO PRADO - METROPOLITANA DE SANTIAGO",
"LOLA - ARAUCANÍA",
"LONCOCHE - ARAUCANÍA",
"LONGAVÍ - MAULE",
"LONGOVILO - ARAUCANÍA",
"LONQUIMAY - ARAUCANÍA",
"LOS ÁLAMOS - BIOBÍO",
"LOS ANDES - VALPARAÍSO",
"LOS ÁNGELES - BIOBÍO",
"LOS LAGOS - LOS RÍOS",
"LOS MUERMOS - LOS LAGOS",
"LOS SAUCES - ARAUCANÍA",
"LOS VILOS - COQUIMBO",
"LOTA - BIOBÍO",
"LUMACO - ARAUCANÍA",
"MACHALÍ - DEL LIBERTADOR BDO. O'HIGGINS",
"MACUL - METROPOLITANA DE SANTIAGO",
"MAIPÚ - METROPOLITANA DE SANTIAGO",
"MALLOA - DEL LIBERTADOR BDO. O'HIGGINS",
"MARCHIHUE - DEL LIBERTADOR BDO. O'HIGGINS",
"MARIQUINA - LOS RÍOS",
"MARÍA ELENA - ANTOFAGASTA",
"MARÍA PINTO - METROPOLITANA DE SANTIAGO",
"MARIQUINA - LOS RÍOS",
"MAULE - MAULE",
"MAULLÍN - LOS LAGOS",
"MEJILLONES - ANTOFAGASTA",
"MELIPEUCO - ARAUCANÍA",
"MELIPILLA - METROPOLITANA DE SANTIAGO",
"MOLINA - MAULE",
"MONTE PATRIA - COQUIMBO",
"MOSTAZAL - DEL LIBERTADOR BDO. O'HIGGINS",
"MULCHÉN - BIOBÍO",
"NACIMIENTO - BIOBÍO",
"NANCAGUA - DEL LIBERTADOR BDO. O'HIGGINS",
"NATALES - MAGALLANES Y DE LA ANTÁRTICA",
"NAVIDAD - DEL LIBERTADOR BDO. O'HIGGINS",
"NECOCHEA - LOS RÍOS",
"NINHUE - ÑUBLE",
"NOGALES - VALPARAÍSO",
"NUEVA IMPERIAL - ARAUCANÍA",
"ÑIQUÉN - ÑUBLE",
"ÑUÑOA - METROPOLITANA DE SANTIAGO",
"OLIVAR - DEL LIBERTADOR BDO. O'HIGGINS",
"OLLAGÜE - ANTOFAGASTA",
"OLLOLLETA - ARAUCANÍA",
"OSORNO - LOS LAGOS",
"OVALLE - COQUIMBO",
"O' HIGGINS - ANTÁRTICA CHILENA",
"PADRE HURTADO - METROPOLITANA DE SANTIAGO",
"PADRE LAS CASAS - ARAUCANÍA",
"PAIGUANO - COQUIMBO",
"PAILLACO - LOS RÍOS",
"PAINE - METROPOLITANA DE SANTIAGO",
"PALENA - LOS LAGOS",
"PALMILLA - DEL LIBERTADOR BDO. O'HIGGINS",
"PANQUEHUE - VALPARAÍSO",
"PAPUDO - VALPARAÍSO",
"PAREDONES - DEL LIBERTADOR BDO. O'HIGGINS",
"PARRAL - MAULE",
"PEDRO AGUIRRE CERDA - METROPOLITANA DE SANTIAGO",
"PELARCO - MAULE",
"PELLUHUE - MAULE",
"PELVINI - LOS RÍOS",
"PENAFLOR - METROPOLITANA DE SANTIAGO",
"PÉREZ - DEL LIBERTADOR BDO. O'HIGGINS",
"PETORCA - VALPARAÍSO",
"PEUMO - DEL LIBERTADOR BDO. O'HIGGINS",
"PICA - TARAPACÁ",
"PICHIDEGUA - DEL LIBERTADOR BDO. O'HIGGINS",
"PICHILEMU - DEL LIBERTADOR BDO. O'HIGGINS",
"PINTO - ÑUBLE",
"PIRQUE - METROPOLITANA DE SANTIAGO",
"PITRUFQUÉN - ARAUCANÍA",
"PLACILLA - DEL LIBERTADOR BDO. O'HIGGINS",
"PORTEZUELO - ÑUBLE",
"PORVENIR - MAGALLANES Y DE LA ANTÁRTICA",
"POZO ALMONTE - TARAPACÁ",
"PRIEGUE - LOS RÍOS",
"PROVIDENCIA - METROPOLITANA DE SANTIAGO",
"PUCHUNCAVÍ - VALPARAÍSO",
"PUCÓN - ARAUCANÍA",
"PUDAHUEL - METROPOLITANA DE SANTIAGO",
"PUEBLO SECO - MAULE",
"PUEBLO DE DIOS - COQUIMBO",
"PUEBLO HUNDIDO - LOS RÍOS",
"PUEBLITO - LOS RÍOS",
"PUEBLO NUEVO - ÑUBLE",
"PUENTE ALTO - METROPOLITANA DE SANTIAGO",
"PUERTO AYSÉN - AYSÉN DEL GENERAL CARLOS IBÁÑEZ DEL CAMPO",
"PUERTO CISNES - AYSÉN DEL GENERAL CARLOS IBÁÑEZ DEL CAMPO",
"PUERTO MONTT - LOS LAGOS",
"PUERTO NATALES - MAGALLANES Y DE LA ANTÁRTICA",
"PUERTO OCTAY - LOS LAGOS",
"PUERTO VARAS - LOS LAGOS",
"PUMANQUE - DEL LIBERTADOR BDO. O'HIGGINS",
"PUNITAQUI - COQUIMBO",
"PUNTA ARENAS - MAGALLANES Y DE LA ANTÁRTICA",
"PUQUELDÓN - LOS LAGOS",
"PURÉN - ARAUCANÍA",
"PURRANQUE - LOS LAGOS",
"PUTAENDO - VALPARAÍSO",
"PUTÚ - MAULE",
"PUYEHUE - LOS LAGOS",
"QUEILÉN - LOS LAGOS",
"QUELLÓN - LOS LAGOS",
"QUEMCHI - LOS LAGOS",
"QUILACO - BIOBÍO",
"QUILICURA - METROPOLITANA DE SANTIAGO",
"QUILLECO - BIOBÍO",
"QUILLÓN - ÑUBLE",
"QUILLOTA - VALPARAÍSO",
"QUILPUÉ - VALPARAÍSO",
"QUINCHAO - LOS LAGOS",
"QUINTA DE TILCOCO - DEL LIBERTADOR BDO. O'HIGGINS",
"QUINTA NORMAL - METROPOLITANA DE SANTIAGO",
"QUIRIHUE - ÑUBLE",
"RAHUE - LOS RÍOS",
"RAÍCES - LOS LAGOS",
"RAMADILLAS - COQUIMBO",
"RÁNQUIL - ÑUBLE",
"RÁNQUILCO - ÑUBLE",
"RAUCO - MAULE",
"RAÚL MARÍN BAJO - LOS LAGOS",
"RECOLETA - METROPOLITANA DE SANTIAGO",
"RENGO - DEL LIBERTADOR BDO. O'HIGGINS",
"RENCA - METROPOLITANA DE SANTIAGO",
"RÍO BUENO - LOS RÍOS",
"RÍO CLARO - DEL LIBERTADOR BDO. O'HIGGINS",
"RÍO IBÁÑEZ - AYSÉN GRAL C. IBÁÑEZ DEL CAMPO",
"RÍO NEGRO - LOS LAGOS",
"RÍO VERDE - MAGALLANES Y DE LA ANTÁRTICA",
"ROMERAL - DEL LIBERTADOR BDO. O'HIGGINS",
"SAAVEDRA - ARAUCANÍA",
"SAGRADA FAMILIA - MAULE",
"SALAMANCA - COQUIMBO",
"SAN ANTONIO - VALPARAÍSO",
"SAN BERNARDO - METROPOLITANA DE SANTIAGO",
"SAN CARLOS - ÑUBLE",
"SAN CLEMENTE - MAULE",
"SAN ESTEBAN - VALPARAÍSO",
"SAN FABIÁN - ÑUBLE",
"SAN FELIPE - VALPARAÍSO",
"SAN FERNANDO - DEL LIBERTADOR BDO. O'HIGGINS",
"SAN GREGORIO - MAGALLANES Y DE LA ANTÁRTICA",
"SAN JAVIER - MAULE",
"SAN JOAQUÍN - METROPOLITANA DE SANTIAGO",
"SAN JOSÉ DE MAIPO - METROPOLITANA DE SANTIAGO",
"SAN JUAN DE LA COSTA - LOS RÍOS",
"SAN MIGUEL - METROPOLITANA DE SANTIAGO",
"SAN NICOLÁS - ÑUBLE",
"SAN PABLO - LOS RÍOS",
"SAN PEDRO - BIOBÍO",
"SAN PEDRO DE ATACAMA - ANTOFAGASTA",
"SAN PEDRO DE LA PAZ - BIOBÍO",
"SAN RAFAEL - DEL LIBERTADOR BDO. O'HIGGINS",
"SAN RAMÓN - METROPOLITANA DE SANTIAGO",
"SAN ROSENDO - BIOBÍO",
"SAN VICENTE - DEL LIBERTADOR BDO. O'HIGGINS",
"SANTA BÁRBARA - BIOBÍO",
"SANTA CRUZ - DEL LIBERTADOR BDO. O'HIGGINS",
"SANTA JUANA - BIOBÍO",
"SANTA MARÍA - VALPARAÍSO",
"SANTIAGO - METROPOLITANA DE SANTIAGO",
"SANTO DOMINGO - VALPARAÍSO",
"SIERRA GORDA - ANTOFAGASTA",
"SIN DEFINIR - METROPOLITANA DE SANTIAGO",
"TALAGANTE - METROPOLITANA DE SANTIAGO",
"TALCA - MAULE",
"TALCAHUANO - BIOBÍO",
"TALTAL - ANTOFAGASTA",
"TAMARUGAL - TARAPACÁ",
"TEMUCO - ARAUCANÍA",
"TENO - DEL LIBERTADOR BDO. O'HIGGINS",
"TEODORO SCHMIDT - ARAUCANÍA",
"TIERRA AMARILLA - ATACAMA",
"TILTIL - METROPOLITANA DE SANTIAGO",
"TIMAUKEL - MAGALLANES Y DE LA ANTÁRTICA",
"TIRÚA - BIOBÍO",
"TOCOPILLA - ANTOFAGASTA",
"TOLTÉN - ARAUCANÍA",
"TOMÉ - BIOBÍO",
"TORRES DEL PAINE - MAGALLANES Y DE LA ANTÁRTICA",
"TORTEL - AYSÉN GRAL C. IBÁÑEZ DEL CAMPO",
"TRAIGUÉN - ÑUBLE",
"TREGUACO - ÑUBLE",
"TREHUACO - ÑUBLE",
"TUCAPEL - ÑUBLE",
"VALDIVIA - LOS RÍOS",
"VALLENAR - ATACAMA",
"VALPARAÍSO - VALPARAÍSO",
"VICHUQUÉN - MAULE",
"VICTORIA - ARAUCANÍA",
"VICUÑA - COQUIMBO",
"VILCÚN - ARAUCANÍA",
"VILLA ALEMANA - VALPARAÍSO",
"VILLA ALEGRE - MAULE",
"VILLARRICA - ARAUCANÍA",
"VIÑA DEL MAR - VALPARAÍSO",
"VITACURA - METROPOLITANA DE SANTIAGO",
"YERBAS BUENAS - MAULE",
"YUMBEL - BIOBÍO",
"YUNGAY - ÑUBLE",
"ZAPALLAR - VALPARAÍSO",
"ÑIQUÉN - ÑUBLE",
"ÑUÑOA - METROPOLITANA DE SANTIAGO"}



#______________________________________________________________________________________________________________________________________________________________________________    
#INTERFAZ GRÁFICA   
# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Selección de Vehículo")

# Variables de control
marca_var = tk.StringVar()
modelo_var = tk.StringVar()
tipo_vehiculo_var = tk.StringVar()
tipo_persona_var = tk.StringVar()
uso_vehiculo_var = tk.StringVar()
patente_var = tk.StringVar()
ano_var = tk.StringVar()
estilo_var = tk.StringVar()
comuna_var = tk.StringVar()
# Marco principal
marco_principal = ttk.Frame(ventana, padding="10")
marco_principal.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Etiqueta y lista desplegable para la marca
ttk.Label(marco_principal, text="Seleccione la marca:").grid(row=0, column=0, sticky=tk.W)
marca_combobox = ttk.Combobox(marco_principal, textvariable=marca_var, values=list(marcas_numericas.keys()))
marca_combobox.grid(row=0, column=1, sticky=tk.W, pady=5)
# Enlazar la función de actualización a la selección de la marca
marca_var.trace_add('write', actualizar_modelos)

# Etiqueta y lista desplegable para el modelo
ttk.Label(marco_principal, text="Seleccione el modelo:").grid(row=1, column=0, sticky=tk.W)
modelo_combobox = ttk.Combobox(marco_principal, textvariable=modelo_var, values=[])
modelo_combobox.grid(row=1, column=1, sticky=tk.W, pady=5)

# Etiqueta y lista desplegable para el uso del vehículo
ttk.Label(marco_principal, text="Seleccione el uso del vehículo:").grid(row=2, column=0, sticky=tk.W)
uso_vehiculo_combobox = ttk.Combobox(marco_principal, textvariable=uso_vehiculo_var, values=["usado", "nuevo"])
uso_vehiculo_combobox.grid(row=2, column=1, sticky=tk.W, pady=5)

# Etiqueta y lista desplegable para el tipo de vehículo
ttk.Label(marco_principal, text="Seleccione el tipo de vehículo:").grid(row=3, column=0, sticky=tk.W)
tipo_vehiculo_combobox = ttk.Combobox(marco_principal, textvariable=tipo_vehiculo_var, values=["particular", "comercial"])
tipo_vehiculo_combobox.grid(row=3, column=1, sticky=tk.W, pady=5)

# Etiqueta y barra desplegable para el rubro
ttk.Label(marco_principal, text="Seleccionar Rubro:").grid(row=4, column=0, sticky=tk.W)
rubro_var = tk.StringVar()
rubro_combobox = ttk.Combobox(marco_principal, textvariable=rubro_var, values=["No aplica","Contenedores", "Materiales de Construccion" , "Transporte rubro propio de la empresa",
                                                                                "Telecomunicaciones", "Transporte personal: Empresa/Institucion", "Turismo", "Taxi",
                                                                                "Transporte Escolar", "Transporte publico de pasajeros", "Transporte privado de pasajeros",
                                                                                "Seguridad Publica"])
rubro_combobox.grid(row=4, column=1, sticky=tk.W, pady=5)

# Etiqueta y entrada para la patente
ttk.Label(marco_principal, text="Ingrese la patente:").grid(row=5, column=0, sticky=tk.W)
patente_entry = ttk.Entry(marco_principal, textvariable=patente_var)
patente_entry.grid(row=5, column=1, sticky=tk.W, pady=5)

# Etiqueta y entrada para el año
ttk.Label(marco_principal, text="Ingrese el Año:").grid(row=6, column=0, sticky=tk.W)
ano_entry = ttk.Entry(marco_principal, textvariable=ano_var)
ano_entry.grid(row=6, column=1, sticky=tk.W, pady=5)

# Etiqueta y lista desplegable para el tipo de persona
ttk.Label(marco_principal, text="Seleccione el tipo de persona:").grid(row=7, column=0, sticky=tk.W)
tipo_persona_combobox = ttk.Combobox(marco_principal, textvariable=tipo_persona_var, values=["natural", "juridica"])
tipo_persona_combobox.grid(row=7, column=1, sticky=tk.W, pady=5)

# Etiqueta y entrada para el RUT
ttk.Label(marco_principal, text="Ingrese el RUT:").grid(row=8, column=0, sticky=tk.W)
rut_entry = ttk.Entry(marco_principal)
rut_entry.grid(row=8, column=1, sticky=tk.W, pady=5)

# Etiqueta y entrada para el nombre del contratante
ttk.Label(marco_principal, text="Ingrese el nombre del contratante:").grid(row=9, column=0, sticky=tk.W)
nombre_contratante_entry = ttk.Entry(marco_principal)
nombre_contratante_entry.grid(row=9, column=1, sticky=tk.W, pady=5)

# Etiqueta y entrada para el apellido del contratante
ttk.Label(marco_principal, text="Ingrese el apellido del contratante:").grid(row=10, column=0, sticky=tk.W)
apellido_contratante_entry = ttk.Entry(marco_principal)
apellido_contratante_entry.grid(row=10, column=1, sticky=tk.W, pady=5)


# Etiqueta y lista desplegable para el tipo de vehículo
ttk.Label(marco_principal, text="Estilo vehiculo:").grid(row=11, column=0, sticky=tk.W)
tipo_vehiculo_combobox = ttk.Combobox(marco_principal, textvariable=estilo_var, values=["JEEP", "STATION WAGON", "SEDAN", "AUTOMOVIL","CAMIONETA","FURGON"])
tipo_vehiculo_combobox.grid(row=11, column=1, sticky=tk.W, pady=5)

# Convertir el conjunto a una lista y ordenarla alfabéticamente
lista_comunas = sorted(list(comunas))


#Comuna Etiqueta y lista desplegable para el tipo de vehículo
# Etiqueta y lista desplegable para la comuna
ttk.Label(marco_principal, text="Comuna:").grid(row=12, column=0, sticky=tk.W)
comuna_combobox = ttk.Combobox(marco_principal, textvariable=comuna_var, values=lista_comunas)
comuna_combobox.grid(row=12, column=1, sticky=tk.W, pady=5)

# Botón para obtener los datos
ttk.Button(marco_principal, text="Obtener Datos", command=obtener_datos).grid(row=13, column=0, columnspan=2, pady=10)

# Iniciar el bucle principal
ventana.mainloop()
