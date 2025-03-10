import geopandas as gpd
import numpy as np
from shapely.geometry import Point
import aiohttp
import asyncio
import json

API_KEY = "AIzaSyDa429OaC_9kJEEzBIRMD2Sia22eBadWpE"  # Reemplaza con tu clave de API

# Cargar municipios desde un archivo GeoJSON
municipios_geojson = gpd.read_file("municipiosBurgos.geojson")

# Verifica si 'provincia' es una columna válida
print(municipios_geojson.columns)

# Si la columna 'provincia' existe, puedes filtrar por ella, si no, obtendrás todos los municipios
municipios_burgos = municipios_geojson['name'].tolist()

async def fetch(url, session):
    """Realiza una solicitud HTTP asíncrona."""
    async with session.get(url) as response:
        return await response.json()

def generar_puntos_dentro_municipio(municipio, num_puntos):
    """Genera coordenadas aleatorias dentro del polígono de un municipio."""
    poligono = municipios_geojson[municipios_geojson["name"] == municipio].geometry.values[0]
    
    puntos = []
    while len(puntos) < num_puntos:
        minx, miny, maxx, maxy = poligono.bounds
        punto = Point(np.random.uniform(minx, maxx), np.random.uniform(miny, maxy))
        if poligono.contains(punto):
            puntos.append((punto.y, punto.x))  # Lat, Lng
    
    return puntos

async def obtener_reviews(place_id, session):
    """Obtiene las reseñas de un lugar dado su place_id y cuenta cuántas reseñas tiene."""
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=reviews&key={API_KEY}"
    data = await fetch(url, session)

    reviews = data.get("result", {}).get("reviews", [])
    return len(reviews), reviews  # Devuelve la cantidad de reseñas y las reseñas

async def obtener_lugares(lat, lng, session):
    """Obtiene lugares cercanos y sus Place IDs, además de la cantidad de reseñas."""
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=5000&key={API_KEY}"
    lugares_con_reviews = []

    while url:
        data = await fetch(url, session)

        for lugar in data.get("results", []):
            place_id = lugar.get("place_id")  # Place ID del lugar

            if place_id:
                # Obtener el número de reseñas de este lugar
                num_reviews, _ = await obtener_reviews(place_id, session)

                lugares_con_reviews.append((place_id, num_reviews, lugar.get("name", "Desconocido")))

        # Siguiente grupo de lugares (paginación)
        next_page_token = data.get("next_page_token")
        if next_page_token:
            await asyncio.sleep(3)  # Ajustar el tiempo de espera si es necesario
            url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={next_page_token}&key={API_KEY}"
        else:
            url = None

    # Ordenamos los lugares por la cantidad de reseñas (de mayor a menor)
    lugares_con_reviews.sort(key=lambda x: x[1], reverse=True)
    return lugares_con_reviews

async def procesar_municipio(municipio, session):
    """Procesa un municipio, generando puntos y obteniendo los Place IDs con más reseñas."""
    puntos = generar_puntos_dentro_municipio(municipio, num_puntos=5)  # Genera 5 puntos dentro del municipio
    lugares_con_reviews_totales = []

    for lat, lng in puntos:
        lugares_con_reviews = await obtener_lugares(lat, lng, session)
        lugares_con_reviews_totales.extend(lugares_con_reviews)

    # Seleccionamos los 10 lugares con más reseñas
    lugares_con_reviews_totales = lugares_con_reviews_totales[:200]

    print(f"{municipio} - {len(lugares_con_reviews_totales)} lugares con más reseñas")
    return {municipio: {"total_lugares": len(lugares_con_reviews_totales), "lugares": lugares_con_reviews_totales}}

async def main():
    # Obtener los municipios de Burgos (suponiendo que están en la columna "name")
    municipios_burgos = municipios_geojson['name'].tolist()

    async with aiohttp.ClientSession() as session:
        tareas = [procesar_municipio(m, session) for m in municipios_burgos]
        resultados = await asyncio.gather(*tareas)

        # Guardar los resultados en un archivo JSON
        with open("lugares_con_mas_reseñas_burgos.json", "w", encoding="utf-8") as f:
            json.dump({k: v for r in resultados for k, v in r.items()}, f, ensure_ascii=False, indent=4)

    print("\nResultados guardados en: lugares_con_mas_reseñas_burgos.json")

# Ejecutar el script asíncrono
asyncio.run(main())
