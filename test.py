import geopandas as gpd
import numpy as np
from shapely.geometry import Point
import aiohttp
import asyncio
import json

API_KEY = "AIzaSyDa429OaC_9kJEEzBIRMD2Sia22eBadWpE"

# Cargar municipios desde un archivo GeoJSON
municipios_geojson = gpd.read_file("municipioscyl.geojson")

#print(municipios_geojson.columns)

async def fetch(url, session):
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
            puntos.append((punto.y, punto.x)) 
    
    return puntos

async def obtener_reviews(place_id, session):
    """Obtiene las reseñas de un lugar dado su place_id."""
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=reviews&key={API_KEY}"
    
    data = await fetch(url, session)
    
    reviews = data.get("result", {}).get("reviews", [])
    return [{"autor": r.get("author_name", "Desconocido"), "rating": r.get("rating", 0), "texto": r.get("text", "")} for r in reviews]

async def obtener_lugares(lat, lng, session):
    """Obtiene lugares cercanos y sus reseñas."""
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=2000&key={API_KEY}"
    lugares = {}

    while url:
        data = await fetch(url, session)

        for lugar in data.get("results", []):
            place_id = lugar["place_id"]
            nombre = lugar.get("name", "Desconocido")
            reviews = await obtener_reviews(place_id, session)

            lugares[place_id] = {
                "nombre": nombre,
                "reviews": reviews
            }

        # Siguiente grupo de reviews
        next_page_token = data.get("next_page_token")
        if next_page_token:
            await asyncio.sleep(2)
            url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={next_page_token}&key={API_KEY}"
        else:
            url = None

    return lugares


async def procesar_municipio(municipio, session):
    puntos = generar_puntos_dentro_municipio(municipio, num_puntos=5)  # 5 puntos de búsqueda dentro del polígono
    lugares_totales = {}

    for lat, lng in puntos:
        lugares = await obtener_lugares(lat, lng, session)
        lugares_totales.update(lugares) 

    print(f"{municipio} - {len(lugares_totales)} lugares encontrados")
    return {municipio: {"total_lugares": len(lugares_totales), "lugares": list(lugares_totales.values())}}

async def main():
    municipios = ["Villalmanzo"]  # Municipios a procesar
    
    async with aiohttp.ClientSession() as session:
        tareas = [procesar_municipio(m, session) for m in municipios]
        resultados = await asyncio.gather(*tareas)

        with open("lugares_municipios.json", "w", encoding="utf-8") as f:
            json.dump({k: v for r in resultados for k, v in r.items()}, f, ensure_ascii=False, indent=4)

    print("\nResultados guardados en: lugares_municipios.json")

asyncio.run(main())