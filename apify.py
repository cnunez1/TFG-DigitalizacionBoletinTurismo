import requests
import time

# Configuración
APIFY_API_KEY = 'your_apify_api_key'  # Reemplaza con tu API Key de Apify
PLACE_ID = 'google_place_id'  # Reemplaza con el ID del lugar de Google que deseas extraer las reseñas
APIFY_TASK_ID = 'google-reviews-scraper'  # ID del actor de Google Reviews Scraper en Apify
APIFY_API_URL = f'https://api.apify.com/v2/actor-tasks/{APIFY_TASK_ID}/execute'

# Cabeceras para la autenticación
headers = {
    'Authorization': f'ApifyToken {APIFY_API_KEY}'
}

# Parámetros del payload para ejecutar el scraper
payload = {
    'placeId': PLACE_ID,  # ID del lugar de Google (cambiar según sea necesario)
    'maxReviews': 100,  # Número máximo de reseñas a extraer
}

# Función para ejecutar el actor de Apify
def run_google_reviews_scraper():
    response = requests.post(APIFY_API_URL, json=payload, headers=headers)
    if response.status_code == 200:
        print("El actor ha sido ejecutado exitosamente.")
        return response.json()
    else:
        print(f"Error al ejecutar el actor de Apify: {response.status_code}")
        return None

# Función para obtener los resultados del actor
def get_results(run_id):
    results_url = f'https://api.apify.com/v2/acts/{APIFY_TASK_ID}/runs/{run_id}/dataset/items'
    response = requests.get(results_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al obtener los resultados: {response.status_code}")
        return None

# Función para extraer reseñas
def extract_reviews():
    # Ejecutar el actor
    print("Ejecutando el scraper de Google Reviews...")
    run_response = run_google_reviews_scraper()
    
    if run_response:
        run_id = run_response['data']['id']
        print(f"Actor iniciado, ID de ejecución: {run_id}")
        
        # Esperar a que el actor termine
        print("Esperando los resultados...")
        while True:
            results = get_results(run_id)
            if results:
                print(f"Se han extraído {len(results)} reseñas.")
                for review in results:
                    print(f"Reseña: {review['text']}")
                break
            time.sleep(5)  # Esperar 5 segundos antes de intentar obtener los resultados nuevamente

# Ejecutar el script
if __name__ == "__main__":
    extract_reviews()
