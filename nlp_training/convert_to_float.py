import json

# Ruta al archivo JSONL original
input_path = "./data/dev.jsonl"
# Ruta al archivo JSONL corregido
output_path = "./data/dev_corrected.jsonl"

# Abrir el archivo original y crear uno nuevo con los valores corregidos
with open(input_path, "r", encoding="utf-8") as infile, open(output_path, "w", encoding="utf-8") as outfile:
    for line in infile:
        data = json.loads(line)
        # Convertir los valores de las categorías a float
        data["cats"] = {key: float(value) for key, value in data["cats"].items()}
        # Escribir la línea corregida en el nuevo archivo
        outfile.write(json.dumps(data, ensure_ascii=False) + "\n")

print(f"Archivo corregido guardado en: {output_path}")