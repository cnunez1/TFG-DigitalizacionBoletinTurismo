import pandas as pd
from datetime import datetime
from dateutil import parser

def parse_fecha(fecha_str):
    try:
        fecha = parser.parse(fecha_str)
        return fecha.strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        print(f"Error parsing fecha: {fecha_str}. Error: {e}")
        return None

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
values_list = []
for _, row in df.iterrows():
    fecha_raw = sql_value(row.get("publishedAtDate", "NULL"))
    fecha_parsed = parse_fecha(fecha_raw)
    fecha = f"'{fecha_parsed}'" if fecha_parsed else "NULL"
    texto = sql_value(row.get("text", row.get("textTranslated", "NULL")))
    categoria = sql_value(row.get("categoryName", "NULL"))
    valoracion = row.get("stars", "NULL")
    placeID = sql_value(row.get("placeId", "NULL"))
    idioma = sql_value(row.get("language", "NULL"))
    respuesta = sql_value(row.get("responseFromOwnerText", "NULL"))
    genero = sql_value(row.get("reviewContext/Tipo de viaje", "NULL"))

    # Insert SQL
    value_line = f"({fecha}, {texto}, {categoria}, {valoracion}, {placeID}, {idioma}, {respuesta}, {genero}),"
    values_list.append(value_line)

with open("inserts_reseñas.sql", "w", encoding="utf-8") as f:
    f.write("\n".join(values_list))

print("Script generado con éxito.")