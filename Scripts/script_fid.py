from selenium.common.exceptions import TimeoutException, NoSuchElementException, NoSuchFrameException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
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
import unicodedata
import traceback
import logging
import locale
import time
import sys
import json
import os

# Definiciones 
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
    
# Directorio actual script
directorio_actual = os.path.dirname(os.path.abspath(__file__))

# Configurar el registro
log_file_path = os.path.join(directorio_actual, "..", "Reportes", "reporte_fid.txt")
logging.basicConfig(filename=log_file_path, level=logging.INFO )
sys.stdout = open(log_file_path, 'w')
sys.stderr = open(log_file_path, 'w')

try:
 # Ruta de chromedriver
    service = Service(executable_path=os.path.join(directorio_actual, "..", "chromedriver.exe"))
    driver = webdriver.Chrome(service=service)

 # Datos
    datos_file_path = os.path.join(directorio_actual, "..", "Datos", "datos_ans.txt")
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

    driver.get("https://portal.fidseguros.cl/Fidnet_UI/Logins.aspx?Type=2")
    driver.maximize_window()  

 # Inicio de sesión
   # Credenciales
    ruta_credenciales = os.path.join(directorio_actual, '..','credenciales.json')
    # Leer el archivo JSON desde la ruta relativa
    with open(ruta_credenciales, 'r') as file:
        credentials = json.load(file)
    email = credentials['email']
    password = credentials['password_fid']

    user_locator = (By.ID, "Base_Th_wt31_block_wtBotones_wtLoginStructure_Username")
    USERNAME = esperar_elemento(driver, user_locator, 1 , 3)
    USERNAME.send_keys(email)

    pass_locator = (By.ID, "Base_Th_wt31_block_wtBotones_wtpass")
    PASS = esperar_elemento(driver, pass_locator, 1 , 3)
    PASS.send_keys(password)

    continuar_locator = (By.ID, "Base_Th_wt31_block_wtBotones_wt15")
    CONTINUAR = esperar_elemento (driver, continuar_locator , 1 , 3)
    hacer_clic_elemento_con_reintentos_js(driver, CONTINUAR, 5)

    esperar_elemento_locator = (By.ID, "Base_Th_wt74_block_wtMainContent_wt1")
    ESPERAR = esperar_elemento(driver, esperar_elemento_locator,1 ,3, max_intentos=5)
    if ESPERAR:
         driver.get("https://portal.fidseguros.cl/FidWeb_Fidens_UI/GlobalFidens.aspx?Tipo=VM")
    else:
        print("No se pudo acceder a la pagina de cotización")
        driver.quit()

 # Cambiar iframe
    try:
        WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, '#Base_Th_wt9_block_wtMainContent_wtContainerIframe iframe')))
    except (NoSuchFrameException, TimeoutException):
        print("Error: No se pudo encontrar o cambiar al iframe")

 # Particular o comercial
 # Particular    
    if datos["tipo_vehiculo"] == "particular":
        P_O_C_locator = (By.XPATH, "//mat-select[@id='mat-select-1']")
        P_O_C = esperar_elemento(driver, P_O_C_locator, 1 , 3)
        hacer_clic_elemento_con_reintentos(driver, P_O_C)
        particular_locator = (By.ID, "mat-option-1")
        PARTICULAR = esperar_elemento(driver, particular_locator, 1 , 2 )
        hacer_clic_elemento_con_reintentos(driver, PARTICULAR, 5) 

 # Comercial
    else:
        P_O_C_locator = (By.XPATH, "//mat-select[@id='mat-select-1']")
        P_O_C = esperar_elemento(driver, P_O_C_locator, 1 , 3)
        hacer_clic_elemento_con_reintentos(driver, P_O_C)
        comercio_locator = (By.XPATH, '//mat-option/span[text()="Comercio"]')
        COMERCIO = esperar_elemento(driver, comercio_locator, 1)
        hacer_clic_elemento_con_reintentos(driver, COMERCIO, 5)

 # Nuevo o Usado
    usado_locator = (By.ID , "mat-radio-11-input")
    USADO = esperar_elemento(driver, usado_locator, 1 , 3)
    hacer_clic_elemento_con_reintentos_js(driver, USADO, 5)

 # Patente
    patente_locator = (By.CLASS_NAME, "mat-form-field-wrapper")
    PATENTE = esperar_elemento (driver, patente_locator , 1 , 2)
    PATENTE.send_keys("Test")
                 
    time.sleep(25)

except Exception as e:
    # Registrar cualquier excepción que pueda ocurrir
    print(f"Error: {str(e)}")
    logging.error(f"Error: {str(e)}")
    print(traceback.format_exc())  # Esto imprimirá el rastreo completo de la excepción
    logging.error(traceback.format_exc())

sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__