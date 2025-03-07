import requests

overpass_url = "http://overpass-api.de/api/interpreter"

query = """
[out:json];
node
  (42.04418334407709,-3.750750137783876,42.05336128782978,-3.7368455662506728);
out;
"""

params = {'data': query}
response = requests.get(overpass_url, params=params)

if response.status_code == 200:
    try:
        data = response.json()

        for element in data['elements']:
            tags = element.get('tags', {})  # Obtener las etiquetas (si existen)

            if tags:
                lat = element['lat']
                lon = element['lon']
                print(f"Nodo con Etiquetas | Latitud: {lat}, Longitud: {lon}")
                print("   Etiquetas:", tags)
                print("-" * 50)

    except ValueError:
        print("No se pudo convertir la respuesta a formato JSON.")
else:
    print(f"Error al hacer la solicitud. Código de estado: {response.status_code}")
    print(f"Mensaje de error: {response.text}")
