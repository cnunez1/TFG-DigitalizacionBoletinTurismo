import logging, os, pickle, pyodbc, json
import azure.functions as func
import tensorflow as tf
from collections import defaultdict
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Carga del modelo y objetos al inicio

ruta_base = os.path.dirname(__file__) 

modelo_path = os.path.join(ruta_base, "review_model.keras")
try:
    model = load_model(modelo_path)
except Exception as e:
    logging.error(f"Error cargando modelo: {e}")
    raise

tokenizer_path = os.path.join(ruta_base, "tokenizer.pkl")
try:
    with open(tokenizer_path, "rb") as f:
        tokenizer = pickle.load(f)
except Exception as e:
    logging.error(f"Error cargando tokenizer: {e}")
    raise

label_encoder_path = os.path.join(ruta_base, "label_encoder.pkl")
try:
    with open(label_encoder_path, "rb") as f:
        label_encoder = pickle.load(f)
except Exception as e:
    logging.error(f"Error cargando label encoder: {e}")
    raise

def predecir_categoria(texto):
    secuencia = tokenizer.texts_to_sequences([texto])
    padded = pad_sequences(secuencia, maxlen=200)
    pred = model.predict(padded, verbose=0)

    index_top1 = pred.argmax(axis=1)[0]
    categoria_top1 = label_encoder.inverse_transform([index_top1])[0]

    return categoria_top1

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Recibiendo reviews para procesar")

    try:
        reviews = req.get_json()
    except Exception as e:
        logging.error(f"Error leyendo JSON: {e}")
        return func.HttpResponse("JSON inválido", status_code=400)

    # DB connection
    server = 'ubu-reviews-dti.database.windows.net'
    database = 'reviews'
    username = 'ubuadmin'
    password = 'UBUreviews2025'
    driver = '{ODBC Driver 18 for SQL Server}'

    try:
        conn = pyodbc.connect(
            f"DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=no;Authentication=SqlPassword;TLSVersion=1.3;"
        )
        cursor = conn.cursor()
    except Exception as e:
        logging.error(f"Error conectando a la DB: {e}")
        return func.HttpResponse("Error de conexión a base de datos", status_code=500)

    respuestas = []

    reviews_por_title = defaultdict(list)
    for r in reviews:
        title = r.get("title", None)
        if title:
            reviews_por_title[title].append(r)
        else:
            # Si no tiene title
            respuestas.append({"text": r.get("text", ""), "status": "sin title, review ignorada"})

    for title, review_group in reviews_por_title.items():
        # Obtener reviews de la DB para este POI (title)
        try:
            cursor.execute("SELECT texto FROM reviews WHERE title = ?", title)
            rows = cursor.fetchall()
            textos_db = [row[0] for row in rows]
        except Exception as e:
            logging.error(f"Error consultando reviews DB para POI {title}: {e}")
            textos_db = []

        # Combinar todos los textos (DB + JSON) para predecir categoría
        textos_json = [r.get("text", "") for r in review_group if r.get("text", "")]
        textos_combinados = textos_db + textos_json
        if not textos_combinados:
            # Sin textos, saltar este POI
            for r in review_group:
                respuestas.append({"text": r.get("text", ""), "status": "no hay textos para predecir categoría"})
            continue

        # Predecir categoría para el POI usando todos los textos concatenados
        texto_concat = " ".join(textos_combinados)
        categoria_poi = predecir_categoria(texto_concat)

        # Insertar solo las reviews del JSON (input)
        for r in review_group:
            texto = r.get("text", "")
            if not texto:
                continue

            try:
                valoracion = int(r.get("stars", 0))
            except:
                valoracion = 0

            try:
                cursor.execute(
                    """
                    INSERT INTO reviews (texto, categoriaPOI, valoracion, title, nombre, genero)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    texto,
                    categoria_poi,
                    valoracion,
                    title,
                    r.get("name"),
                    r.get("genero")
                )
                conn.commit()
                respuestas.append({"text": texto, "prediccion": categoria_poi, "status": "guardado"})
            except pyodbc.Error as e:
                err_msg = str(e)
                logging.error(f"Error guardando review para POI {title}: {err_msg}")
                respuestas.append({"text": texto, "prediccion": categoria_poi, "status": f"error: {err_msg}"})

    cursor.close()
    conn.close()

    return func.HttpResponse(json.dumps(respuestas), status_code=200, mimetype="application/json")
