import requests, json

url = "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/2862"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    municipios_lista = []

    for item in data:
        nombre = item["Nombre"].split(".")[0].strip() 
        if "," in nombre:
            nombre1 = nombre.split(",")[0].strip() 
            article = nombre.split(",")[1].strip() 
            nombre = f"{article} {nombre1}"
        municipios_lista.append(nombre) 

    # Convertir la lista en un conjunto para eliminar duplicados
    municipios = set(municipios_lista)

    with open("municipios.json", "w", encoding="utf-8") as file:
        json.dump(sorted(municipios), file, indent=4, ensure_ascii=False)

    print(f"Archivo 'municipios.json' generado con éxito.")
else:
    print("Error al obtener los datos:", response.status_code)

    