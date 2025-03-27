import json, csv, math
from google.oauth2 import service_account
from googleapiclient.discovery import build
import time

with open("fusionado.json", "r", encoding="utf-8") as f:
    fusion_data = json.load(f)

client_secret_file = 'client-secret.json'

credentials = service_account.Credentials.from_service_account_file(
    client_secret_file, scopes=['https://www.googleapis.com/auth/cloud-platform']
)

service = build('places', 'v1', credentials=credentials)

with open("places.json", "r", encoding="utf-8") as f:
    places = json.load(f)

# Función para calcular el radio en metros dependiendo de la población
def get_search_radius(population):
    if population <= 500:
        return 1500  # 1.5 km
    elif population <= 1000:
        return 2000  # 2 km
    else:
        return 2500  # 2.5 km

# Función para realizar la búsqueda en la API
def search_pois(query, lat=None, lng=None, radius=None, next_page_token=None):
    print(f"Buscando POIs para: '{query}' en lat: {lat}, lng: {lng}, radio: {radius}m")  # DEBUG
    request_body = {
        'textQuery': query,
        'languageCode': 'es'
    }
    
    if lat is not None and lng is not None and radius is not None:
        location_restriction = {
            "rectangle": {
                "low": {
                    "latitude": lat - (radius / 111320),
                    "longitude": lng - (radius / (111320 * abs(math.cos(math.radians(lat)))))
                },
                "high": {
                    "latitude": lat + (radius / 111320),
                    "longitude": lng + (radius / (111320 * abs(math.cos(math.radians(lat)))))
                }
            }
        }
        request_body['locationRestriction'] = location_restriction
    
    if next_page_token:
        request_body['pageToken'] = next_page_token
    
    response = service.places().searchText(body=request_body, fields='places.attributions,places.id,places.displayName').execute()
    return response

# Función para cargar IDs existentes desde el archivo CSV para no añadir duplicados
def load_existing_ids(csv_filename):
    existing_ids = set()
    try:
        with open(csv_filename, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if row:  
                    existing_ids.add(row[0])
    except FileNotFoundError:
        pass
    return existing_ids

# Función para guardar los resultados en el CSV
def save_to_csv(results, csv_filename, existing_ids, municipio_name, query):
    count = 0
    with open(csv_filename, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        for result in results:
            if result['id'] not in existing_ids:
                writer.writerow([result['id'], result['displayName'], result['attributions'], result['Municipio']])
                existing_ids.add(result['id'])
                count += 1
    print(f"Municipio '{municipio_name}', Query '{query}': {count} POIs guardados")

csv_filename = "resultados.csv"
existing_ids = load_existing_ids(csv_filename)

for municipio in fusion_data:
    municipio_name = municipio["name"]
    population = municipio["population"]
    coordinates = municipio["coordinates"]
    
    # Comprobar si las coordenadas son válidas (no "Desconocidas")
    if isinstance(coordinates, list) and len(coordinates) == 2 and all(isinstance(i, (int, float)) for i in coordinates):
        # Si las coordenadas son válidas, desempaquetarlas
        lng, lat = coordinates
        radius = get_search_radius(population) if population != -1 else None
    else:
        # Si las coordenadas son desconocidas, no se aplica location_restriction
        lng, lat, radius = None, None, None
        print(f"Coordenadas desconocidas para {municipio_name}. Buscando solo por nombre.")
        
        for place in places:
            query = f"{place} in {municipio_name}" if population == -1 else place
            results = []
            next_page_token = None  

            while True:
                # Realizar la búsqueda sin location_restriction ya que las coordenadas son desconocidas
                response = search_pois(query, None, None, None, next_page_token)
                
                if 'places' in response:
                    for result in response['places']:
                        formatted_result = {
                            'id': result.get('id'),
                            'displayName': result.get('displayName'),
                            'attributions': result.get('attributions', 'No attribution available'),
                            'Municipio': municipio_name
                        }
                        results.append(formatted_result)
                
                print(f"Encontrados {len(results)} POIs en esta iteración.")  # DEBUG
                
                # Si existe un nextPageToken, esperar antes de continuar
                if 'nextPageToken' in response:
                    next_page_token = response['nextPageToken']
                    time.sleep(2)  
                else:
                    break  

            # Guardar los resultados si se han encontrado
            if results:
                save_to_csv(results, csv_filename, existing_ids, municipio_name, query)

print(f"Búsqueda de POIs finalizada. Los resultados se han guardado en {csv_filename}.")
