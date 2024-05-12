from selenium.common.exceptions import (TimeoutException,ElementClickInterceptedException,)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from difflib import SequenceMatcher, get_close_matches
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import logging, sys, time, traceback
from selenium import webdriver
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd
import json
import os


#Definiciones
def seleccionar_opcion_similar(valor_manual, opciones):
    mejor_coincidencia = get_close_matches(valor_manual, opciones, n=1, cutoff=0.6)
    return mejor_coincidencia[0] if mejor_coincidencia else None

def encontrar_mejor_coincidencia(valor_deseado, opciones):
        mejor_coincidencia = max(opciones, key=lambda opcion: SequenceMatcher(None, valor_deseado, opcion.text.strip()).ratio())
        return mejor_coincidencia.text.strip()

def esperar_elemento(driver, locator, *numeros_condiciones, max_intentos=5):
    condiciones = {
        1: EC.presence_of_element_located,
        2: EC.visibility_of_element_located,
        3: EC.element_to_be_clickable
    }
    condiciones_espera = [condiciones[num] for num in numeros_condiciones]
    intentos = 0
    elemento = None
    while intentos < max_intentos:
        try:
            for condicion in condiciones_espera:
                elemento = WebDriverWait(driver, 10).until(condicion(locator))
                if elemento:
                    print(f"Elemento {locator} encontrado.")
                    return elemento
        except TimeoutException:
            print(f"Elemento {locator} no encontrado. Intento {intentos + 1}/{max_intentos}. Selector: {locator}")
            intentos += 1
    return elemento  # Devuelve None si el elemento no se encuentra después de varios intentos
    
def hacer_clic_elemento_con_reintentos(driver, elemento, intentos_maximos=3):
    intentos = 0
    while intentos < intentos_maximos:
        try:
            elemento.click()
            print("Clic en el elemento realizado correctamente.")
            return True  # Se hizo clic exitosamente, salimos del bucle
        except ElementClickInterceptedException:
            print("Error: ElementClickInterceptedException. Volviendo a intentar...")
            intentos += 1
    print(f"No se pudo hacer click en el elemento {elemento} después de {intentos_maximos} intentos.")
    return False  # No se pudo hacer clic después de los intentos máximos

def hacer_clic_elemento_con_reintentos_js(driver, elemento, intentos_maximos=3):
    intentos = 0
    while intentos < intentos_maximos:
        try:
            driver.execute_script("arguments[0].click();", elemento)
            print("Clic en el elemento realizado correctamente.")
            return True  # Se hizo clic exitosamente, salimos del bucle
        except ElementClickInterceptedException:
            print("Error: ElementClickInterceptedException. Volviendo a intentar...")
            intentos += 1
    print(f"No se pudo hacer click en el elemento {elemento} después de {intentos_maximos} intentos.")
    return False  # No se pudo hacer clic después de los intentos máximos

def esperar_pagina_cargada(driver):
    try:
        # Espera a que el elemento overlay desaparezca
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, 'overlay'))
        )
        print("El overlay ha desaparecido")
    except Exception as e:
        print("Error al esperar el overlay desaparecido:", e)

# Obtener el directorio actual (donde se encuentra el script)
directorio_actual = os.path.dirname(os.path.abspath(__file__))

# Configurar el registro
log_file_path = os.path.join(directorio_actual, '..', 'Reportes', 'reporte_reale.txt')
logging.basicConfig(filename=log_file_path, level=logging.INFO)

# Redirigir stdout y stderr a un archivo de registro
sys.stdout = open(log_file_path, 'w')
sys.stderr = open(log_file_path, 'w')

