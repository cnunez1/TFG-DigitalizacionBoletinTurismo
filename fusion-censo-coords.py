import json

with open("fusion.json", "r", encoding="utf-8") as f:
    fusion_data = json.load(f)

existing_municipalities = {entry["name"] for entry in fusion_data}

with open("municipios.json", "r", encoding="utf-8") as f:
    municipios_data = json.load(f)

# Agregar los municipios faltantes con datos desconocidos
for municipio in municipios_data:
    if municipio not in existing_municipalities:
        fusion_data.append({
            "name": municipio,
            "coordinates": ["Desconocidas"],
            "population": -1
        })

# Ordenar por población (de mayor a menor)
fusion_data.sort(key=lambda x: x["population"], reverse=True)

with open("fusionado.json", "w", encoding="utf-8") as f:
    json.dump(fusion_data, f, ensure_ascii=False, indent=4)

print("Archivo fusionado.json creado y ordenado correctamente.")
