import geopandas as gpd
import json
import matplotlib.pyplot as plt
from shapely.geometry import MultiPolygon, Polygon, box, Point

# Limites de Burgos
with open("burgos.geojson", "r", encoding="utf-8") as f:
    burgos_data = json.load(f)

# Extraer MultiPolygon correctamente
polygons = []
for poly_coords in burgos_data["features"][0]["geometry"]["coordinates"]:
    shell = poly_coords[0]  # Contorno exterior
    holes = poly_coords[1:] if len(poly_coords) > 1 else []  # Hoyos internos
    polygons.append(Polygon(shell, holes))

burgos_geom = MultiPolygon(polygons)
gdf_burgos = gpd.GeoDataFrame(geometry=[burgos_geom])

# Municipios con población
with open("fusion.json", "r", encoding="utf-8") as f:
    municipios_data = json.load(f)

# Generar la cuadrícula adaptativa según la población
grid_adaptativa = []
diagonales = [] 

for municipio in municipios_data:
    nombre = municipio["name"]
    lon, lat = municipio["coordinates"]
    poblacion = municipio["population"]

    # Ajustar el número de subdivisiones
    if poblacion > 10000:  
        num_subdivisiones = 8
        divisor = num_subdivisiones
    elif poblacion > 1000:  
        num_subdivisiones = 2
        divisor = 2.5
    else:
        num_subdivisiones = 1
        divisor = num_subdivisiones

    # Definir la celda base
    cell_size = 0.03 / divisor 

    for i in range(num_subdivisiones):
        for j in range(num_subdivisiones):
            x1 = lon - 0.015 + (i * cell_size)
            y1 = lat - 0.015 + (j * cell_size)
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            cuadrado = box(x1, y1, x2, y2)

            # Agregar solo si el cuadrado está dentro de Burgos
            if burgos_geom.contains(Point(lon, lat)):
                grid_adaptativa.append(cuadrado)
                diagonales.append({
                    "municipio": nombre,
                    "inicio": [x1, y1],
                    "fin": [x2, y2]
                })

# Crear GeoDataFrame con la cuadrícula generada
gdf_grid_adaptativa = gpd.GeoDataFrame(geometry=grid_adaptativa)

fig, ax = plt.subplots(figsize=(10, 10))
gdf_burgos.plot(ax=ax, facecolor="lightgray", edgecolor="black", linewidth=1)  # Mapa de Burgos
gdf_grid_adaptativa.plot(ax=ax, facecolor="none", edgecolor="red", linewidth=0.7)

for diagonal in diagonales:
    (x1, y1) = diagonal["inicio"]
    (x2, y2) = diagonal["fin"]
    ax.plot([x1, x2], [y1, y2], color="blue", linestyle="dashed", linewidth=0.7)

plt.title("Mapa de Burgos con Cuadrícula y Diagonales")
plt.show()

with open("diagonales.json", "w", encoding="utf-8") as f:
    json.dump(diagonales, f, ensure_ascii=False, indent=4)

print(f"Se han guardado {len(diagonales)} diagonales en 'diagonales.json'.")
