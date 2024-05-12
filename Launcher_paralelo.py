import concurrent.futures
import subprocess
import os

def limpiar_directorio(ruta):
    try:
        # Obtener la lista de archivos en la ruta especificada
        archivos = os.listdir(ruta)
        for archivo in archivos:
            # Construir la ruta completa del archivo
            ruta_archivo = os.path.join(ruta, archivo)
            # Verificar si es un archivo y no un directorio
            if os.path.isfile(ruta_archivo):
                # Eliminar el archivo
                os.remove(ruta_archivo)
        print(f"Se han eliminado todos los archivos de {ruta}")
    except Exception as e:
        print(f"Error al limpiar el directorio: {e}")
# Función para ejecutar un script
def ejecutar_script(script_path):
    subprocess.run(['python', script_path])


directorio_actual = os.path.dirname(os.path.abspath(__file__))
#Ruta Scripts 
script_renta_path = os.path.join(directorio_actual, "Scripts", "script_rentanacional.py")
script_liberty_path = os.path.join(directorio_actual, "Scripts", "script_liberty.py")
script_ans_path = os.path.join(directorio_actual, "Scripts", "script_ans.py")
script_reale_path =  os.path.join(directorio_actual, "Scripts", "script_reale.py")
script_sura_path =  os.path.join(directorio_actual, "Scripts", "script_sura.py")
script_zurich_path = os.path.join(directorio_actual, "Scripts", "script_zurich.py")

#Borrar imagenes
ruta_imagenes = os.path.join(directorio_actual, ".." , "Imagenes")

limpiar_directorio(ruta_imagenes)

# Ejecutar los scripts en paralelo
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = []
    futures.append(executor.submit(ejecutar_script, script_renta_path))
    futures.append(executor.submit(ejecutar_script, script_liberty_path))
    futures.append(executor.submit(ejecutar_script, script_ans_path))
    futures.append(executor.submit(ejecutar_script, script_reale_path))
    futures.append(executor.submit(ejecutar_script, script_sura_path))
    futures.append(executor.submit(ejecutar_script, script_zurich_path))


    # Esperar a que todos los scripts terminen
    for future in concurrent.futures.as_completed(futures):
        try:
            future.result()
        except Exception as e:
            print(f'Error al ejecutar el script: {e}')

