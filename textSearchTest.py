import pandas as pd
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Ruta a tu archivo de credenciales
client_secret_file = 'client-secret.json'

# Definir credenciales usando el archivo JSON
credentials = service_account.Credentials.from_service_account_file(
    client_secret_file, scopes=['https://www.googleapis.com/auth/cloud-platform']
)

# Construir servicio de Google Places API
service = build('places', 'v1', credentials=credentials)

query = 'restaurants in Burgos, Spain'

request_body = {
    'textQuery': query,
    'languageCode': 'es',
    'locationRestriction': {
        'rectangle': {
            'low': {'latitude': 42.28992, 'longitude': -3.82420},
            'high': {'latitude': 42.41114, 'longitude': -3.59136}
        }
    }
}

# Lista para almacenar todos los resultados
all_places = []

while True:
    # Ejecutar la solicitud
    response = service.places().searchText(body=request_body, fields='*').execute()
    
    # Agregar lugares a la lista
    if 'places' in response:
        all_places.extend(response['places'])

    # Verificar si hay más páginas
    if 'nextPageToken' in response:
        request_body['pageToken'] = response['nextPageToken']
    else:
        break  # No hay más resultados, salir del bucle

# Guardar los resultados en un CSV
if all_places:
    df = pd.DataFrame(all_places)
    df.to_csv('places.csv', index=False)
    print(f"Se encontraron {len(all_places)} lugares. Datos guardados en 'places.csv'")
else:
    print("No se encontraron lugares.")
