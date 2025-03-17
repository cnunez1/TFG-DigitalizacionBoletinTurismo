import json
import unidecode
from fuzzywuzzy import process  # Para coincidencia difusa

# Normalizar nombres
def normalize_name(name):
    return unidecode.unidecode(name.strip().lower())

# Nombre más cercano
def get_closest_match(name, choices):
    match = process.extractOne(name, choices)  
    if match and match[1] > 80:  # Si la coincidencia es bastante buena (umbral de 80%)
        return match[0]
    return None 

with open('coordenadas.geojson', 'r', encoding='utf-8') as f:
    coordinates_data = json.load(f)

with open('censo.json', 'r', encoding='utf-8') as f:
    censo_data = json.load(f)

population_data = {}
municipio_names = []
combined_data = []

for entry in censo_data:
    municipio_nombre = entry['Nombre'].split('.')[0].strip()  # Obtener el nombre del municipio
    population = entry['Data'][0]['Valor']  
    normalized_name = normalize_name(municipio_nombre)  
    population_data[normalized_name] = population
    municipio_names.append(normalized_name)  

# Recorrer los datos de coordenadas y añadir la población correspondiente
for feature in coordinates_data['features']:
    municipio_nombre = feature['properties']['name']
    normalized_name = normalize_name(municipio_nombre) 
    coordinates = feature['geometry']['coordinates']
    
    matched_name = get_closest_match(normalized_name, municipio_names)
    
    if matched_name:
        population = population_data.get(matched_name)  
        combined_data.append({
            'name': municipio_nombre,
            'coordinates': coordinates,
            'population': population
        })
    else:
        print(f"Municipio {municipio_nombre} no encontrado en el censo, omitiendo.")
    
with open('fusion.json', 'w', encoding='utf-8') as f:
    json.dump(combined_data, f, ensure_ascii=False, indent=4)

print("Datos combinados guardados en 'fusion.json'")
print(f"Se han combinado {len(combined_data)} municipios con datos de población.")
