from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from difflib import get_close_matches
from difflib import SequenceMatcher
from unidecode import unidecode
from selenium import webdriver
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd
import traceback
import logging
import json
import time
import sys
import os

#Definiciones 
def esperar_carga_barra(driver):
    try:
        WebDriverWait(driver, 75).until(
            EC.text_to_be_present_in_element((By.CLASS_NAME, "percentBarLoaderNum"), "100")
        )
        print("La barra de carga se ha cargado completamente.")
        return True
    except Exception as e:
        print(f"Error al esperar la carga de la barra: {str(e)}")
        return False
    
def seleccionar_opcion_similar(valor_manual, opciones):
        mejor_coincidencia = get_close_matches(valor_manual, opciones, n=1, cutoff=0.6)
        return mejor_coincidencia[0] if mejor_coincidencia else None

def encontrar_mejor_coincidencia(valor_deseado, opciones):
        mejor_coincidencia = max(opciones, key=lambda opcion: SequenceMatcher(None, valor_deseado, opcion.text.strip()).ratio())
        return mejor_coincidencia.text.strip()

def esperar_elemento(driver, locator, *numeros_condiciones, max_intentos=5):
    # Define las condiciones de espera y sus códigos
    condiciones = {
        1: EC.presence_of_element_located,
        2: EC.visibility_of_element_located,
        3: EC.element_to_be_clickable,
        4: EC.element_located_to_be_selected,
        5: EC.visibility_of_all_elements_located
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

def esperar_elemento_interactuable(driver, locator, max_intentos=5, timeout=10):
    intentos = 0
    while intentos < max_intentos:
        try:
            elemento = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))
            print("Elemento interactuable encontrado.")
            return elemento
        except TimeoutException:
            print(f"El elemento interactuable no se encontró en el intento {intentos + 1}/{max_intentos}")
            intentos += 1
    print(f"El elemento interactuable no se encontró después de {max_intentos} intentos.")
    return None

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

def esperar_carga_pagina(driver, intentos=0, max_intentos=5):
    while intentos < max_intentos:
        try:
            spinner_invisible = WebDriverWait(driver, 10).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "p-progress-spinner-circle"))
            )
            print("El spinner 'p-progress-spinner-circle' ha desaparecido, la página ha cargado completamente.")
            return True  # La carga fue exitosa
        except TimeoutException:
            print(f"Tiempo de espera agotado. El spinner 'p-progress-spinner-circle' aún está presente o la página no ha cargado completamente. Intento {intentos + 1}/{max_intentos}")
            intentos += 1
            time.sleep(2)  # Espera un poco antes de intentar nuevamente
    print(f"No se pudo cargar completamente la página después de {max_intentos} intentos.")
    return False  # La carga falló

# Directorio actual:
directorio_actual = os.path.dirname(os.path.abspath(__file__))

# Configurar el registro
log_file_path = os.path.join(directorio_actual, '..', 'Reportes','reporte_ans.txt')
logging.basicConfig(filename=log_file_path, level=logging.INFO )
sys.stdout = open(log_file_path, 'w')
sys.stderr = open(log_file_path, 'w')

try:
 # Ruta de chromedriver
    ruta_chromedriver = os.path.join(directorio_actual, '..', 'chromedriver.exe')   
    service = Service(executable_path=ruta_chromedriver)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service=service, options=chrome_options)
                              
 # Datos  
    datos_file_path = os.path.join(directorio_actual, '..', 'Datos','datos_ans.txt') 
    with open(datos_file_path, 'r', encoding='utf-8') as file:
        datos_content = file.read()
        datos = eval(datos_content)

    #Print datos
    print("____________________________________________________________________________________________________")
    print(datos)
    print("____________________________________________________________________________________________________")

