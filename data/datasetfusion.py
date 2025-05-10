import pandas as pd

# Leer los tres archivos CSV
dataset1 = pd.read_csv('dataset1.csv', encoding='utf-8')
dataset2 = pd.read_csv('dataset2.csv', encoding='utf-8')
dataset3 = pd.read_csv('dataset3.csv', encoding='utf-8')

# Fusionar los tres datasets. Usamos `ignore_index=True` para que se asignen nuevos índices
merged_data = pd.concat([dataset1, dataset2, dataset3], ignore_index=True)

# Guardar el dataset fusionado en un nuevo archivo CSV
merged_data.to_csv('merged_dataset.csv', index=False, encoding='utf-8')

print("Los datasets han sido fusionados y guardados en 'merged_dataset.csv'.")
