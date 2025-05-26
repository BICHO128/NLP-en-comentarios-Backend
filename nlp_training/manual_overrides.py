# scripts/generate_manual_map.py
import json
from unidecode import unidecode

# 1) Carga tu wordlist (un archivo con una palabra por línea)
#    Puedes usar uno de libre disponibilidad, p.ej. https://github.com/tdozat/SpanishDict
with open("spanish_wordlist.txt", encoding="utf8") as f:
    palabras = {w.strip() for w in f if w.strip()}

# 2) Genera el mapeo: cada forma caída de tildes → palabra original
manual_map = {}
for w in palabras:
    key = unidecode(w.lower())
    if key != w.lower():
        # si no colisiona con otra palabra distinta
        if key in manual_map and manual_map[key] != w:
            # conflicto: decide manualmente o mantén el más frecuente
            continue
        manual_map[key] = w.lower()

# 3) Guarda el resultado a JSON para inspección / ajuste manual
with open("nlp_training/manual_map.json", "w", encoding="utf8") as f:
    json.dump(manual_map, f, ensure_ascii=False, indent=2)

print(f"Se generaron {len(manual_map)} mapeos de tildes.")
