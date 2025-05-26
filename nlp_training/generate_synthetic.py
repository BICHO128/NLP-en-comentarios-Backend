import json
import random

# Ruta a tu JSON de patrones
PATTERNS_PATH    = "C:\\PROYECTO DE NLP\BACKEND\\nlp_training\\patterns.json"
# Archivo base y de salida
TRAIN_PATH       = "data/train.jsonl"
SYNTHETIC_PATH   = "data/train_synthetic.jsonl"

# Plantillas por sentimiento
TEMPLATES = {
    "positivo": [
        "Me pareció {term}.",
        "El comentario fue muy {term}.",
        "Realmente lo encontré {term}.",
        "Considero que esto es {term}.",
    ],
    "neutral": [
        "Me resultó {term}.",
        "El contenido estuvo {term}.",
        "En general fue {term}.",
        "El curso estuvo {term}.",
    ],
    "negativo": [
        "Fue bastante {term}.",
        "Lo encontré muy {term}.",
        "Desafortunadamente fue {term}.",
        "No me pareció más que {term}.",
    ],
}

def load_patterns(path):
    with open(path, encoding="utf8") as f:
        patterns = json.load(f)
    return patterns  # {'positivo': [...], 'neutral': [...], 'negativo': [...]}

def generate_synthetic(patterns, per_class=300):
    synthetic = []
    for label, terms in patterns.items():
        chosen = random.choices(terms, k=per_class)
        for term in chosen:
            tpl = random.choice(TEMPLATES[label])
            text = tpl.format(term=term)
            record = {
                "text": text,
                "cats": {
                    "positivo": int(label=="positivo"),
                    "neutral":  int(label=="neutral"),
                    "negativo": int(label=="negativo"),
                }
            }
            synthetic.append(record)
    random.shuffle(synthetic)
    return synthetic

def main():
    patterns = load_patterns(PATTERNS_PATH)
    synthetic = generate_synthetic(patterns, per_class=300)
    # 1) volcamos tu train original
    with open(TRAIN_PATH, encoding="utf8") as f_in, \
         open(SYNTHETIC_PATH, "w", encoding="utf8") as f_out:
        for line in f_in:
            f_out.write(line)
        # 2) luego añadimos los sintéticos
        for rec in synthetic:
            f_out.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"✔ Generados {len(synthetic)} ejemplos sintéticos en {SYNTHETIC_PATH}")

if __name__ == "__main__":
    main()
