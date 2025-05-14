import pandas as pd
import time, os
from apify_client import ApifyClient

APIFY_TOKEN = 'apify_api_dqQjlkWTTigcB0CcwCqTs3e9K2RhJC3E4WGP'
ACTOR_ID = 'compass/google-maps-reviews-scraper'
campos = ["categoryName", "city", "reviewsCount", "stars", "state", "text", "title", "url", "name"]

print(f"Iniciando el cliente de Apify con token {APIFY_TOKEN}")

client = ApifyClient(APIFY_TOKEN)
start_time = time.time()

# Actor input
run_input = {
    "placeIds": ["ChIJcxx4lHUnRA0RAWMFXEtStOQ",
      "ChIJE0O2aVsmRA0RzOwZXEwvYNA",
      "ChIJY8aEKaQnRA0R52N57-1o4k8",
      "ChIJnU8DeGcmRA0RHx8HSVjZuZg"],  
    "maxReviews": 99999,
    "reviewsSort": "newest",
    "personalData": True 
}

# Run the Actor
run = client.actor(ACTOR_ID).call(run_input=run_input)
filtered_data = []

for item in client.dataset.iterate_items():
    filtered_item = {}
    for key in campos:
        if key in item:
            filtered_item[key] = item[key]

    filtered_data.append(filtered_item)

if filtered_data:
    df = pd.DataFrame(filtered_data)
    
    file_exists = os.path.isfile("google_reviews.csv")

    df.to_csv("google_reviews.csv", mode='a', header=not file_exists, index=False)
    print("Datos agregados a google_reviews.csv")
else:
    print("No se encontraron reseñas para guardar.")

end_time = time.time()

execution_time = end_time - start_time
print(f"Tiempo de ejecución: {execution_time:.2f} segundos")