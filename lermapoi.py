import pandas as pd

# Lista de archivos CSV
archivos = ["filtrado1.csv", "filtrado2.csv", "filtrado3.csv"]

# Nombre del archivo de salida
archivo_salida = "place_ids.txt"

# Abrimos el archivo en modo 'append'
with open(archivo_salida, "a", encoding="utf-8") as f:
    for archivo in archivos:
        try:
            df = pd.read_csv(archivo)
            if 'placeId' in df.columns:
                for pid in df['placeId'].dropna():
                    f.write(str(pid) + "\n")
            else:
                print(f"⚠️ La columna 'placeId' no está en {archivo}")
        except Exception as e:
            print(f"❌ Error leyendo {archivo}: {e}")

print(f"✅ place_ids guardados en {archivo_salida}")
