from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from difflib import SequenceMatcher, get_close_matches
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from datetime import datetime
import traceback
import logging
import json
import time
import sys
import os

# Definiciones
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

def seleccionar_opcion_similar(valor_manual, opciones):
                mejor_coincidencia = get_close_matches(valor_manual, opciones, n=1, cutoff=0.6)
                return mejor_coincidencia[0] if mejor_coincidencia else None
        
def encontrar_mejor_coincidencia(valor_deseado, opciones):
            mejor_coincidencia = max(opciones, key=lambda opcion: SequenceMatcher(None, valor_deseado, opcion.text.strip()).ratio())
            return mejor_coincidencia.text.strip()

def espera_pagina_cargada(driver):
    try:
        # Espera a que el elemento con el estilo dado esté presente y visible
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@style="opacity: 0; z-index: 1400; transition: opacity 195ms cubic-bezier(0.4, 0, 0.2, 1) 0ms; visibility: hidden;"]'))
        )
        print("La página está cargada")
    except Exception as e:
        print("Error al esperar la página cargada:", e)

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

# Obtener el directorio actual (donde se encuentra el script)
directorio_actual = os.path.dirname(os.path.abspath(__file__))

try:
 # Configurar el registro
    log_file_path = os.path.join(directorio_actual, '..', 'Reportes','reporte_liberty.txt') 
    logging.basicConfig(filename=log_file_path, level=logging.INFO)
    sys.stdout = open(log_file_path, 'w')
    sys.stderr = open(log_file_path, 'w')

 # Ruta de chromedriver
    service = Service(executable_path=os.path.join(directorio_actual, '..', 'chromedriver.exe'))
    driver = webdriver.Chrome(service=service)

 # Datos
    datos_file_path =  os.path.join(directorio_actual, '..', 'Datos', 'datos_liberty.txt') 
    with open(datos_file_path, 'r', encoding='utf-8') as file:
        datos_content = file.read()
        datos = eval(datos_content)
    print(datos)
        
 # Registro de información
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    informe = f"Informe - Cliente: {datos['nombre_contratante']}, Apellido: {datos['apellido_contratante']}, " \
              f"Patente: {datos['patente']}, Fecha: {fecha_actual}"
    print(informe)
    print("____________________________________________________________________________")



 # Credenciales
    ruta_credenciales = os.path.join(directorio_actual, '..','credenciales.json')
    #.. Leer el archivo JSON desde la ruta relativa
    with open(ruta_credenciales, 'r') as file:
        credentials = json.load(file)
    rut = credentials['rut_liberty']
    password = credentials['password_liberty']
    email = credentials['email']
    #.. Login
    driver.maximize_window()
    driver.get("https://www.liberty.cl/menu_aplicaciones/viewLogin")

    RUT_LIBERTY_locator = (By.CLASS_NAME, "nomUsuario")
    RUT_LIBERTY = esperar_elemento(driver, RUT_LIBERTY_locator, 1)
    RUT_LIBERTY.send_keys(rut)

    PASSWORD_LIBERTY_locator = (By.ID, "j_password")
    PASSWORD_LIBERTY = esperar_elemento(driver, PASSWORD_LIBERTY_locator, 1)
    PASSWORD_LIBERTY.send_keys(password + Keys.ENTER)

 # Página de inicio
    boton_inicio_locator = (By.XPATH, "//div[@id='bot1']//a[@id='10']")
    BOTON_INICIO = esperar_elemento(driver, boton_inicio_locator, 1,2,3)
    hacer_clic_elemento_con_reintentos(driver, BOTON_INICIO)
    espera_pagina_cargada(driver)

 # Botón vehiculo liviano 
    boton_liviano_locator = (By.XPATH, "//button[.//span[contains(@class, 'MuiButton-label')]//div//p[text()='Livianos']]")
    BOTON_LIVIANO = esperar_elemento(driver, boton_liviano_locator, 1,2,3)
    hacer_clic_elemento_con_reintentos(driver, BOTON_LIVIANO)
    print("____________________________________________________________________________")
    
    espera_pagina_cargada(driver)

 # Checkbox
    checkbox_locator = (By.CLASS_NAME, "MuiIconButton-label")
    CHECKBOX = esperar_elemento(driver, checkbox_locator, 1,2,3)
    hacer_clic_elemento_con_reintentos(driver, CHECKBOX)

 # Rut                         
    rut_input_liberty_locator = (By.ID, "rut")
    rut_input_liberty = esperar_elemento(driver, rut_input_liberty_locator, 1,2)
    if rut_input_liberty.is_enabled:
        rut_input_liberty.send_keys(datos["rut"])
    else:
        pass

    espera_pagina_cargada(driver)

    if datos["tipo_persona"] == "natural":
        nombre_input_liberty_locator = (By.ID, "name")
        nombre_input_liberty = esperar_elemento(driver, nombre_input_liberty_locator, 1,2)
        nombre_input_liberty.send_keys(Keys.CONTROL + "a")
        nombre_input_liberty.send_keys(Keys.DELETE)
        nombre_input_liberty.send_keys(datos["nombre_contratante"])
       
        espera_pagina_cargada(driver)
        
 # Apellido
        apellido_input_liberty_locator = (By.ID, "lastname")
        apellido_input_liberty = esperar_elemento(driver, apellido_input_liberty_locator, 1,2)
        apellido_input_liberty.send_keys(Keys.CONTROL + "a")
        apellido_input_liberty.send_keys(Keys.DELETE)
        apellido_input_liberty.send_keys(datos["apellido_contratante"])
        espera_pagina_cargada(driver)
    else:
        razon_social_locator = (By.ID, "razonsocial")
        razon_social = esperar_elemento(driver, razon_social_locator, 1,2)
        razon_social.send_keys(Keys.CONTROL + "a")
        razon_social.send_keys(Keys.DELETE)
        razon_social.send_keys(datos["nombre_contratante"]) 

    espera_pagina_cargada(driver)

 # E-mail
    email_input_locator = (By.ID, "email")
    email_input_liberty = esperar_elemento(driver, email_input_locator, 1,2)
    if email_input_liberty.is_enabled():
        email_input_liberty.send_keys(Keys.CONTROL + "a")
        email_input_liberty.send_keys(Keys.DELETE)
        email_input_liberty.send_keys(email)
    else:
        pass

    espera_pagina_cargada(driver)

 # Telefono
    phone_input_locator = (By.ID, "phone")
    phone_input_liberty = esperar_elemento(driver, phone_input_locator, 1,2)
    if phone_input_liberty.is_enabled:
        phone_input_liberty.send_keys(Keys.CONTROL + "a")
        phone_input_liberty.send_keys(Keys.DELETE)
        phone_input_liberty.send_keys("+56979425896")
    else:
        pass

    espera_pagina_cargada(driver)

 # ¿El contratante es igual al asegurado?       =            SI              
    radio_si_locator = (By.XPATH, '//input[@name="samedata" and @value="si"]')
    radio_si = esperar_elemento(driver, radio_si_locator, 1 ,2, 3)
    hacer_clic_elemento_con_reintentos(driver, radio_si)

 # ¿Uso en aplicación de pasajeros/entregas?    =            NO                                          
    radio_no_susQuestions_0_locator = (By.XPATH, '//input[@name="susQuestions[0].question" and @value="no"]')
    radio_no_susQuestions_0 = esperar_elemento(driver, radio_no_susQuestions_0_locator, 1,2 ,3)
    hacer_clic_elemento_con_reintentos(driver, radio_no_susQuestions_0)

 # ¿Es alta gama, híbrido o eléctrico?        =            NO               
    radio_no_susQuestions_1_locator = (By.XPATH, '//input[@name="susQuestions[1].question" and @value="no"]')
    radio_no_susQuestions_1 = esperar_elemento(driver, radio_no_susQuestions_1_locator, 1, 2, 3)
    hacer_clic_elemento_con_reintentos(driver, radio_no_susQuestions_1)

 # Switch Auto usado - Auto nuevo                             
    if datos["uso_vehiculo"] == "nuevo":
            # Hacer clic en el radio button "Sí"
            vehiculo_nuevo_locator = (By.XPATH, '//input[@name="newVehicle" and @value="si"]')
            vehiculo_nuevo = esperar_elemento(driver, vehiculo_nuevo_locator, 1, 2,3)
            hacer_clic_elemento_con_reintentos(driver, vehiculo_nuevo)
    else:
            # Hacer clic en el radio button "No"
            vehiculo_usado_locator = (By.XPATH, '//input[@name="newVehicle" and @value="no"]')
            vehiculo_usado = esperar_elemento(driver, vehiculo_usado_locator, 1,2,3)
            hacer_clic_elemento_con_reintentos(driver, vehiculo_usado)
 
 # Vehiculo particular o comercial
    select_element_locator = (By.ID, "mui-component-select-vehUse")
    select_element = esperar_elemento(driver, select_element_locator, 1,2,3)
    hacer_clic_elemento_con_reintentos(driver, select_element)

    if datos["tipo_vehiculo"] == "particular":

 # Vehiculo particular                     
        option_particular_locator = (By.XPATH, '//li[@data-value="1"]')
        option_particular = esperar_elemento(driver, option_particular_locator, 1 ,2,3)
        hacer_clic_elemento_con_reintentos(driver, option_particular)
        
    else:  
 # Vehiculo comercial
        option_comercial_locator = (By.XPATH, '//li[@data-value="2"]')
        option_comercial = esperar_elemento(driver, option_comercial_locator, 1,2, 3)
        hacer_clic_elemento_con_reintentos(driver, option_comercial)
         
 # Rubro
        elemento_lista_desplegable_locator = (By.ID, 'mui-component-select-vehAreaLight')
        ELEMENTO_LISTA_DESPLEGABLE = esperar_elemento(driver, elemento_lista_desplegable_locator,1,2,3)
        hacer_clic_elemento_con_reintentos(driver,ELEMENTO_LISTA_DESPLEGABLE)
        dropdown_locator=(By.CLASS_NAME, "MuiMenu-list")
        esperar_elemento(driver, elemento_lista_desplegable_locator, 1,2,3)
        rubro_valor = datos["rubro"]
        rubro_locator = (By.XPATH, f'//li[@data-value="{rubro_valor}"]')
        RUBRO = esperar_elemento(driver, rubro_locator,1,2,3)
        hacer_clic_elemento_con_reintentos(driver, RUBRO)     
                                 
 # Patente
    patente_input_liberty_locator = (By.ID, "plate")
    patente_input_liberty = esperar_elemento(driver, patente_input_liberty_locator, 1 ,2, 3)
    if patente_input_liberty:
        patente_input_liberty.click()
        patente_input_liberty.send_keys(Keys.CONTROL + "a")
        patente_input_liberty.send_keys(Keys.DELETE)
        patente_input_liberty.send_keys(datos["patente"])
    else:
        print("El elemento 'plate' no se encontró después de varios intentos.")
    
 # Marca
    element_marca_locator = (By.XPATH, "//div[@id='mui-component-select-vehBrand']")
    element_marca = esperar_elemento(driver, element_marca_locator, 1 ,2 ,3)
    espera_pagina_cargada(driver)
    hacer_clic_elemento_con_reintentos(driver, element_marca)
    marca_liberty_valor = str(datos['marca_liberty'])
    lista_marca_locator = (By.CLASS_NAME, "MuiList-root")
    lista_desplegable = esperar_elemento(driver, lista_marca_locator, 1)
    try:
        select_marca_element = driver.find_element(By.XPATH, f'//li[text()="{marca_liberty_valor}"]')
        driver.execute_script("arguments[0].click();", select_marca_element)
        print(f"Se seleccionó la marca deseada '{marca_liberty_valor}' sin imprimir la lista de modelos.")
        print("____________________________________________________________________________________________________")
    except:
        opciones_disponibles = lista_desplegable.find_elements(By.XPATH, "//li[@role='option']")
        opciones_texto = [opcion.text for opcion in opciones_disponibles]
        print("Opciones disponibles:")
        for opcion in opciones_texto:
            print(opcion)
        mejor_coincidencia = max(opciones_texto, key=lambda opcion: SequenceMatcher(None, marca_liberty_valor, opcion).ratio())
        driver.execute_script("arguments[0].click();", [opcion for opcion in opciones_disponibles if opcion.text == mejor_coincidencia][0])
        print(f"Se seleccionó la mejor coincidencia para '{marca_liberty_valor}': {mejor_coincidencia}")

    espera_pagina_cargada(driver)
 
 # Modelo
    element_modelo= (By.ID, "mui-component-select-vehModel")
    ELEMENT_MODELO = esperar_elemento(driver, element_modelo, 1 , 2, 3)
    espera_pagina_cargada(driver)
    hacer_clic_elemento_con_reintentos(driver, ELEMENT_MODELO)
    modelo_deseado = datos["modelo"]
    lista_modelo_locator = (By.CLASS_NAME, "MuiList-root")
    lista_desplegable = esperar_elemento(driver, lista_marca_locator, 1,2)
    try:
        select_modelo_element = driver.find_element(By.XPATH, f'//li[text()="{modelo_deseado}"]')
        driver.execute_script("arguments[0].click();", select_modelo_element)
        print(f"Se seleccionó el modelo deseado '{modelo_deseado}' sin imprimir la lista de modelos.")
        print("____________________________________________________________________________________________________")
    except:
        opciones_disponibles = driver.find_elements(By.XPATH, "//li[@role='option']")
        opciones_texto = [opcion.text for opcion in opciones_disponibles]
        print("Opciones disponibles de modelos:")
        for opcion in opciones_texto:
            print(opcion)
        mejor_coincidencia = max(opciones_texto, key=lambda opcion: SequenceMatcher(None, modelo_deseado, opcion).ratio())
        driver.execute_script("arguments[0].click();", [opcion for opcion in opciones_disponibles if opcion.text == mejor_coincidencia][0])
        print(f"Se seleccionó la mejor coincidencia para '{modelo_deseado}': {mejor_coincidencia}")

    espera_pagina_cargada(driver)

 # Estilo vehiculo
    estilo_locator = (By.ID, 'mui-component-select-vehType')
    ESTILO = esperar_elemento(driver, estilo_locator,1,2,3)
    hacer_clic_elemento_con_reintentos(driver, ESTILO)
    estilo_deseado = datos["estilo_vehiculo"]
    opciones_disponibles = driver.find_elements(By.XPATH, "//ul[@role='listbox']//li[@role='option']")
    opciones_texto = [opcion.text for opcion in opciones_disponibles]
    mejor_coincidencia = max(opciones_texto, key=lambda opcion: SequenceMatcher(None, estilo_deseado, opcion).ratio())
    driver.execute_script("arguments[0].click();", [opcion for opcion in opciones_disponibles if opcion.text == mejor_coincidencia][0])
    print(opciones_texto)
    print(f"Se seleccionó la mejor coincidencia para '{estilo_deseado}': {mejor_coincidencia}")

 # Año de vehiculo
    ano_locator = (By.ID, "mui-component-select-vehYear")
    element_ano = esperar_elemento(driver,ano_locator , 1 , 2 ,3)
    espera_pagina_cargada(driver)
    hacer_clic_elemento_con_reintentos(driver, element_ano)
    opciones_ano_locator = (By.CLASS_NAME, "MuiList-root")
    opciones_ano_element = esperar_elemento(driver, opciones_ano_locator, 1, 2, 3)
    opciones_ano = opciones_ano_element.find_elements(By.CLASS_NAME, "MuiListItem-root")
    lista_opciones_ano = [opcion.text for opcion in opciones_ano if opcion.text]
    print(lista_opciones_ano)
    # Año deseado
    ano_deseado = str(datos['ano'])
    print("Lista de opciones de año:", lista_opciones_ano)
    for opcion in opciones_ano:
        if opcion.text == ano_deseado:
            driver.execute_script("arguments[0].click();", opcion)
            print(f"Año '{ano_deseado}' seleccionado.")
            break
    else:
        print(f"El año '{ano_deseado}' no se encuentra en la lista de opciones.")
    print("____________________________________________________________________________")

    espera_pagina_cargada(driver)

 # Continuar
    continuar_button_locator = (By.XPATH, "//span[text()='Continuar']")
    continuar_button = esperar_elemento(driver, continuar_button_locator, 3)
    if continuar_button:
        print("Haciendo clic en el botón Continuar...")
        hacer_clic_elemento_con_reintentos(driver, continuar_button)      
    else:
        print("No se encontró el botón Continuar después de varios intentos.")
    
    time.sleep(1)

    espera_pagina_cargada(driver)

   # Esperar a que el botón de cierre esté presente y visible
    #boton_cierre_locator = (By.XPATH, "//div[contains(@style, 'display: block;')]")
    #BOTON_CIERRE = esperar_elemento(driver, boton_cierre_locator, 1, 2, 3)

    # Hacer clic en el botón de cierre
    #hacer_clic_elemento_con_reintentos_js(driver, BOTON_CIERRE)
     
    #.. Scrollear Página
    driver.execute_script("window.scrollTo(0, window.scrollY + 500)")
    
    #.. Pantallazo
    timestamp = time.strftime("%Y%m%d_%H%M%S")  
    cliente_nombre = datos['nombre_contratante']   
    screenshot_path = os.path.join(directorio_actual, '..', 'Imagenes', f'captura_{cliente_nombre}_{timestamp}_liberty.png') 
    driver.save_screenshot(screenshot_path)
    
except Exception as e:
    error_msg = f"Error: {str(e)}"
    print(error_msg)
    logging.error(error_msg)
    traceback_msg = traceback.format_exc()
    print(traceback_msg)
    logging.error(traceback_msg)

sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__

driver.quit()







