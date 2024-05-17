from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
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
import traceback
import logging
import time
import json
import sys
import os

#Definiciones 
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

def espera_carga_completa(driver, tiempo_espera=10):
    try:
        WebDriverWait(driver, tiempo_espera).until(
            EC.presence_of_element_located((By.ID, "detalle_panelUpdateProgress"))
        )
        WebDriverWait(driver, tiempo_espera).until(
            EC.invisibility_of_element_located((By.ID, "detalle_panelUpdateProgress"))
        )
        print("La página ha cargado completamente.")
        return True
    except Exception as e:
        print(f"Error al esperar la carga completa de la página: {str(e)}")
        return False

# Directorio actual
directorio_actual = os.path.dirname(os.path.abspath(__file__))

# Configurar el registro
log_file_path = os.path.join(directorio_actual,"..", "Reportes","reporte_zurich.txt")
logging.basicConfig(filename=log_file_path, level=logging.INFO )
sys.stdout = open(log_file_path, 'w')
sys.stderr = open(log_file_path, 'w')

try:
 # Ruta de chromedriver
    service = Service(executable_path=os.path.join(directorio_actual,"..", "chromedriver.exe"))
    driver = webdriver.Chrome(service=service)
 
 # Datos
    datos_file_path = os.path.join (directorio_actual,"..", "Datos","datos_ans.txt")
    with open(datos_file_path, 'r', encoding='utf-8') as file:
        datos_content = file.read()
        datos = eval(datos_content)
     
     #.. Ver datos
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
    rut = credentials['rut_zurich']
    password = credentials['password_zurich']    

    #.. Login
    driver.get("https://portalcorredores.zurich.cl/auth/login")
    driver.maximize_window()

 # User
    user_locator = (By.CSS_SELECTOR, '.input-user input')
    USER = esperar_elemento(driver, user_locator, 2)
    USER.send_keys(rut)  # Envía las teclas al campo de entrada

 # Pass        
    password_locator = (By.CSS_SELECTOR, '.input-user input[type="password"]')
    PASSWORD = esperar_elemento(driver, password_locator, 2)
    PASSWORD.send_keys(password)

 # Botón
    BOTON_INGRESAR = esperar_elemento(driver, (By.CLASS_NAME, 'btn-continue'), 3)
    hacer_clic_elemento_con_reintentos(driver, BOTON_INGRESAR)

    time.sleep(5)

    driver.get("https://portalcorredores.zurich.cl/cotizadores/accesos")

 # Botón Automovil
    boton_automovil_locator = (By.ID, "Cotizadores-Seguros-Individuales-Automovil")
    BOTON_AUTOMOVIL = esperar_elemento(driver, boton_automovil_locator, 1, 2 ,3)
    hacer_clic_elemento_con_reintentos(driver, BOTON_AUTOMOVIL, 5)

 # Botón Continue
    button_locator = (By.CLASS_NAME, 'btn-continue--active')  # Selector del botón por su clase
    BUTTON = esperar_elemento(driver, button_locator, 2)  # Esperar a que el botón esté presente y sea clickeable
    hacer_clic_elemento_con_reintentos(driver, BUTTON)  # Hacer clic en el botón utilizando la función definida

 # Botón continuar
    boton_continue_2_locator = (By.ID, "Boton-Modal-Cotizadores-Cotizar")
    BOTON_CONTINUE_2 = esperar_elemento(driver, boton_continue_2_locator, 1,2,3)
    hacer_clic_elemento_con_reintentos(driver, BOTON_CONTINUE_2, 5)

    espera_carga_completa(driver)

    # Obtener todas las ventanas abiertas por el controlador
    ventanas_abiertas = driver.window_handles
    print("Identificadores de ventanas abiertas:", ventanas_abiertas)

    while True:
    # Realiza la operación que deseas repetir
        if len(ventanas_abiertas) > 1:
            print("Se encontraron ventanas emergentes adicionales.")
            # Cambiar al contexto de la ventana principal (primera ventana)
            driver.switch_to.window(ventanas_abiertas[1])  # Cambia al primer índice si hay más de una ventana abierta
            print("Se cambió al contexto de la ventana principal")
            break  # Sale del bucle una vez que la operación se ha realizado

 # Auto Usado
    if datos["uso_vehiculo"] == "usado":
        auto_usado_locator = (By.XPATH, '//input[@id="detalle_rdbUsado_0" and @value="S"]')
        AUTO_USADO = esperar_elemento(driver, auto_usado_locator, 3)
        hacer_clic_elemento_con_reintentos(driver, AUTO_USADO)

        #Patente
        patente_locator = (By.ID, "detalle_txtPatente")
        PATENTE = esperar_elemento(driver, patente_locator, 1, 3)
        PATENTE.send_keys(datos["patente"])
        PATENTE.send_keys(Keys.ENTER)

    else: 
        auto_nuevo_locator = (By.XPATH, '//input[@id="detalle_rdbUsado_1" and @value="N"]')
        AUTO_NUEVO = esperar_elemento(driver, auto_nuevo_locator, 3)
        hacer_clic_elemento_con_reintentos(driver, AUTO_NUEVO)
    
    espera_carga_completa(driver)
           
 # Marca
    cbo_marca_locator = (By.ID, "detalle_cboMarca")
    cbo_marca_element = esperar_elemento(driver, cbo_marca_locator, 1 ,  3)
    select_cbo_marca = Select(cbo_marca_element)
    marca_deseada = datos["marca"] 
    if cbo_marca_element.is_enabled(): 
        try:
            select_cbo_marca.select_by_visible_text(marca_deseada)
            print(f"Se seleccionó la marca deseada: {marca_deseada}")
        except:
            # Imprimir todas las opciones disponibles
            print("Opciones disponibles:")
            for opcion in select_cbo_marca.options:
                print(opcion.text)
            # Seleccionar la mejor coincidencia utilizando SequenceMatcher
            opciones_disponibles = [opcion.text for opcion in select_cbo_marca.options]
            mejor_coincidencia = max(opciones_disponibles, key=lambda opcion: SequenceMatcher(None, marca_deseada, opcion).ratio())
            select_cbo_marca.select_by_visible_text(mejor_coincidencia)
            print(f"Se seleccionó la mejor coincidencia para '{marca_deseada}': {mejor_coincidencia}")
    else:
        pass

    espera_carga_completa(driver)

    time.sleep(4)

 # Modelo
    cbo_modelo_locator = (By.ID, "detalle_cboModelo")
    cbo_modelo_element = esperar_elemento(driver, cbo_modelo_locator, 1 , 3)
    select_cbo_modelo = Select(cbo_modelo_element)
    modelo_deseado = datos["modelo"]
    if cbo_modelo_element.is_enabled():
        try:
            # Intentar seleccionar el modelo deseado
            select_cbo_modelo.select_by_visible_text(modelo_deseado)
            print(f"Se seleccionó el modelo deseado: {modelo_deseado}")
        except:
            # Si el modelo exacto no está disponible, seleccionar la mejor coincidencia
            print("Opciones disponibles:")
            for opcion in select_cbo_modelo.options:
                print(opcion.text)
            opciones_disponibles = [opcion.text for opcion in select_cbo_modelo.options]
            mejor_coincidencia = max(opciones_disponibles, key=lambda opcion: SequenceMatcher(None, modelo_deseado, opcion).ratio())
            select_cbo_modelo.select_by_visible_text(mejor_coincidencia)
            print(f"Se seleccionó la mejor coincidencia para '{modelo_deseado}': {mejor_coincidencia}")
        
    else:
        pass

 # Año
    ano_locator = (By.ID, "detalle_cboAno")
    cbo_ano = esperar_elemento(driver, ano_locator, 1 , 3)
    if cbo_ano.is_enabled():
        hacer_clic_elemento_con_reintentos(driver, cbo_ano)
        select_element_ano_locator = (By.ID,"detalle_cboAno")
        select_ano = esperar_elemento(driver, select_element_ano_locator, 1 ,3)
        select_ano_element= Select(select_ano)
        options = select_ano_element.options
        for option in options:
            print(option.text) 
        select_ano_element.select_by_value(datos["ano"])  # Selecciona el año 2023
    else:       
        pass

 # Uso Vehiculo
    # Particular
    if datos["uso_vehiculo"]== "particular":
        select_element_uso_locator = (By.ID,"detalle_cboUso")
        select_uso = esperar_elemento(driver, select_element_uso_locator, 1 ,3)
        select_element_uso = Select(select_uso)
        select_element_uso.select_by_value("1")
    else:
        select_element_uso_locator = (By.ID,"detalle_cboUso")
        select_uso = esperar_elemento(driver, select_element_uso_locator, 1 ,3)
        select_element_uso = Select(select_uso)
        select_element_uso.select_by_value("2")


 # Rut
    rut_locator = (By.ID, "detalle_txtRut")
    RUT = esperar_elemento(driver, rut_locator, 1 , 3)
    RUT.send_keys(datos["rut"])
    RUT.send_keys(Keys.ENTER)
    espera_carga_completa(driver)
 
 # Nombre
    nombre_locator = (By.ID, "detalle_txtAuxNombres")
    NOMBRE = esperar_elemento(driver, nombre_locator, 1 , 3)
    if NOMBRE.is_enabled():
        nombre_contratante = datos["nombre_contratante"]
        apellido_contratante = datos["apellido_contratante"]
        NOMBRE.send_keys(nombre_contratante + apellido_contratante)
    else:
        pass

 # Comuna 
    comuna_deseada = datos["comuna"]
    comuna_locator = (By.ID, "detalle_cboComuna")
    COMUNA = esperar_elemento(driver, comuna_locator,1,2,3)
    hacer_clic_elemento_con_reintentos(driver, COMUNA)
    opciones_comuna = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#detalle_cboComuna option"))
    )
    opciones_ordenadas = sorted(opciones_comuna, key=lambda x: unidecode(x.text.strip().lower()))
    print("Opciones disponibles de comuna:")
    for opcion_comuna in opciones_ordenadas:
        print(opcion_comuna.text.strip())
    mejor_coincidencia_comuna = max(opciones_ordenadas, key=lambda opcion: unidecode(opcion.text.strip().lower()).startswith(unidecode(comuna_deseada.lower())))
    hacer_clic_elemento_con_reintentos(driver, mejor_coincidencia_comuna)
    print(f"Se seleccionó la comuna deseada: {mejor_coincidencia_comuna.text.strip()}")

    espera_carga_completa(driver)

 # Botón cotizar
    boton_cotizar_locator = (By.ID, "detalle_btnCotizar")
    COTIZAR = esperar_elemento (driver, boton_cotizar_locator, 1 , 2,3)
    hacer_clic_elemento_con_reintentos(driver, COTIZAR) 

 # Botón comprar
    boton_comprar_locator = (By.ID, "detalle_btnComprar")
    esperar_elemento(driver, boton_comprar_locator,1,2,3, max_intentos=50)

    #.. Scrollear pag
    driver.execute_script("window.scrollTo(0, window.scrollY + 500)")

    #.. Pantallazo
    timestamp = time.strftime("%Y%m%d_%H%M%S")  # Agrega un timestamp para hacer el nombre único
    cliente_nombre = datos['nombre_contratante']  # Usa el nombre del cliente como parte del nombre del archivo
    screenshot_path = os.path.join(directorio_actual, "..", "Imagenes", f"captura_{cliente_nombre}_{timestamp}_ZURICH.png")
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