# Registro de información
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    informe = f"Informe - Cliente: {datos['nombre_contratante']}, Apellido: {datos['apellido_contratante']}, " \
            f"Patente: {datos['patente']}, Fecha: {fecha_actual}"
    print(informe)
    print("____________________________________________________________________________________________________")

 
 # Credenciales
    ruta_credenciales = os.path.join(directorio_actual, '..','credenciales.json')
    # Leer el archivo JSON desde la ruta relativa
    with open(ruta_credenciales, 'r') as file:
        credentials = json.load(file)
    # Acceder a los datos
    email = credentials['email']
    password = credentials['password_ans']
    #.. Página login
    driver.get("https://www.ant.cl/portal/account/login")
    driver.maximize_window()
    #.. Botón Login
    BOTON_LOGIN_locator = (By.ID, "login-login-button")
    BOTON_LOGIN = esperar_elemento(driver, BOTON_LOGIN_locator, 1, 3)
    hacer_clic_elemento_con_reintentos(driver, BOTON_LOGIN)
    #.. Rut
    RUT_ANS_locator = (By.ID, "email")
    RUT_ANS = esperar_elemento(driver, RUT_ANS_locator, 1, 3)
    RUT_ANS.send_keys(Keys.CONTROL + "a")
    RUT_ANS.send_keys(email)
    #.. Pass
    PASS_ANS_locator = (By.ID, "password")
    PASS_ANS = esperar_elemento(driver, PASS_ANS_locator, 1, 3)
    PASS_ANS.send_keys(Keys.CONTROL + "a")
    PASS_ANS.send_keys(password)
    PASS_ANS.send_keys(Keys.ENTER)
    #_________________________________________________________________________________________________#
   
    esperar_carga_pagina(driver)

 # Vehiculos livianos
    elemento_vehiculos_livianos_locator = (By.XPATH, '//span[contains(text(), "Vehículos Livianos")]')
    BOTON_VEHICULO_LIVIANO = esperar_elemento(driver, elemento_vehiculos_livianos_locator,1,2,3)
    hacer_clic_elemento_con_reintentos_js(driver, BOTON_VEHICULO_LIVIANO)
    
    #.. Cambiar iframe
    iframe_locator = (By.ID, "iframe-render")
    IFRAME = esperar_elemento(driver, iframe_locator,1,2)
    driver.switch_to.frame(IFRAME)

    esperar_carga_pagina(driver)
    
 #Tipo de persona
    TIPO_PERSONA_locator = (By.ID, "PerAsegurado_PersonalidadJuridicaID")
    TIPO_PERSONA = esperar_elemento(driver, TIPO_PERSONA_locator,1,2,4,5)
    select_tipo_persona = Select(TIPO_PERSONA)

    time.sleep(2)

 # Natural
    if datos["tipo_persona"] == "natural":
        select_tipo_persona.select_by_value("100")
 # Juridica
    else:
        select_tipo_persona.select_by_value("110")
    
 # Rut contratante
    RUT_CONTRATANTE_locator = (By.ID, "PerAsegurado_Identificacion")
    RUT_CONTRATANTE = esperar_elemento(driver, RUT_CONTRATANTE_locator,1,3)
    elemento_rut_contratante = esperar_elemento_interactuable(driver, (By.ID, "PerAsegurado_Identificacion"))
    if elemento_rut_contratante:
        elemento_rut_contratante.send_keys(datos["rut"])
    else:
        print("El elemento RUT_CONTRATANTE no es interactuable.") 

    if datos["tipo_persona"] == "natural":

 # Nombre contratante
        nombre_persona_locator = (By.ID, "PerAsegurado_Nombres")
        NOMBRE_PERSONA = esperar_elemento(driver, nombre_persona_locator, 1,2,3 )
        NOMBRE_PERSONA.send_keys(datos["nombre_contratante"])
        
        apellido_persona_p_locator = (By.ID, "PerAsegurado_ApellidoPaterno")
        APELLIDO_PERSONA_P = esperar_elemento(driver, apellido_persona_p_locator, 1,2,3)
        APELLIDO_PERSONA_P.send_keys(datos["apellido_contratante"])

 # Apellido contratante
        apellido_persona_m_locator = (By.ID, "PerAsegurado_ApellidoMaterno")
        APELLIDO_PERSONA_M = esperar_elemento(driver, apellido_persona_m_locator,1,2,3)
        APELLIDO_PERSONA_M.send_keys("A")
   
    else:
        razon_social_locator = (By.ID, "PerAsegurado_RazonSocial")
        RAZON_SOCIAL = esperar_elemento(driver, razon_social_locator,1,2,3)
        RAZON_SOCIAL.send_keys(datos["nombre_contratante"]) 

 # Marca Vehiculo
    MARCA_VEHICULO_locator = (By.ID, "MarcaVehiculos")
    MARCA_VEHICULO = esperar_elemento(driver, MARCA_VEHICULO_locator, 1,2,3,4,5)
    hacer_clic_elemento_con_reintentos(driver ,MARCA_VEHICULO)
    select_marca_vehiculo = Select(MARCA_VEHICULO)
    MARCA_DESEADA = str(datos["marca"])
    try:
        # .. Opcion deseada
        select_marca_vehiculo.select_by_visible_text(MARCA_DESEADA)
        print(f"Se seleccionó la marca deseada :{MARCA_DESEADA} sin printear la lista de opciones")
        print("____________________________________________________________________________________________________")

    except:
       # Imprimir todas las opciones disponibles
        print("Opciones disponibles:")
        for opcion in select_marca_vehiculo.options:
            print(opcion.text)
            print("____________________________________________________________________________________________________")
            
        opciones_disponibles = [opcion.text for opcion in select_marca_vehiculo.options]
        mejor_coincidencia = max(opciones_disponibles, key=lambda opcion: SequenceMatcher(None, MARCA_DESEADA, opcion).ratio())

        select_marca_vehiculo.select_by_visible_text(mejor_coincidencia)

        print(f"Se selecciona la mejor coincidencia para '{MARCA_DESEADA}': {mejor_coincidencia}")
        print("____________________________________________________________________________________________________")
      
 # Modelo vehiculo
    select_element_modelo_locator = (By.ID, "ModeloVehiculos")
    select_element = esperar_elemento(driver, select_element_modelo_locator, 1,2,3,4,5)
    hacer_clic_elemento_con_reintentos(driver ,select_element)
    select_modelo = Select(select_element)
    dato_deseado = datos["modelo"]
    try:
        select_modelo.select_by_visible_text(dato_deseado)
        print(f"Se selecciono el modelo deseado {dato_deseado} sin printear la lista de modelos")
        print("____________________________________________________________________________________________________")
    
    except:
        print("Opciones disponibles:")
        for opcion in select_modelo.options:
            print(opcion.text)
        opciones_disponibles = [opcion.text for opcion in select_modelo.options]
        mejor_coincidencia = max(opciones_disponibles, key=lambda opcion: SequenceMatcher(None, dato_deseado, opcion).ratio())
        select_modelo.select_by_visible_text(mejor_coincidencia)
        print(f"Se selecciono la mejor coincidencia para '{dato_deseado}': {mejor_coincidencia}")
        print("____________________________________________________________________________________________________")
    
    time.sleep(2)

 # Año
    ano_locator = (By.ID, "A_o_vehiculo_livianos_TablaSimple_Entero" )
    ANO = esperar_elemento(driver, ano_locator,1,2,3)
    select_ano = Select(ANO)
    dato_deseado = datos["ano"]
    try:
        select_ano.select_by_visible_text(dato_deseado)
        print(f"Se selecciono el ano deseado {dato_deseado} sin printear la lista de anos")
        print("____________________________________________________________________________________________________")
    
    except:
        print("Opciones disponibles:")
        for opcion in select_ano.options:
            print(opcion.text)
        opciones_disponibles = [opcion.text for opcion in select_ano.options]
        mejor_coincidencia = max(opciones_disponibles, key=lambda opcion: SequenceMatcher(None, dato_deseado, opcion).ratio())
        select_ano.select_by_visible_text(mejor_coincidencia)
        print(f"Se selecciono la mejor coincidencia para '{dato_deseado}': {mejor_coincidencia}")
        print("____________________________________________________________________________________________________")

 # Uso vehiculo
    uso_vehiculo_locator = (By.ID, "select2-uso_vehiculo_TablaSimple_Texto-container")
    USO_VEHICULO = esperar_elemento(driver, uso_vehiculo_locator,1,2,3)
    hacer_clic_elemento_con_reintentos(driver, USO_VEHICULO)
    opciones_uso_vehiculo = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.select2-results__option'))
    )
    for opcion in opciones_uso_vehiculo:
        print(opcion.text.strip())
    print("____________________________________________________________________________________________________")

 # Comercial
    if datos["uso_vehiculo"] == "comercial":
        for opcion in opciones_uso_vehiculo:
            if opcion.text.strip() == "Comercial":
                opcion.click()
                print("Se seleccionó la opción Comercial")
                print("____________________________________________________________________________________________________") 
                break        
 # Particular
    else:
        for opcion in opciones_uso_vehiculo:
            if opcion.text.strip() == "Particular":
                opcion.click()
                print("Se seleccionó la opción Particular") 
                print("____________________________________________________________________________________________________")
                break  

 # Comuna
    comuna_locator = (By.ID, "Comuna")
    COMUNA = esperar_elemento(driver, comuna_locator, 1,2,3)
    hacer_clic_elemento_con_reintentos(driver, COMUNA)
    select_comuna = Select(COMUNA)
    dato_deseado = datos["comuna"]
    try:
        select_comuna.select_by_visible_text(dato_deseado)
        print(f"Se selecciono el comuna deseado {dato_deseado} sin printear la lista de comunas")
        print("____________________________________________________________________________________________________")
    
    except:
        print("Opciones disponibles:")
        for opcion in select_comuna.options:
            print(opcion.text)
        opciones_disponibles = [opcion.text for opcion in select_comuna.options]
        mejor_coincidencia = max(opciones_disponibles, key=lambda opcion: SequenceMatcher(None, dato_deseado, opcion).ratio())
        select_comuna.select_by_visible_text(mejor_coincidencia)
        print(f"Se selecciono la mejor coincidencia para '{dato_deseado}': {mejor_coincidencia}")
        print("____________________________________________________________________________________________________")
        
 # Checkbox
    cobertura_total_checkbox_locator = (By.ID, "Cobertura_Total_CheckboxSimple")
    cobertura_total_checkbox = esperar_elemento(driver, cobertura_total_checkbox_locator , 1,2,3)
    hacer_clic_elemento_con_reintentos_js(driver, cobertura_total_checkbox)
    
 # Tipo pago
    tipo_pago_locator = (By.ID, "TipoMedioPago")
    tipo_pago = esperar_elemento(driver, tipo_pago_locator,1,2,3)
    select_pago = Select(tipo_pago)
    select_pago.select_by_visible_text("PAT")  

 # Tipo cuotas
    tipo_cuotas_locator = (By.ID, "Cuotas")
    tipo_cuotas = esperar_elemento(driver, tipo_cuotas_locator,1,3)
    select_cuotas = Select(tipo_cuotas)
    select_cuotas.select_by_visible_text("11")
    time.sleep(1)

 # Cotizar
    elemento_cotizar = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, "Cotizar"))
    )
    hacer_clic_elemento_con_reintentos_js(driver, elemento_cotizar)     

    esperar_carga_barra(driver) 

    time.sleep(2)

    try:
            # Busca alerta a cerrar
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert.warning.validacionTarificacion")))
            close_button = driver.find_element(By.CSS_SELECTOR, ".alert.warning.validacionTarificacion .close")
            close_button.click()
    except:
        print("No hubo alerta que cerrar")
        
 # Scrollear pagina
    driver.execute_script("window.scrollTo(0, window.scrollY + 125)")
    
    time.sleep(1)

 # Pantallazo
    timestamp = time.strftime("%Y%m%d_%H%M%S")  # Agrega un timestamp para hacer el nombre único
    cliente_nombre = datos['nombre_contratante']  # Usa el nombre del cliente como parte del nombre del archivo
    screenshot_path = os.path.join(directorio_actual, '..', 'Imagenes',f'captura_{cliente_nombre}_{timestamp}_ANS.png') 
    driver.save_screenshot(screenshot_path)

