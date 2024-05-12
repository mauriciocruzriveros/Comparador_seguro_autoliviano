from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from difflib import SequenceMatcher
import time
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.ui import Select
from difflib import get_close_matches
from datetime import datetime
import logging
import sys
from selenium.common.exceptions import StaleElementReferenceException
from bs4 import BeautifulSoup
import traceback
import pandas as pd 
from unidecode import unidecode
from selenium.common.exceptions import TimeoutException
import json
import os

def esperar_elemento(driver, locator, *numeros_condiciones, max_intentos=5):
        # Define las condiciones de espera y sus códigos
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
        
def seleccionar_opcion_similar(valor_manual, opciones):
    mejor_coincidencia = get_close_matches(valor_manual, opciones, n=1, cutoff=0.6)
    return mejor_coincidencia[0] if mejor_coincidencia else None

def encontrar_mejor_coincidencia(valor_deseado, opciones):
        mejor_coincidencia = max(opciones, key=lambda opcion: SequenceMatcher(None, valor_deseado, opcion.text.strip()).ratio())
        return mejor_coincidencia.text.strip()

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

# Directorio actual de Script
# print(f"Directorio actual de Script : {directorio_actual}")
directorio_actual = os.path.dirname(os.path.abspath(__file__))

# Configurar el registro
log_file_path = os.path.join(directorio_actual, '..', 'Reportes','reporte_sura.txt')
logging.basicConfig(filename=log_file_path, level=logging.INFO )
sys.stdout = open(log_file_path, 'w')
sys.stderr = open(log_file_path, 'w')

try:
 # Ruta de chromedriver
    service = Service(executable_path=os.path.join(directorio_actual, '..','chromedriver.exe'))
    driver = webdriver.Chrome(service=service)

 # Datos
    datos_file_path = os.path.join(directorio_actual, '..','Datos', "datos_ans.txt")
    with open(datos_file_path, 'r', encoding='utf-8') as file:
        datos_content = file.read()
        datos = eval(datos_content)

    print("____________________________________________________________________________________________________")
    print(datos)
    print("____________________________________________________________________________________________________")

 # Registro de información
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    informe = f"Informe - Cliente: {datos['nombre_contratante']}, Apellido: {datos['apellido_contratante']}, " \
            f"Patente: {datos['patente']}, Fecha: {fecha_actual}"
    print(informe)
    print("____________________________________________________________________________________________________")
    
    driver.get("https://seguros.sura.cl/acceso/corredor")
    driver.maximize_window()
    
