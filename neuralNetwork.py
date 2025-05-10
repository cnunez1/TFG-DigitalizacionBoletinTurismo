import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.metrics import TopKCategoricalAccuracy
import os

# ===========================
# 1. Cargar los archivos CSV
# ===========================
# Ruta de los archivos CSV
data_dir = "./data/lerma/"
file_names = ["dataset1.csv", "dataset2.csv", "dataset3.csv", "dataset4.csv"]

# Leer y concatenar los CSV
dfs = []
for file in file_names:
    df = pd.read_csv(os.path.join(data_dir, file))
    dfs.append(df)

# Unir todos los DataFrames en uno solo
df = pd.concat(dfs, ignore_index=True)

# Asegúrate de tener estas columnas
text_col = "text"           # columna con las reviews
target_col = "categoryName" # columna con la categoría a predecir

# Elimina filas vacías
df = df[[text_col, target_col]].dropna()

# ===========================
# 2. Preparar datos
# ===========================
X = df[text_col].astype(str).tolist()
y = df[target_col]

# Codificar categorías (ej. "Restaurante" -> 0, "Hotel" -> 1, etc.)
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)
y_cat = to_categorical(y_encoded)

# ===========================
# 3. Tokenizar texto
# ===========================
tokenizer = Tokenizer(num_words=10000, oov_token="<OOV>")
tokenizer.fit_on_texts(X)
X_seq = tokenizer.texts_to_sequences(X)
X_pad = pad_sequences(X_seq, maxlen=200)

# ===========================
# 4. Split en entrenamiento y test
# ===========================
X_train, X_test, y_train, y_test = train_test_split(X_pad, y_cat, test_size=0.2, random_state=42)

# ===========================
# 5. Modelo de red neuronal
# ===========================
model = Sequential()
model.add(Embedding(input_dim=10000, output_dim=128, input_length=200))
model.add(LSTM(64, return_sequences=False))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dense(y_cat.shape[1], activation='softmax'))

top3 = TopKCategoricalAccuracy(k=3)

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy', top3])

# ===========================
# 6. Entrenamiento
# ===========================
model.fit(X_train, y_train, epochs=15, batch_size=64, validation_data=(X_test, y_test))

# ===========================
# 7. Predicción (ejemplo)
# ===========================
def predecir_categoria(review):
    secuencia = tokenizer.texts_to_sequences([review])
    padded = pad_sequences(secuencia, maxlen=200)
    pred = model.predict(padded)

    # TOP-1
    index_top1 = pred.argmax(axis=1)[0]
    categoria_top1 = label_encoder.inverse_transform([index_top1])[0]

    # TOP-3
    top3_indices = pred[0].argsort()[-3:][::-1]
    top3_categorias = label_encoder.inverse_transform(top3_indices)
    top3_probs = pred[0][top3_indices]

    print(f"\n📝 Review: {review}")
    print(f"✅ Predicción principal: {categoria_top1}")
    print("📊 Top 3 categorías:")
    for i in range(3):
        print(f"  {i+1}. {top3_categorias[i]} ({top3_probs[i]*100:.2f}%)")

    return categoria_top1


# Ejemplo
print(predecir_categoria("El lugar es excelente, la atención increíble y la comida espectacular"))
print(predecir_categoria("No me gustan los profesores, son muy aburridos"))
print(predecir_categoria("Malas instalaciones, no volveré"))
print(predecir_categoria("El hotel es muy cómodo y la atención es buena"))
print(predecir_categoria("Falta agua"))
