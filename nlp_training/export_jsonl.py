import mysql.connector
import json

# 1. Conexión a la base de datos
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Bicho777#",
    database="nlp_comentarios"  # o el nombre que uses
)
cursor = conn.cursor(dictionary=True)

# 2. Consulta de comentarios
cursor.execute("SELECT texto, sentimiento FROM comentarios")
rows = cursor.fetchall()

# 3. Escritura en JSONL
output_path = "data/all_comments.jsonl"  # relativo a nlp_training/
with open(output_path, "w", encoding="utf8") as f_out:
    for row in rows:
        text = row["texto"]
        sentimiento = row["sentimiento"].strip().lower()  # 'positivo','neutral' o 'negativo'
        cats = {"positivo": 0, "neutral": 0, "negativo": 0}
        if sentimiento in cats:
            cats[sentimiento] = 1
        else:
            # en caso de etiquetas diferentes
            continue  
        record = {"text": text, "cats": cats}
        f_out.write(json.dumps(record, ensure_ascii=False) + "\n")

# 4. Cierre de conexión
cursor.close()
conn.close()

print(f"✅ Se han exportado {len(rows)} comentarios a {output_path}")