# Credenciales
    ruta_credenciales = os.path.join(directorio_actual, '..','credenciales.json')
    # Leer el archivo JSON desde la ruta relativa
    with open(ruta_credenciales, 'r') as file:
        credentials = json.load(file)
    # Acceder a los datos
    rut = credentials['rut_sura']
    password = credentials['password_sura']

 # Botón Rut
    BOTON_LOGIN_locator = (By.ID, "Rut")
    BOTON_LOGIN = esperar_elemento(driver, BOTON_LOGIN_locator, 1, 2, 3, max_intentos=3)
    if BOTON_LOGIN:
        hacer_clic_elemento_con_reintentos(driver , BOTON_LOGIN)
    else:
        print(f"No se pudo encontrar el botón {BOTON_LOGIN_locator}.")

    for digito in rut:
        BOTON_LOGIN.send_keys(digito)
    
 # Botón Pass
    BOTON_PASS_locator = (By.ID, "Password")
    BOTON_PASS = esperar_elemento(driver, BOTON_PASS_locator, 1, 2, 3, max_intentos=10)
    if BOTON_PASS:
        hacer_clic_elemento_con_reintentos(driver ,BOTON_PASS)
    else:
        print(f"No se pudo encontrar el botón {BOTON_PASS_locator}")
    BOTON_PASS.send_keys(password)
 
 # Botón Enviar
    BOTON_ENVIAR_locator = (By.ID, "btnEnviar")
    BOTON_ENVIAR = esperar_elemento(driver, BOTON_ENVIAR_locator, 1, 2, 3, max_intentos=10)
    if BOTON_ENVIAR:
        hacer_clic_elemento_con_reintentos(driver, BOTON_ENVIAR)
    else:
        print(f"No se pudo encontrar {BOTON_ENVIAR_locator}.")
 
 # Esperar que cargue la página
    # enlace_ventas_locator = (By.ID, "ctlMenuSuperior_TB417B4A6110_ctl00_ctl00_navigationUl")
    # enlace_ventas = esperar_elemento(driver, enlace_ventas_locator, 1,2, max_intentos=10)
    # if enlace_ventas:
    #     pass
    # else:
    #     print(f"No se pudo encontrar {enlace_ventas_locator}")

    time.sleep(3)

 # Particular
    if datos["tipo_vehiculo"] == "particular":
        driver.get("https://seguros.sura.cl/sucursal-virtual/corredor/venta/movilidad/autoclickanual/cotizar/particular-cotizar")
        tipo_vehiculo_parametro = "particular"
 
 # Comercial
    else:
        driver.get("https://seguros.sura.cl/sucursal-virtual/corredor/venta/movilidad/autoclickanual/cotizar/comercial-cotizar")
        tipo_vehiculo_parametro = "comercial"

 # Cambiar iframe
    iframe_locator = (By.ID, "ifrExternalFrame")
    iframe_element = esperar_elemento(driver, iframe_locator, 1, max_intentos=5)
    if iframe_element:
        driver.switch_to.frame(iframe_element)
        print("Cambiado al contexto del iframe correctamente.")
    else:
        print(f"No se pudo encontrar {iframe_locator}.")
   
 # Click No
    elemento_no_locator = (By.CLASS_NAME, "checkMayorNo")
    ELEMENTO_NO = esperar_elemento(driver, elemento_no_locator, 1, 2, 3, max_intentos=3)
    hacer_clic_elemento_con_reintentos_js(driver, ELEMENTO_NO)
 
 # Rut
    elemento_rut_locator = (By.ID, 'RiesgoActual_Asegurado_Persona_Rut')
    ELEMENTO_RUT = esperar_elemento(driver, elemento_rut_locator, 1, 2, 3, max_intentos=3)
    rut = datos["rut"]
    rut_sin_ultimo_digito = rut[:-1]
    ELEMENTO_RUT.send_keys(rut_sin_ultimo_digito)

 # Botón buscar
    boton_buscar_locator = (By.ID, "btnBuscar")
    BOTON_BUSCAR = esperar_elemento(driver, boton_buscar_locator,1,2,3)
    hacer_clic_elemento_con_reintentos(driver,BOTON_BUSCAR)

 # Persona Natural
    if datos["tipo_persona"] == "natural":
    # Nombre
        elemento_nombre_locator = (By.ID, 'RiesgoActual_Asegurado_Persona_Nombre')
        elemento_nombre = esperar_elemento(driver, elemento_nombre_locator, 1, 2, 3, max_intentos=3)
        if elemento_nombre.is_enabled():
            elemento_nombre.send_keys(Keys.CONTROL + "a")
            elemento_nombre.send_keys(datos["nombre_contratante"]) 
        else:
            print(f"No se pudo encontrar {elemento_nombre_locator}")

 # Apellido
        elemento_apellido_paterno_locator = (By.ID, 'RiesgoActual_Asegurado_Persona_ApellidoPaterno')
        elemento_apellido_paterno = esperar_elemento(driver, elemento_apellido_paterno_locator, 1, 2, 3, max_intentos=3)
        if elemento_apellido_paterno.is_enabled():
            elemento_apellido_paterno.send_keys(datos["apellido_contratante"])  
        else:
            print(f"No se pudo encontrar {elemento_apellido_paterno_locator}")

    else:
        razon_social_locator = (By.ID, "RiesgoActual_Asegurado_Persona_NombreCompleto")
        RAZON_SOCIAL = esperar_elemento(driver, razon_social_locator,1,2,3)
       
        if RAZON_SOCIAL.is_enabled():
            time.sleep(2)
            RAZON_SOCIAL.clear()
            RAZON_SOCIAL.send_keys(datos["nombre_contratante"]) 
        else:
            pass

 # Vehiculo nuevo
    if datos["uso_vehiculo"] == "nuevo":
        elemento_estado_nuevo_locator = (By.ID, 'EstadoVehiculoNuevo')
        elemento_estado_nuevo = esperar_elemento(driver, elemento_estado_nuevo_locator, 1, 2, 3, max_intentos=3)
        if elemento_estado_nuevo:
            driver.execute_script("arguments[0].click();", elemento_estado_nuevo)
            print("Clic en 'Estado Nuevo' realizado correctamente.")
        else:
            print(f"No se pudo encontrar {elemento_estado_nuevo_locator}")
    
        actions = ActionChains(driver)
        actions.send_keys('\ue00C').perform()

    else:
        elemento_estado_usado_locator = (By.ID, 'EstadoVehiculoUsado')
        elemento_estado_usado = esperar_elemento(driver, elemento_estado_usado_locator, 1, 2, 3, max_intentos=3)
        if elemento_estado_usado:
            driver.execute_script("arguments[0].click();", elemento_estado_usado)
            print("Clic en 'Estado Usado' realizado correctamente.")

            #Alerta 
            alerta_locator = (By.CLASS_NAME, "btn-group")
            ALERTA = esperar_elemento(driver, alerta_locator, 1,2,3)
            hacer_clic_elemento_con_reintentos_js(driver, ALERTA)
        else:
            print(f"No se pudo encontrar {elemento_estado_usado_locator}")
        
    actions = ActionChains(driver)
    actions.send_keys('\ue00C').perform()      

 # Marca
    marca_locator = (By.XPATH, "//span[@class='k-input' and text()='SELECCIONE MARCA']")
    MARCA = esperar_elemento(driver, marca_locator, 1, 3)
    hacer_clic_elemento_con_reintentos_js(driver, MARCA, 3)
    marca_sura_valor = str(datos['marca'])

    try:
        select_marca_element_locator = (By.XPATH, f'//li[text()="{marca_sura_valor}"]')
        SELECT_MARCA_ELEMENTO = esperar_elemento(driver, select_marca_element_locator, 1, 2, 3)
        hacer_clic_elemento_con_reintentos_js(driver, SELECT_MARCA_ELEMENTO)
        print(f"Se seleccionó la marca deseada '{marca_sura_valor}' sin imprimir la lista de modelos.")
        print("____________________________________________________________________________________________________")

    except:
        lista_marca_locator = (By.XPATH, "//ul[@id='Vehiculo_MarcaID_listbox']")
        lista_desplegable = esperar_elemento(driver, lista_marca_locator, 1)
        opciones_disponibles = lista_desplegable.find_elements(By.XPATH, "//li[@role='option']")

        # Filtrar las opciones para eliminar "SELECCIONE MODELO" y líneas vacías
        opciones_filtradas = [opcion for opcion in opciones_disponibles if opcion.text.strip() and opcion.text.strip() != 'SELECCIONE MODELO']
        opciones_texto_filtrado = [opcion.text.strip() for opcion in opciones_filtradas]

        print("Opciones disponibles:")
        for opcion in opciones_texto_filtrado:
            print(opcion)

        mejor_coincidencia = max(opciones_texto_filtrado, key=lambda opcion: SequenceMatcher(None, marca_sura_valor, opcion).ratio())
        driver.execute_script("arguments[0].click();", [opcion for opcion in opciones_filtradas if opcion.text.strip() == mejor_coincidencia][0])
        print(f"Se seleccionó la mejor coincidencia para '{marca_sura_valor}': {mejor_coincidencia}")

    hacer_clic_elemento_con_reintentos_js(driver, MARCA, 3)
    
    time.sleep(1)

 # Modelo
    modelo_locator = (By.XPATH, "//span[@class='k-input' and text()='SELECCIONE MODELO']")
    MODELO = esperar_elemento(driver, modelo_locator, 1, 3)
    hacer_clic_elemento_con_reintentos_js(driver, MODELO)
    modelo_sura_valor = str(datos['modelo'])

    try:
        select_modelo_element_locator = (By.XPATH, f'//li[contains(text(), "{modelo_sura_valor}")]')
        SELECT_MODELO_ELEMENTO = esperar_elemento(driver, select_modelo_element_locator, 1, 2, 3)
        hacer_clic_elemento_con_reintentos_js(driver, SELECT_MODELO_ELEMENTO)
        print(f"Se seleccionó el modelo deseado '{modelo_sura_valor}' sin imprimir la lista de modelos.")
        print("____________________________________________________________________________________________________")

    except:
        lista_modelo_locator = (By.XPATH, "//ul[@id='Vehiculo_ModeloID_listbox']")
        lista_desplegable_modelo = esperar_elemento(driver, lista_modelo_locator, 1)
        opciones_disponibles_modelo = lista_desplegable_modelo.find_elements(By.XPATH, "//li[@role='option']")

        # Filtrar las opciones para eliminar "SELECCIONE MODELO" y líneas vacías
        opciones_filtradas_modelo = [opcion_modelo for opcion_modelo in opciones_disponibles_modelo if opcion_modelo.text.strip() and opcion_modelo.text.strip() != 'SELECCIONE MODELO']
        opciones_texto_filtrado_modelo = [opcion_modelo.text.strip() for opcion_modelo in opciones_filtradas_modelo]

        print("Opciones disponibles de modelo:")
        for opcion_modelo in opciones_texto_filtrado_modelo:
            print(opcion_modelo)

        mejor_coincidencia_modelo = max(opciones_texto_filtrado_modelo, key=lambda opcion_modelo: SequenceMatcher(None, modelo_sura_valor, opcion_modelo).ratio())
        driver.execute_script("arguments[0].click();", [opcion_modelo for opcion_modelo in opciones_filtradas_modelo if opcion_modelo.text.strip() == mejor_coincidencia_modelo][0])
        print(f"Se seleccionó la mejor coincidencia para el modelo '{modelo_sura_valor}': {mejor_coincidencia_modelo}")
 
 # Patente
    patente_locator = (By.ID, "Vehiculo_Patente")
    patente_element = esperar_elemento(driver, patente_locator,1,3)
    uso_vehiculo = datos["uso_vehiculo"]
    if uso_vehiculo == "nuevo":
        patente_element.send_keys("ET0000")
    else:
        patente_element.send_keys(datos["patente"]) 

 # Año
    ano_locator = (By.ID, "Vehiculo_Ano")
    ano_element = esperar_elemento(driver, ano_locator, 1, 3)
    if ano_element:
        ano_element.clear()
        ano_element.send_keys(datos["ano"])
        print(f"Año '{datos['ano']}' ingresado correctamente.")
    else:
        print(f"No se pudo encontrar el elemento {ano_locator}.")

 # Continuar
    boton_siguiente_locator = (By.ID, "btnCotizar")
    boton_siguiente_element = esperar_elemento(driver, boton_siguiente_locator, 1, 3)
    if boton_siguiente_element:
        hacer_clic_elemento_con_reintentos(driver, boton_siguiente_element, 3)
        print("Se hizo clic en el botón 'Siguiente' correctamente.")
    else:
        print(f"No se pudo encontrar el botón 'Siguiente' con el locator {boton_siguiente_locator}.")
    
    time.sleep(5)

    driver.execute_script("window.scrollTo(0, window.scrollY + 1500)")
    driver.switch_to.default_content()
    driver.execute_script("window.scrollTo(0, window.scrollY + 250)")

 # Cambiar iframe
    iframe_locator = (By.ID, "ifrExternalFrame")
    iframe_element = esperar_elemento(driver, iframe_locator, 1, max_intentos=5)
    if iframe_element:
        driver.switch_to.frame(iframe_element)
        print("Cambiado al contexto del iframe correctamente.")
    else:
        print(f"No se pudo encontrar {iframe_locator}.")
    
 # Cuotas
    radio_cuota_locator = (By.ID, "chkCuota")
    radio_cuota_element = esperar_elemento(driver, radio_cuota_locator, 1, 3) 
    if radio_cuota_element:
        hacer_clic_elemento_con_reintentos_js(driver, radio_cuota_element,5)
        print("Se hizo clic en el radio button 'Valor Cuota' correctamente.")
    else:
        print(f"No se pudo encontrar el radio button 'Valor Cuota' con el locator {radio_cuota_locator}.")  
    
    # Opcion 11
    option_11 = driver.find_element(By.XPATH, "//li[text()='11']")
    hacer_clic_elemento_con_reintentos_js(driver, option_11, 5)
    print("Se seleccionó '11' en el elemento desplegable correctamente.")
    
 # Pantallazo
    timestamp = time.strftime("%Y%m%d_%H%M%S")  
    cliente_nombre = datos['nombre_contratante']  
    screenshot_path = os.path.join(directorio_actual, '..','Imagenes', f"captura_{cliente_nombre}_{timestamp}_sura.png")
    driver.save_screenshot(screenshot_path)
    
#     parametros = {
#     'tipo_vehiculo': tipo_vehiculo_parametro,
#     'tipo_persona': 'natural',
#     'rut': '144187865',
#     'nombre_contratante': 'Yasna',
#     'apellido_contratante': 'Paredes',
#     'uso_vehiculo': 'usado',
#     'patente': 'RLRJ87',
#     'marca': 'MG',
#     'modelo': 'RX5',
#     'ano': '2022',
#     'rubro': '',
#     'estilo_vehiculo': 'AUTOMOVIL',
#     'comuna': 'VIÑA DEL MAR - VALPARAÍSO',
#     'marca_liberty': 'MG'
# }

# # Verificación
#     ruta_archivo = os.path.join(directorio_actual, '..','Seleccion', 'seleccion_sura')
#     with open(ruta_archivo, 'w') as archivo:
#         for clave, valor in parametros.items():
#             archivo.write(f'{clave}: {valor}\n')

except Exception as e:
    # Registrar cualquier excepción que pueda ocurrir
    print(f"Error: {str(e)}")
    logging.error(f"Error: {str(e)}")
    print(traceback.format_exc())  # Esto imprimirá el rastreo completo de la excepción
    logging.error(traceback.format_exc())

sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__

driver.quit()
