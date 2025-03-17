import pandas as pd
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
import time

# Ruta a tu archivo de credenciales
client_secret_file = 'client-secret.json'

# Definir credenciales usando el archivo JSON
credentials = service_account.Credentials.from_service_account_file(
    client_secret_file, scopes=['https://www.googleapis.com/auth/cloud-platform']
)

# Construir servicio de Google Places API
service = build('places', 'v1', credentials=credentials)

# Cargar las coordenadas desde el archivo 'diagonales.json'
with open('diagonales.json', 'r') as f:
    coordenadas = json.load(f)

# Lista para almacenar todos los resultados
all_places = []

# Iterar sobre las coordenadas
for area in coordenadas:
    municipio = area["municipio"]
    inicio = area["inicio"]
    fin = area["fin"]
    
    query = 'restaurants'
    request_body = {
        'textQuery': query,
        'languageCode': 'es',
        'locationRestriction': {
            'rectangle': {
                'low': {'latitude': inicio[1], 'longitude': inicio[0]},  
                'high': {'latitude': fin[1], 'longitude': fin[0]}     
            }
        }
    }

    print(f"Buscando en el área de {municipio} con coordenadas {inicio} a {fin}...")

    while True:
        # Ejecutar la solicitud
        response = service.places().searchText(body=request_body, fields='*').execute()

        # Verificar si hay resultados y agregarlos a la lista
        if 'places' in response:
            for place in response['places']:
                place['municipio'] = municipio  # Agregar municipio a cada lugar
            all_places.extend(response['places'])

        # Verificar si hay más páginas
        if 'nextPageToken' in response:
            request_body['pageToken'] = response['nextPageToken']
            time.sleep(2)  # Esperar un poco para que la siguiente página cargue
        else:
            break  # No hay más resultados, salir del bucle

# Guardar los resultados en un CSV
if all_places:
    df = pd.DataFrame(all_places)
    df.to_csv('places.csv', index=False)
    print(f"Se encontraron {len(all_places)} lugares. Datos guardados en 'places.csv'.")
else:
    print("No se encontraron lugares.")
