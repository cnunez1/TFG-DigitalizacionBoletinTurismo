import pandas as pd

df = pd.read_csv("../data/lerma/dataset1.csv")

# Opcional: reemplazar NaN por NULL en SQL
df = df.fillna("NULL")

# Función para limpiar valores y poner comillas si es string
def sql_value(val):
    if val == "NULL" or pd.isna(val):
        return "NULL"
    val = str(val).replace("'", "''")  # Escapar comillas simples
    return f"'{val}'"

# Crear INSERTS
values_list = set()
for _, row in df.iterrows():
    placeID = sql_value(row['placeId'])
    municipio = sql_value(row['city'])
    nombrePOI = sql_value(row['title'])
    direccion = sql_value(row['address'])
    
    # Crear la línea de los valores
    value_line = f"({placeID}, {municipio}, {nombrePOI}, {direccion}),"
    values_list.add(value_line)

with open("inserts_pois.sql", "w", encoding="utf-8") as f:
    f.write("\n".join(values_list))

print("Script generado con éxito.")