# Scrap
    html = driver.page_source
    data = []
    soup = BeautifulSoup(html, 'html.parser')
    tabla = soup.find('table', {'id': 'grilla-vehiculos'})
    if tabla:
        filas = tabla.find_all('tr')
        for fila in filas:
            if fila.find(class_="companyProduct") and fila.find(class_="mb-0 d-block ufPrice"):
                fila_data = [celda.get_text(strip=True) for celda in fila.find_all(['th', 'td'])]
                data.append(fila_data)
    # Crear Df
    df = pd.DataFrame(data)
    df.columns = ['Nombre de plan', 'S/D', 'UF-3', 'UF-5', 'UF-10','UF-15', 'UF-20','UF-25', 'UF-30']
         #. Eliminar desde $ en adelante
    regex = r'\$.*'
         #. Limpiar Df excepto la primera columna 'Nombre de plan'
    df.iloc[:, 1:] = df.iloc[:, 1:].replace(regex, '', regex=True)
         #. Imprimir df
    print(df)

        # Guardar el DataFrame en un directorio específico
    ruta_scrap =  os.path.join(directorio_actual, '..', 'Scrap', 'scrap_ans.txt')
    df.to_csv(ruta_scrap, index=False)
   
except Exception as e:
   # Registrar cualquier excepción que pueda ocurrir
    print(f"Error: {str(e)}")
    logging.error(f"Error: {str(e)}")
    print(traceback.format_exc())  # Esto imprimirá el rastreo completo de la excepción
    logging.error(traceback.format_exc())

sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__

driver.quit()



