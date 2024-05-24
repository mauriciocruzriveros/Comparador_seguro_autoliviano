import os
import pandas as pd
import numpy as np

directorio_actual = os.path.dirname(os.path.abspath(__file__))
print(directorio_actual)
directorio_csvs = os.path.join(directorio_actual, "Scrap")
print(directorio_csvs)

# Crear una matriz de ceros con numpy
data = np.zeros((0,15))
columnas = ["Compania", "Nombre de plan", "0UF", "3UF","5UF", "10UF","15UF","20UF", "25UF", "30UF", "35UF", "40UF", "45UF","50UF", "Otros"]
df = pd.DataFrame(data, columns=columnas)
print(df)

directorio_scrap_renta = os.path.join(directorio_csvs, "scrap_renta.csv")
directorio_scrap_liberty = os.path.join(directorio_csvs, "scrap_liberty.csv")
directorio_scrap_sura = os.path.join(directorio_csvs, "scrap_sura.csv")
directorio_scrap_reale = os.path.join(directorio_csvs, "scrap_reale.csv")
directorio_scrap_ans = os.path.join(directorio_csvs, "scrap_ans.csv")

# Renta
data_renta = pd.read_csv(directorio_scrap_renta)
data_renta['Compania'] = 'Renta'
    #.Mapeo columnas
mapeo_columnas_renta = {
    'Tipo de plan': 'Nombre de plan',
    'D-0': '0UF',
    'D-3': '3UF',
    'D-5': '5UF',
    'D-10': '10UF',
    'D-15': '15UF',
    'D-20': '20UF',
    'D-30': '30UF', 
    'Otros': 'Otros'
}
    #.Renombrar columnas 
data_renta_renombrado = data_renta.rename(columns=mapeo_columnas_renta)
    #.Rellenar valores nulos con pd.NA
data_renta_renombrado = data_renta_renombrado.fillna(pd.NA)
    #.Concatenar con DataFrame objetivo
df = pd.concat([df, data_renta_renombrado], ignore_index=True)
# print(df)


# Sura
data_sura = pd.read_csv(directorio_scrap_sura)
print(data_sura)
data_sura['Compania'] = 'Sura'
     #.Mapeo columnas
mapeo_columnas_sura = {
    'Nombre Plan': 'Nombre de plan',
    'SD': '0UF',
    'D3': '3UF',
    'D5': '5UF',
    'D10': '10UF',
    'D20': '20UF',
    'D50': '50UF', 
    'Otros': 'Otros'
}
    #.Renombrar columnas 
data_sura_renombrado = data_sura.rename(columns=mapeo_columnas_sura)
    #.Rellenar valores nulos con pd.NA
data_sura_renombrado = data_sura_renombrado.fillna(pd.NA)
    # Obtener las filas 2 y 3 del DataFrame 
filas_concatenar = data_sura_renombrado.iloc[1:3]
# Concatenar solo las filas seleccionadas con df
df = pd.concat([df, filas_concatenar], ignore_index=True)
# print(df)




#Eliminar Otros
# Filtrar las filas que tienen valores en la columna "Otros"
filas_con_otros = df[df['Otros'].notna()]
# Obtener los índices de las filas con valores en "Otros"
indices_a_eliminar = filas_con_otros.index
# Eliminar las filas con valores en "Otros" del DataFrame
df = df.drop(indices_a_eliminar)
print(df)