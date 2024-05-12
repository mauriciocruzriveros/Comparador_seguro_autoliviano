import subprocess
import os

directorio_actual = os.path.dirname(os.path.abspath(__file__))

# Ruta a tus scripts
script_renta_path = os.path.join(directorio_actual, "Scripts", "script_rentanacional.py")
script_liberty_path = os.path.join(directorio_actual, "Scripts", "script_liberty.py")
script_ans_path = os.path.join(directorio_actual, "Scripts", "script_ans.py")
script_reale_path =  os.path.join(directorio_actual, "Scripts", "script_reale.py")
script_sura_path =  os.path.join(directorio_actual, "Scripts", "script_sura.py")
script_zurich_path = os.path.join(directorio_actual, "Scripts", "script_zurich.py")

# Ejecutar el primer script
subprocess.run(['python', script_renta_path])

# Ejecutar el segundo script
subprocess.run(['python', script_liberty_path])

# Ejecutar el tercer script
subprocess.run(['python', script_ans_path])

# Ejecutar el tercer script
subprocess.run(['python', script_reale_path])

# Ejecutar el tercer script
subprocess.run(['python', script_sura_path])

# Ejecutar el tercer script
subprocess.run(['python', script_zurich_path])

