import pandas as pd
import matplotlib.pyplot as plt

# 1.- Cargar los DataFrames desde los archivos CSV
dfX = pd.read_csv("python/Problemas 1 y 2/Prueba 1/Datos/X.csv", sep =',')
dfY = pd.read_csv("python/Problemas 1 y 2/Prueba 1/Datos/Y.csv", sep=';')
dfZ = pd.read_csv("python/Problemas 1 y 2/Prueba 1/Datos/Z.csv", sep=',')

#2.-Normalizar datos columnas de precios 
dfY['Price'] = dfY['Price'].str.replace(',', '.') 
dfY['Price'] = dfY['Price'].astype(float)
dfX['Price'] = dfX['Price'].astype(float)
dfZ['Price'] = dfZ['Price'].astype(float)

# 3.-Como  los DataFrames tienen diferentes formatos de fecha, vamos a normalizar las fechas de los tres DataFrames
# El dfY tiene formato datatime[64] y se normalizara asi: 
dfY['Date'] = pd.to_datetime(dfY['Date'], format='%d/%m/%Y', errors='coerce').dt.normalize()
# El dfX y dfZ tienen formato iso y se normalizara asi:
for df in [dfX, dfZ]:
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.normalize()
    
#4.- Merge entre dataframes con fechas que existan en los tres DataFrames 
df_merged = dfX.merge(dfY, on='Date', how='inner', suffixes=('_X', '_Y')).merge(dfZ,on='Date',how='inner')
df_merged.rename(columns={'Price': 'Price_Z'}, inplace=True)

#5.- Precios de los equipo 1 y 2
PrecioEquipo1  = (df_merged['Price_X'] * .20) + (df_merged['Price_Y'] * .80)
PrecioEquipo2  = (df_merged['Price_X'] + df_merged['Price_Y'] + df_merged['Price_Z'] )/ 3

print("Precio del equipo 1:", PrecioEquipo1)
print("Precio del equipo 2:", PrecioEquipo2)
print("--------------------------------------------------")

df_merged['Equipo1'] = PrecioEquipo1
df_merged['Equipo2'] = PrecioEquipo2
# 5.1.- Estadísticas descriptivas de los precios de los equipos

print("Promedio del equipo 1:", PrecioEquipo1.mean())
print("Promedio del equipo 2:", PrecioEquipo2.mean())
print("--------------------------------------------------")
print("Precio maximo equipo 1:", PrecioEquipo1.max())
print("Precio maximo equipo 2:", PrecioEquipo2.max())
print("--------------------------------------------------")

# 6.- Graficar los precios de los equipos
df_merged.set_index('Date')[['Equipo1', 'Equipo2']].plot(figsize=(12,6))
plt.title('Serie de tiempo del Precio de los Equipos') 
plt.ylabel('Precio')
plt.grid(True)
plt.show()


