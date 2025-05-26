# # export_comments.py
# import json, random
# from pathlib import Path
# import os, sys
# # añade la raíz del proyecto al path
# sys.path.insert(0, os.path.abspath(os.path.join(__file__, '../../..')))
# from documentacion.evaluacion.database import db_session
# from documentacion.evaluacion.models   import Evaluacion

# DATA_DIR   = Path(__file__).parent
# TRAIN_FILE = DATA_DIR / "train.spacy.jsonl"
# DEV_FILE   = DATA_DIR / "dev.spacy.jsonl"

# all_evals = db_session.query(Evaluacion).all()
# random.shuffle(all_evals)
# split = int(len(all_evals) * 0.8)
# train_evals, dev_evals = all_evals[:split], all_evals[split:]

# def to_jsonl(e: Evaluacion):
#     return {
#       "text": e.comentario_docente,
#       "cats": {
#         "positivo": int(e.sentimiento_docente == "positivo"),
#         "neutral" : int(e.sentimiento_docente == "neutral"),
#         "negativo": int(e.sentimiento_docente == "negativo"),
#       }
#     }

# for path, items in [(TRAIN_FILE, train_evals),(DEV_FILE, dev_evals)]:
#     with open(path, "w", encoding="utf8") as f:
#         for ev in items:
#             f.write(json.dumps(to_jsonl(ev), ensure_ascii=False) + "\n")

# print(f"✅ {len(train_evals)}→{TRAIN_FILE.name}, {len(dev_evals)}→{DEV_FILE.name}")