try:
 #Ruta de chromedriver
    service = Service(executable_path=os.path.join(directorio_actual, '..', 'chromedriver.exe')) 
    driver = webdriver.Chrome(service=service)

 #Datos
    datos_file_path = os.path.join(directorio_actual, '..', 'Datos','datos_reale.txt') 
    with open(datos_file_path, 'r', encoding='utf-8') as file:
            datos_content = file.read()
            datos = eval(datos_content)
    print("____________________________________________________________________________________________________")
    print(datos)
    
 #Registro de información
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    informe = f"Informe - Cliente: {datos['nombre_contratante']}, Apellido: {datos['apellido_contratante']}, " \
                f"Patente: {datos['patente']}, Fecha: {fecha_actual}"
    print(informe)
    print("____________________________________________________________________________________________________")
 
 #Página Login
    driver.get("https://apps4.realechile.cl/portalCorredores/login")
    driver.maximize_window()

    # Construir la ruta relativa al archivo credenciales.json
    ruta_credenciales = os.path.join(directorio_actual, '..','credenciales.json')
    # Leer el archivo JSON desde la ruta relativa
    with open(ruta_credenciales, 'r') as file:
        credentials = json.load(file)
    # Acceder a los datos
    rut = credentials['rut_reale']
    password = credentials['password_reale']
    email = credentials["email"]

    RUT_REALE_locator = (By.ID, "username")
    RUT_REALE = esperar_elemento(driver, RUT_REALE_locator, 1, 2 ,3, max_intentos=15)
    RUT_REALE.send_keys(rut)

    PASS_REALE_locator = (By.ID, "password")
    PASS_REALE = esperar_elemento(driver, PASS_REALE_locator, 1, 2 ,3, max_intentos=15)
    PASS_REALE.send_keys(password)
    PASS_REALE.send_keys(Keys.ENTER)

 #Cotizador Liviano
    driver.get(f"https://cotizador.realechile.cl/index/{rut}")
    locator_liviano = (By.XPATH, '//*[contains(text(), "liviano")]')
    ELEMENTO_LIVIANO = esperar_elemento(driver, locator_liviano, 1,2,3)
    hacer_clic_elemento_con_reintentos(driver, ELEMENTO_LIVIANO)  

 #Persona Natural o Jurídica
 #Persona Natural
    if datos["tipo_persona"] == "natural":
        tipo_persona_locator = (By.ID, "tipoPersona")
        TIPO_PERSONA = esperar_elemento(driver, tipo_persona_locator, 1, 2, 3)
        hacer_clic_elemento_con_reintentos(driver, TIPO_PERSONA)
            
        elemento_opcion_locator = (By.XPATH, '//option[@value="1: 41"]')
        elemento_opcion = esperar_elemento(driver, elemento_opcion_locator, 1, 2)
        Select(TIPO_PERSONA).select_by_value("1: 41")
        print("Persona : Natural")
        print("________________________________________________________")

        esperar_pagina_cargada(driver)
 #Rut
        rut_contratante_locator = (By.ID, "rut")
        RUT_CONTRATANTE = esperar_elemento(driver, rut_contratante_locator, 1, 2, 3)
        RUT_CONTRATANTE.send_keys(datos["rut"])
        print(f"Rut: {datos['rut']}")
        print("________________________________________________________")

        esperar_pagina_cargada(driver)

 #E-Mail
        EMAIL_locator = (By.ID,"email")
        EMAIL = esperar_elemento(driver, EMAIL_locator, 1,2,3)
        hacer_clic_elemento_con_reintentos(driver, EMAIL)

        esperar_pagina_cargada(driver)
        
 #Nombre contratante
        input_nombres_locator = (By.ID, "firstName")
        input_nombres = esperar_elemento(driver, input_nombres_locator, 1, 2, max_intentos=5)
        if input_nombres.is_enabled():
            input_nombres.send_keys(datos["nombre_contratante"])
            print(f"Nombre contratante : {datos['nombre_contratante']} ")
            print("________________________________________________________")
        else:
            print("El campo 'nombre' estaba autocompletado")
            print("________________________________________________________")
            pass 
        esperar_pagina_cargada(driver)
            
 #Apellido contratante
        input_apellidos_locator = (By.ID, "lastName")
        input_apellidos = esperar_elemento(driver, input_apellidos_locator, 1, 2, max_intentos=5)
        if input_apellidos.is_enabled():
            input_apellidos.send_keys(datos["apellido_contratante"])
            print(f"Apellido contratante : {datos['apellido_contratante']} ")
            print("________________________________________________________")
        else:
            print("El campo 'apellido' estaba autocompletado")
            print("________________________________________________________")
            pass

        esperar_pagina_cargada(driver)
 #Persona Jurídica
    else:
        TIPO_PERSONA_locator = (By.ID, "tipoPersona")
        TIPO_PERSONA = esperar_elemento(driver, TIPO_PERSONA_locator, 1, 2, max_intentos=5)
        elemento_xpath_locator = (By.XPATH, '//option[@value="1: 41"]')
        elemento_xpath = esperar_elemento(driver, elemento_xpath_locator, 1, 2, max_intentos=5)
        Select(TIPO_PERSONA).select_by_value("2: 42")
        print("Tipo de persona : Juridica")
        print("________________________________________________________")

        esperar_pagina_cargada(driver)

 #Rut
        RUT_CONTRATANTE_locator = (By.ID, "rut")
        RUT_CONTRATANTE = esperar_elemento(driver, RUT_CONTRATANTE_locator, 1, 2, max_intentos=5)
        if RUT_CONTRATANTE.is_enabled():
            RUT_CONTRATANTE.send_keys(datos["rut"])
            print(f"Rut : {datos['rut']}")

            print("________________________________________________________")
        else:
            print("No se pudo rellenar el campo 'Rut'")
            print("________________________________________________________")
            pass

        esperar_pagina_cargada(driver)

    # Simula un clic en la página
    action = ActionChains(driver)
    action.click().perform()

    esperar_pagina_cargada(driver)

    #E-Mail
    EMAIL_locator = (By.ID, "email")
    EMAIL = esperar_elemento(driver, EMAIL_locator, 1,2 )
    EMAIL.clear()
    EMAIL.send_keys(email)

    esperar_pagina_cargada(driver)

 #Comuna
    comuna_locator = (By.ID, "comuna")
    COMUNA = esperar_elemento(driver, comuna_locator, 1, 2, 3, max_intentos=5)
    select = Select(COMUNA)
    opciones = select.options
    texto_a_seleccionar = datos["comuna"]
    select.select_by_visible_text(texto_a_seleccionar)
    print(f"Se selecciono comuna {datos['comuna']}")
    print("________________________________________________________")

    esperar_pagina_cargada(driver)
        
 #Continuar
    SUBMIT_locator = (By.NAME, "submit")
    SUBMIT = esperar_elemento(driver, SUBMIT_locator, 1, 2,3)
    hacer_clic_elemento_con_reintentos(driver, SUBMIT)
        
    esperar_pagina_cargada(driver)

 #Auto Nuevo
    if datos["uso_vehiculo"] == "nuevo":
        USO_VEHICULO_locator = (By.ID, "nuevoUsado")
        USO_VEHICULO = esperar_elemento(driver, USO_VEHICULO_locator, 1, 2, max_intentos=5)
        if USO_VEHICULO and USO_VEHICULO.is_enabled():
            hacer_clic_elemento_con_reintentos(driver, USO_VEHICULO)
            print("Clic en el elemento USO_VEHICULO realizado correctamente.")
        else:
            print("No se pudo encontrar el elemento USO_VEHICULO o no está habilitado para hacer clic.")
        select = Select(USO_VEHICULO)
        select.select_by_value("1: 1")
        print("Uso vehiculo = Nuevo")
        print("________________________________________________________")

        esperar_pagina_cargada(driver)     

 #Año Vehiculo
        ANO_VEHICULO_locator = (By.ID, "anio")
        ANO_VEHICULO = esperar_elemento(driver, ANO_VEHICULO_locator, 1, 2,  3)
        if ANO_VEHICULO:
            hacer_clic_elemento_con_reintentos(driver, ANO_VEHICULO)
            print("Clic en el elemento ANO_VEHICULO realizado correctamente.")
        else:
            print("No se pudo encontrar el elemento ANO_VEHICULO.")
        
        if ANO_VEHICULO.is_enabled():
            select_ano = Select(ANO_VEHICULO)
            select_ano.select_by_visible_text(datos["ano"])
            print("Se selecciono el año:", datos["ano"])
        else:
            print("Seleccion de año no está habilitada. No se selecciono ningún año.") 

        esperar_pagina_cargada(driver)

        time.sleep(3)
        
 #Marca  
        marca_locator = (By.ID, "marca")
        marca_elemento = esperar_elemento(driver, marca_locator, 1, 2, 3)
        if marca_elemento and marca_elemento.is_enabled():
            hacer_clic_elemento_con_reintentos(driver, marca_elemento)
            print("Clic en 'marca' realizado correctamente.")
            # LISTA Y MEJOR COINCIDENCIA
            valor_deseado_marca = str(datos["marca"])
            try:
                Select(marca_elemento).select_by_visible_text(valor_deseado_marca)
                print(f"Se escogio {datos['marca']} sin printear la lista de opciones ")
                print("_____________________________________________________________________")
            except:
                opciones_marca_elemento = Select(marca_elemento).options
                print("Lista de opciones de marca:")
                for opcion in opciones_marca_elemento:
                    print(opcion.text.strip())
                mejor_coincidencia_marca = encontrar_mejor_coincidencia(valor_deseado_marca, opciones_marca_elemento)
                print(f"\nMejor coincidencia para '{valor_deseado_marca}': {mejor_coincidencia_marca}")
                Select(marca_elemento).select_by_visible_text(mejor_coincidencia_marca)
                print("_____________________________________________________________________")
        else:
            print(f"No se pudo encontrar {marca_locator} o no está habilitado para hacer clic.")
            pass     

        esperar_pagina_cargada(driver)
        time.sleep(3)
       
 #Modelo
        modelo_locator = (By.ID, 'modelo')
        modelo_elemento = esperar_elemento(driver, modelo_locator, 1, 2, 3)
        if modelo_elemento:
            print(f"El elemento {modelo_locator} está presente en la página.")
        else:
            print(f"No se pudo encontrar el elemento {modelo_locator}.")
        if modelo_elemento.is_enabled():
                modelo_deseado = str(datos["modelo"])
                hacer_clic_elemento_con_reintentos(driver, modelo_elemento)
                try:
                    Select(modelo_elemento).select_by_visible_text(modelo_deseado)
                    print(f"Se escogio {datos['modelo']} sin printear la lista de opciones ")
                    print("_____________________________________________________________________")
                
                except:
                    opciones_modelo_elemento = Select(modelo_elemento).options
                    print("Lista de opciones de modelo:")
                    for opcion in opciones_modelo_elemento:
                        print(opcion.text.strip())  
                    
                    mejor_coincidencia_modelo = encontrar_mejor_coincidencia(modelo_deseado, opciones_modelo_elemento)

                    print(f"Mejor coincidencia para '{modelo_deseado}': {mejor_coincidencia_modelo}")
                    print("_____________________________________________________________________")
                    marca_elemento = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.ID, "modelo"))
                    )
                    Select(marca_elemento).select_by_visible_text(mejor_coincidencia_modelo)
        else:
            pass

        esperar_pagina_cargada(driver)

          # Intenta encontrar y seleccionar la versión del modelo
        try:
            version_select_locator = (By.ID, "version")
            VERSION_SELECT = esperar_elemento(driver, version_select_locator,1)

            if VERSION_SELECT.is_enabled():
                hacer_clic_elemento_con_reintentos(driver, VERSION_SELECT)
                select = Select(VERSION_SELECT)
                opciones = [option.text.strip() for option in select.options]

                if not opciones:
                    print("No se encontraron opciones en la lista de versiones.")
                else:
                    print("Lista de opciones:")
                    for opcion in opciones:
                        print(opcion)

                    # Selecciona la primera opción de la lista
                    primera_opcion = opciones[1]
                    select.select_by_visible_text(primera_opcion)
                    print(f"Se seleccionó la primera opción: {primera_opcion}")
        except Exception as e:
            # Maneja la excepción si el elemento no está presente en la página
            print("No se requiere seleccionar versión")
            print(f"Error: {e}")
        
 #Particular
        if datos["tipo_vehiculo"] == "particular":
            tipo_vehiculo_locator = (By.ID, "uso")
            TIPO_VEHICULO = esperar_elemento(driver, tipo_vehiculo_locator,1,2)
            Select(TIPO_VEHICULO).select_by_value("1: Object")
            print("Vehiculo : Particular")
            print("_____________________________________________________________________")

 #Comercial
        else:
            tipo_vehiculo_locator = (By.ID, "uso")
            TIPO_VEHICULO = esperar_elemento(driver, tipo_vehiculo_locator,1,2)
            Select(TIPO_VEHICULO).select_by_value("2: Object")
            print("Vehiculo : Comercial")
            print("_____________________________________________________________________")

        esperar_pagina_cargada(driver)
    
 #Tipo combustible
        tipo_combustible_locator = (By.ID, "tipoCombustible")
        TIPO_COMBUSTIBLE = esperar_elemento(driver, tipo_combustible_locator,1,2)
        Select(TIPO_COMBUSTIBLE).select_by_value("1: 9")

        esperar_pagina_cargada(driver)

 #Km al año
        km_locator = (By.ID, "kmAlAnio")
        KM_X_ANO = esperar_elemento(driver, km_locator,1,2)
        Select(KM_X_ANO).select_by_value("1: 16")

        esperar_pagina_cargada(driver)

 #Compañia anterior
        try:
            compania_anterior_locator = (By.ID, "companiaAnterior")
            COMPANIA_ANTERIOR = esperar_elemento(driver, compania_anterior_locator,1,2)
            if COMPANIA_ANTERIOR.is_enabled:
                Select(COMPANIA_ANTERIOR).select_by_value("1: 14")  
            else:
                pass
        except TimeoutException:
            print("El elemento COMPANIA_ANTERIOR no fue encontrado a tiempo.")
            print("_____________________________________________________________________")

        esperar_pagina_cargada(driver)
          
 #Auto usado
    else:
        uso_vehiculo_locator = (By.ID, "nuevoUsado")
        USO_VEHICULO = esperar_elemento(driver, uso_vehiculo_locator, 1,2,3)
        select = Select(USO_VEHICULO)
        select.select_by_value("2: 0")
        print("Uso vehiculo = Usado")
        print("________________________________________________________")

        esperar_pagina_cargada(driver)

 #Patente
        patente_locator = (By.ID,"patente")
        PATENTE_VEHICULO = esperar_elemento(driver, patente_locator,1,2)
        PATENTE_VEHICULO.send_keys(datos["patente"])
        print(f"Patente = {datos['patente']}")
        print("________________________________________________________")

        esperar_pagina_cargada(driver)


 #Año vehiculo
        ano_vehiculo_locator = (By.ID, "anio")
        ANO_VEHICULO = esperar_elemento(driver, ano_vehiculo_locator,1,2,3)
        hacer_clic_elemento_con_reintentos(driver, ANO_VEHICULO)

        esperar_pagina_cargada(driver)


        if ANO_VEHICULO.is_enabled():
            select_ano = Select(ANO_VEHICULO)
            select_ano.select_by_visible_text(datos["ano"])
            print("Se selecciono el año:", datos["ano"])
            print("_____________________________________________________________________")
        else:
            print("Seleccion de año no está habilitada. No se seleccionará ningún año.") 
            print("_____________________________________________________________________")
        
        esperar_pagina_cargada(driver)

        
 #Marca vehiculo
        marca_locator = (By.ID, "marca")
        MARCA = esperar_elemento(driver, marca_locator,1,2)
        if MARCA.is_enabled():
            valor_deseado_marca = str(datos["marca"])
            hacer_clic_elemento_con_reintentos(driver, MARCA)
            time.sleep(2)
            # LISTA Y MEJOR COINCIDENCIA
            try:
                Select(MARCA).select_by_visible_text(valor_deseado_marca)
                print(f"Se escogio{datos['marca']} sin printear la lista de opciones ")
                print("_____________________________________________________________________")
                
            except:
                opciones_marca_elemento = Select(MARCA).options
                print("Lista de opciones de marca:")
                for opcion in opciones_marca_elemento:
                    print(opcion.text.strip())
                mejor_coincidencia_marca = encontrar_mejor_coincidencia(valor_deseado_marca, opciones_marca_elemento)
                print(f"\nMejor coincidencia para '{valor_deseado_marca}': {mejor_coincidencia_marca}")
                Select(MARCA).select_by_visible_text(mejor_coincidencia_marca)
                print("_____________________________________________________________________")
        else:
            pass
       
        esperar_pagina_cargada(driver)
      
 #Modelo vehiculo
        modelo_locator = (By.ID, "modelo")
        MODELO = esperar_elemento(driver, modelo_locator, 1,2)
        time.sleep(2)
        if MODELO.is_enabled():
            valor_deseado_modelo = str(datos["modelo"])
            hacer_clic_elemento_con_reintentos(driver, MODELO)
            # LISTA Y MEJOR MATCH
            try:
                Select(MODELO).select_by_visible_text(valor_deseado_modelo)
                print(f"Se escogio{datos['modelo']} sin printear la lista de opciones ")
                print("_____________________________________________________________________")

            except:
                opciones_modelo_elemento = Select(MODELO).options
                print("Lista de opciones de modelo:")
                for opcion in opciones_modelo_elemento:
                    print(opcion.text.strip())
                mejor_coincidencia_modelo = encontrar_mejor_coincidencia(valor_deseado_modelo, opciones_modelo_elemento)
                print(f"\nMejor coincidencia para '{valor_deseado_modelo}': {mejor_coincidencia_modelo}")
                Select(MODELO).select_by_visible_text(mejor_coincidencia_modelo)    
                print("_____________________________________________________________________")  
        else:
            pass
        
        esperar_pagina_cargada(driver)

 # Intenta encontrar y seleccionar la versión del modelo
        try:
            version_select_locator = (By.ID, "version")
            VERSION_SELECT = esperar_elemento(driver, version_select_locator,1)

            if VERSION_SELECT.is_enabled():
                hacer_clic_elemento_con_reintentos(driver, VERSION_SELECT)
                select = Select(VERSION_SELECT)
                opciones = [option.text.strip() for option in select.options]

                if not opciones:
                    print("No se encontraron opciones en la lista de versiones.")
                else:
                    print("Lista de opciones:")
                    for opcion in opciones:
                        print(opcion)

                    # Selecciona la primera opción de la lista
                    primera_opcion = opciones[1]
                    select.select_by_visible_text(primera_opcion)
                    print(f"Se seleccionó la primera opción: {primera_opcion}")
        except Exception as e:
            # Maneja la excepción si el elemento no está presente en la página
            print("No se requiere seleccionar versión")
            print(f"Error: {e}")
                               
 #Particular
        if datos["tipo_vehiculo"] == "particular":
            tipo_vehiculo_locator = (By.ID, "uso")
            TIPO_VEHICULO = esperar_elemento(driver, tipo_vehiculo_locator,1,2)
            Select(TIPO_VEHICULO).select_by_value("1: Object")
            print("Vehiculo : Particular")
            print("_____________________________________________________________________")

 #Comercial    
        else:
            tipo_vehiculo_locator = (By.ID, "uso")
            TIPO_VEHICULO = esperar_elemento(driver, tipo_vehiculo_locator,1,2)
            Select(TIPO_VEHICULO).select_by_value("2: Object")
            print("Vehiculo : Comercial")
            print("_____________________________________________________________________")

        esperar_pagina_cargada(driver)

 #Tipo combustible
        tipo_combustible_locator = (By.ID, "tipoCombustible")
        TIPO_COMBUSTIBLE = esperar_elemento(driver, tipo_combustible_locator,1,2)
        Select(TIPO_COMBUSTIBLE).select_by_value("1: 9")

        esperar_pagina_cargada(driver)

 #Km al año
        km_locator = (By.ID, "kmAlAnio")
        KM_X_ANO = esperar_elemento(driver, km_locator,1,2)
        Select(KM_X_ANO).select_by_value("1: 16")

        esperar_pagina_cargada(driver)

 #Compañia anterior
        try:
            compania_anterior_locator = (By.ID, "companiaAnterior")
            COMPANIA_ANTERIOR = esperar_elemento(driver, compania_anterior_locator,1,2)
            if COMPANIA_ANTERIOR.is_enabled:
                Select(COMPANIA_ANTERIOR).select_by_value("1: 14")  
            else:
                pass
        except TimeoutException:
            print("El elemento COMPANIA_ANTERIOR no fue encontrado a tiempo.")
            print("_____________________________________________________________________")

        esperar_pagina_cargada(driver)
          
#Botón continuar
    fa_icon_element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//button[@name="submit"]/fa-icon[@class="ng-fa-icon"]'))
    )
    driver.execute_script("arguments[0].click();", fa_icon_element)
    time.sleep(5)

 #Scrollear página
    driver.execute_script("window.scrollTo(0, window.scrollY + 500)")

 #Pantallazo
    timestamp = time.strftime("%Y%m%d_%H%M%S")  # Agrega un timestamp para hacer el nombre único
    cliente_nombre = datos['nombre_contratante']  # Usa el nombre del cliente como parte del nombre del archivo 
    screenshot_path = os.path.join(directorio_actual, '..', 'Imagenes',f'captura_{cliente_nombre}_{timestamp}_reale.png') 
 #Guardar pantallazo
    driver.save_screenshot(screenshot_path)

except Exception as e:
    # Registrar cualquier excepción que pueda ocurrir
    print(f"Error: {str(e)}")
    logging.error(f"Error: {str(e)}")
    print(traceback.format_exc())  # Esto imprimirá el rastreo completo de la excepción
    logging.error(traceback.format_exc())

sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__

driver.quit()


