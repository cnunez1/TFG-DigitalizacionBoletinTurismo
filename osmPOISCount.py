import json

# Cargar el archivo GeoJSON
with open("osmPOIS3.geojson", "r", encoding="utf-8") as file:
    data = json.load(file)

# Contar el número de características (POIs)
num_pois = len(data.get("features", []))

print(f"Número de POIs: {num_pois}")
