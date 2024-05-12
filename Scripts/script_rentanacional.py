from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from difflib import SequenceMatcher, get_close_matches
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
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

#Funciones
def esperar_carga_completa(driver, intentos=0, max_intentos=5):
    while intentos < max_intentos:
        try:
            spinner = WebDriverWait(driver, 10).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "spinner"))
            )
            print("El spinner ha desaparecido, la página ha cargado completamente.")
            return True  # La carga fue exitosa
        except TimeoutException:
            print(f"Tiempo de espera agotado. El spinner aún está presente o la página no ha cargado completamente. Intento {intentos + 1}/{max_intentos}")
            intentos += 1
            time.sleep(2)  # Espera un poco antes de intentar nuevamente
    print(f"No se pudo cargar completamente la página después de {max_intentos} intentos.")
    return False  # La carga falló

def esperar_elemento_deshabilitado(driver, elemento, intentos=0, max_intentos=5):
    while intentos < max_intentos:
        try:
            WebDriverWait(driver, 10).until_not(
                EC.element_to_be_clickable(elemento)
            )
            print("El elemento está deshabilitado. La espera ha terminado.")
            return True  # El elemento está deshabilitado
        except TimeoutException:
            print(f"El elemento aún está habilitado. Intento {intentos + 1}/{max_intentos}")
            intentos += 1
            time.sleep(2)  # Espera un poco antes de intentar nuevamente
    print("No se pudo verificar el estado del elemento después de {} intentos.".format(max_intentos))
    return False  # No se pudo verificar el estado después de varios intentos

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

# Obtener el directorio actual (donde se encuentra el script)
directorio_actual = os.path.dirname(os.path.abspath(__file__))

# Configurar el registro
log_file_path = os.path.join(directorio_actual, '..', 'Reportes','reporte_renta_nacional.txt')
logging.basicConfig(filename=log_file_path, level=logging.INFO )
sys.stdout = open(log_file_path, 'w')
sys.stderr = open(log_file_path, 'w')

