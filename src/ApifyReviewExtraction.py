import pandas as pd
import time, os
from apify_client import ApifyClient

base_dir = os.path.join(os.path.dirname(__file__), "..", "data", "scripts_data")
os.makedirs(base_dir, exist_ok=True)

csv_file = os.path.join(base_dir, "google_reviews_agua.csv")

APIFY_TOKEN = 'apify_api_BMf8Q3ouJqM7nIqq9mUMJKe0gLOj5v3e2hF4'
ACTOR_ID = 'compass/google-maps-reviews-scraper'
campos = ["categoryName", "city", "reviewsCount", "stars", "state", "text", "title", "placeId", "url", "name"]

print(f"Iniciando el cliente de Apify con token {APIFY_TOKEN}")

client = ApifyClient(APIFY_TOKEN)
start_time = time.time()

# Actor input
run_input = {
    "placeIds": ["ChIJ-3KGQtH8RQ0Rv8z7azqFOnc"],
    "maxReviews": 99999,
    "reviewsSort": "newest",
    "personalData": True,
    "language": "es"
}

# Run the Actor
run = client.actor(ACTOR_ID).call(run_input=run_input)
filtered_data = []

dataset_items = client.dataset(run["defaultDatasetId"]).iterate_items()

for item in dataset_items:
    filtered_item = {}
    for key in campos:
        if key in item:
            filtered_item[key] = item[key]

    filtered_data.append(filtered_item)

if filtered_data:
    df = pd.DataFrame(filtered_data, columns=campos)
    
    file_exists = os.path.isfile(csv_file)
    df.to_csv(csv_file, mode='a', header=not file_exists, index=False)
    print(f"Datos agregados a {csv_file}")
else:
    print("No se encontraron reseñas para guardar.")

end_time = time.time()

execution_time = end_time - start_time
print(f"Tiempo de ejecución: {execution_time:.2f} segundos")