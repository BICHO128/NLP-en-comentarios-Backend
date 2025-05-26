import json
import spacy
from spacy.tokens import DocBin

def jsonl_to_spacy(input_path, output_path, lang="es"):
    nlp = spacy.blank(lang)               # modelo vacio para tokenización
    db = DocBin()                         # contenedor de ejemplos
    with open(input_path, encoding="utf8") as f_in:
        for line in f_in:
            data = json.loads(line)
            doc = nlp.make_doc(data["text"])
            doc.cats = data["cats"]       # asigna las categorías
            db.add(doc)
    db.to_disk(output_path)
    print(f"✔ Generado {output_path}")

if __name__ == "__main__":
    # Ajusta rutas si la carpeta difiere
    jsonl_to_spacy("data/train_corrected.jsonl", "data/train.spacy")
    jsonl_to_spacy("data/dev_corrected.jsonl",   "data/dev.spacy")