try:
    # Ruta chromedriver
    ruta_chromedriver = os.path.join(directorio_actual, '..', 'chromedriver.exe')   
    service = Service(executable_path=ruta_chromedriver)
    driver = webdriver.Chrome(service=service)

 # Datos
    datos_file_path = os.path.join(directorio_actual, '..', 'Datos','datos_rentanacional.txt')
    with open(datos_file_path, 'r', encoding='utf-8') as file:
        # Lee el contenido del archivo y evalúa el diccionario
        datos_content = file.read()
        datos = eval(datos_content)
        print (datos)
    print("_____________________________________________________________________")
 
 # Registro de información
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    informe = f"Informe - Cliente: {datos['nombre_contratante']}, Apellido: {datos['apellido_contratante']}, " \
                f"Patente: {datos['patente']}, Fecha: {fecha_actual}"
    print(informe)
    print("_____________________________________________________________________")
 
 # Inicio de página Renta
    driver.maximize_window()
    driver.get("https://sgi.rentanacional.cl")

 # Credenciales
    ruta_credenciales = os.path.join(directorio_actual, '..','credenciales.json')
    # Leer el archivo JSON desde la ruta relativa
    with open(ruta_credenciales, 'r') as file:
        credentials = json.load(file)
    # Acceder a los datos
    rut = credentials['rut_rentanacional']
    password = credentials['password_rentanacional']
    
 # Rut
    rut_locator = (By.ID, "rutInput")
    Rut = esperar_elemento(driver, rut_locator, 1 , 2,3)
    Rut.send_keys(rut)

 # Pass
    password_locator = (By.ID, "passwordInput")
    Password = esperar_elemento(driver, password_locator, 1 , 2,3)
    Password.send_keys(password + Keys.ENTER)
    
    time.sleep(1)

    esperar_carga_completa(driver)
    
 # Vehiculo particular
    if datos['tipo_vehiculo'] == 'particular':
        driver.get("https://sgi.rentanacional.cl/page-simulacion-en-linea/simulador-cotizacion.php?uso=P")
        tipo_vehiculo_reporte = datos["tipo_vehiculo"]

 # Vehiculo comercial
    else:
        driver.get("https://sgi.rentanacional.cl/page-simulacion-en-linea/simulador-cotizacion.php?uso=C")
        tipo_vehiculo_reporte = datos["tipo_vehiculo"]

    time.sleep(1)
    
    esperar_carga_completa(driver)
   
    
 # Persona jurídica o natural
    label_admin_switch_locator = (By.CSS_SELECTOR, 'label[for="adminSwitchContratante"]')
    label_admin_switch = esperar_elemento(driver, label_admin_switch_locator,1)

 # Persona jurídica
    if datos["tipo_persona"] == "juridica":
        hacer_clic_elemento_con_reintentos(driver, label_admin_switch)
        print("Se selecciono persona juridica")
        #Tipo persona
        tipo_persona_reporte = datos["tipo_persona"]

 # Rut
        rut_input_locator = (By.ID, "rut-contratante")
        rut_input = esperar_elemento(driver, rut_input_locator,1,2)
        if rut_input.is_enabled():
            rut_input.send_keys(datos["rut"])  
            print(f'Nombre contratante : {datos["nombre_contratante"]} ')
        else:
            print("Rut esta deshabilitado")
            pass
         
 # Razón social
        razon_social_locator = (By.ID, "razonSocialContratante")
        razon_social_contratante = esperar_elemento(driver, razon_social_locator,1 , 2)
        if razon_social_contratante.is_enabled():
            print("Razon social esta habilitado")
            razon_social_contratante.send_keys(Keys.CONTROL + "a")
            razon_social_contratante.send_keys(datos["nombre_contratante"])  
        else:
            print("Razon social esta deshabilitada")
            pass
        
 # Campo monto
        campo_monto_locator = (By.ID, "montoRC")
        campo_monto = esperar_elemento(driver, campo_monto_locator, 1)
        hacer_clic_elemento_con_reintentos(driver, campo_monto)
           
 # Persona Natural
    else:
        #Tipo persona
        tipo_persona_reporte = datos["tipo_persona"]
        rut_input_locator = (By.ID, "rut-contratante")
        rut_input = esperar_elemento(driver, rut_input_locator, 1,2)
        if rut_input.is_enabled():
            rut_input.send_keys(datos["rut"])
            rut_input.send_keys(Keys.ENTER)
        else:
            pass

 # Nombre contratante
        nombre_contratante_input_locator = (By.ID, "nombreContratante")
        nombre_contratante_input = esperar_elemento(driver, nombre_contratante_input_locator, 1 ,2, 3)
        if nombre_contratante_input.is_enabled():
            nombre_contratante_input.send_keys(Keys.CONTROL + "a")
            nombre_contratante_input.send_keys(datos["nombre_contratante"])
        
 # Apellido    
        apellido_contratante_locator = (By.ID, "apellidoContratante1")
        apellido_contratante = esperar_elemento(driver, apellido_contratante_locator, 1,2,3)
        if apellido_contratante.is_enabled():
            apellido_contratante.send_keys(Keys.CONTROL + "a") 
            apellido_contratante.send_keys(datos["apellido_contratante"])
        else:
            pass
        
 # Esperar 
    elemento_nombre_contratante = (By.ID, "nombreContratante")
    if esperar_elemento_deshabilitado(driver, elemento_nombre_contratante,1,5):
        print("La caja de texto está deshabilitada.")
    else:
        print("La caja de texto sigue habilitada después de varios intentos.")
        
 # Auto nuevo / Auto usado
 # Auto nuevo 
    # Espera a que el elemento label_materia_asegurar_switch sea clickeable
    label_materia_asegurar_switch_locator = (By.CSS_SELECTOR, 'label[for="materiaAsegurarSwitch"]')
    label_materia_asegurar_switch = esperar_elemento(driver, label_materia_asegurar_switch_locator, 1,2)
    if datos["uso_vehiculo"] == "nuevo":
        hacer_clic_elemento_con_reintentos(driver, label_materia_asegurar_switch)
        print("Se seleccionó Auto Nuevo")
        uso_vehiculo_reporte = datos["uso_vehiculo"]
        esperar_carga_completa(driver)
        print("_____________________________________________________________________")
  
 # Marca
        try:
            elemento_barra_desplegable_locator = (By.ID, "marca")
            elemento_barra_desplegable = esperar_elemento(driver, elemento_barra_desplegable_locator, 1)
            hacer_clic_elemento_con_reintentos(driver, elemento_barra_desplegable)
            marca_select_locator = (By.XPATH, '//select[@id="marca"]/option[@value!=""][text()!="Seleccione ..."]')
            marca_select_element = esperar_elemento(driver, marca_select_locator,1 , 2)
            select = Select(driver.find_element(By.ID, "marca"))
            opciones_marca = [opcion.text for opcion in select.options]
            #Lista de marcas
            print("Opciones de la barra desplegable:")
            opciones_str = '[' + ', '.join(opciones_marca) + ']'
            print(opciones_str)
            opcion_mas_cercana_marca = get_close_matches(datos["marca_rentanacional"], opciones_marca, n=1)
            if opcion_mas_cercana_marca:
                seleccion = opcion_mas_cercana_marca[0]
                select.select_by_visible_text(seleccion)
                print(f"Opción seleccionada: {seleccion}")
 # Verificar si la elección fue exacta o no
                if seleccion == datos["marca_rentanacional"]:
                    marca_reporte = datos["marca_rentanacional"]
                    print("La elección se hizo con una coincidencia exacta.")
                else:
                    marca_reporte = seleccion
                    print("La elección se hizo con la coincidencia más cercana.")
            else:
                print("No se encontró una coincidencia cercana.")
            print("_____________________________________________________________________")
        except TimeoutException:
            print("Tiempo de espera agotado al esperar la presencia del elemento o la selección de la opción.")
        except Exception as e:
            print(f"Se produjo un error inesperado: {e}")
        
 # Modelo
        esperar_carga_completa(driver)
        elemento_barra_modelo_locator = (By.ID, "modelo")
        elemento_barra_modelo = esperar_elemento(driver, elemento_barra_modelo_locator, 1)
        hacer_clic_elemento_con_reintentos(driver,elemento_barra_modelo)
        try:
            modelo_select_locator = (By.XPATH, '//select[@id="modelo"]/option[text()!="Seleccione ..."]')
            modelo_select_element = esperar_elemento(driver, modelo_select_locator, 1)
            select_modelo = Select(elemento_barra_modelo)
            opciones_modelo = [opcion.text for opcion in select_modelo.options]
 # Lista de modelos
            print("Opciones de la barra desplegable de modelos:")
            modelo_str = '[' + ', '.join(opciones_modelo) + ']'
            print(modelo_str)
            opcion_mas_cercana_modelo = get_close_matches(datos["modelo_rentanacional"], opciones_modelo, n=1)
            if opcion_mas_cercana_modelo:
                seleccion_modelo = opcion_mas_cercana_modelo[0]
                select_modelo.select_by_visible_text(seleccion_modelo)
                print(f"Opción de modelo seleccionada: {seleccion_modelo}")
                # Verificar si la elección fue exacta o no
                if seleccion_modelo == datos["modelo_rentanacional"]:
                    print("La elección se hizo con una coincidencia exacta.")
                    modelo_reporte = datos["modelo_rentanacional"]
                else:
                    modelo_reporte = seleccion_modelo
                    print("La elección se hizo con la coincidencia más cercana.")
            else:
                print(f"No se encontró una coincidencia cercana para el modelo {datos['modelo_rentanacional']}.")


        except TimeoutException:
            print("Tiempo de espera agotado. No se pudo cargar la lista de opciones de modelos.")
        print("_____________________________________________________________________")
        
        esperar_carga_completa(driver)

 # Año vehiculo
        elemento_ano_locator = (By.ID, "year")
        elemento_ano = esperar_elemento(driver, elemento_ano_locator, 1,2)
        select_ano = Select(elemento_ano)
        opciones_ano = [opcion.text for opcion in select_ano.options]
        print(opciones_ano)
        select_ano.select_by_value(datos["ano"]) # Corregir aquí
        print("_____________________________________________________")
        print(f"Se seleccionó la opción {datos['ano']}")
        esperar_carga_completa(driver) 

 # Auto usado
 # Patente
    else: 
        patente_auto_locator = (By.ID, "patenteUsado")
        patente_auto = esperar_elemento(driver, patente_auto_locator, 1)
        patente_auto.send_keys(datos["patente"])
        campo_monto_locator = (By.ID, "montoRC")
        campo_monto = esperar_elemento(driver, campo_monto_locator, 1)
        hacer_clic_elemento_con_reintentos(driver, campo_monto)
        esperar_carga_completa(driver)
        uso_vehiculo_reporte = datos["uso_vehiculo"]
        print("_____________________________________________________________________")
       
 # Modelo
        try:
            select_element_locator = (By.CLASS_NAME, "swal2-select")
            select_element = esperar_elemento(driver, select_element_locator, 1)
            select = Select(select_element)
            try:
                select.select_by_value(datos["modelo_rentanacional"])
                print(f"Opción de modelo seleccionada directamente: {datos['modelo_rentanacional']}")
                modelo_reporte = datos["modelo"]
            except NoSuchElementException:
                print("Modelos disponibles en el cuadro de diálogo:")
                modelos_disponibles = [option.text for option in select.options][1:]  # Excluir la opción deshabilitada
                print(modelos_disponibles)
                modelo_a_buscar = datos["modelo_rentanacional"]
                best_match_modelo = max(modelos_disponibles, key=lambda modelo: SequenceMatcher(None, modelo, modelo_a_buscar).ratio())
                if best_match_modelo == modelo_a_buscar:
                    print("¡Coincidencia exacta encontrada:", best_match_modelo)
                    modelo_reporte = datos["modelo_rentanacional"]
                    
                else:
                    
                    print("Mejor match encontrado, pero no es una coincidencia exacta. Mejor match:", best_match_modelo, "Match a buscar:", modelo_a_buscar)
                    # Seleccionar la opción por el texto visible
                    opcion_a_seleccionar = best_match_modelo
                    select.select_by_visible_text(opcion_a_seleccionar)
                    modelo_reporte = best_match_modelo
            
            confirm_locator = (By.CLASS_NAME, 'swal2-confirm')
            boton_confirm = esperar_elemento(driver, confirm_locator ,1,2,3)
            hacer_clic_elemento_con_reintentos(driver, boton_confirm)
            marca_reporte = datos["marca"]
            print("_____________________________________________________________________")

        except NoSuchElementException as e:
            print("Error: El cuadro de diálogo con la lista desplegable no se encontró en la página.")
            print(f"Detalles del error: {str(e)}")

        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")
            print(f"Detalles del error: {str(e)}")

    time.sleep(1)

    esperar_carga_completa(driver)

 # Scrollear página
    driver.execute_script("window.scrollTo(0, window.scrollY + 720)")

 # Pantallazo
    timestamp = time.strftime("%Y%m%d_%H%M%S")  # Agrega un timestamp para hacer el nombre único
    cliente_nombre = datos['nombre_contratante']  # Usa el nombre del cliente como parte del nombre del archivo
    screenshot_path =   os.path.join(directorio_actual, '..', 'Imagenes',f'captura_{cliente_nombre}_{timestamp}_rentanacional.png')
    driver.save_screenshot(screenshot_path)

 # Verificación 
    #parametros = {
    #'tipo_vehiculo': tipo_vehiculo_reporte,
    #'tipo_persona': tipo_persona_reporte,
    #'uso_vehiculo': uso_vehiculo_reporte,
    #'marca': marca_reporte,
    #'modelo': modelo_reporte,
    #'ano': opciones_ano,
#}
    #ruta_archivo = os.path.join(directorio_actual, '..', 'Seleccion','seleccion_rentanacional')
    #with open(ruta_archivo, 'w') as archivo:
    #    for clave, valor in parametros.items():
    #        archivo.write(f'{clave}: {valor}\n')
    
except Exception as e:
    print(f"Error: {str(e)}")
    logging.error(f"Error: {str(e)}")
    print(traceback.format_exc())  
    logging.error(traceback.format_exc())

sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__

driver.quit()


