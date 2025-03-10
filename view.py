import geopandas as gpd
import matplotlib.pyplot as plt

# Cargar el archivo GeoJSON
municipios = gpd.read_file("municipiosBurgos.geojson")

# Visualizar el mapa
municipios.plot()
plt.title("Mapa de Municipios de Burgos")
plt.show()
