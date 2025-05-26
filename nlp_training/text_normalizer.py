# nlp_training/text_normalizer.py

from spellchecker import SpellChecker
import json
from unidecode import unidecode
from nlp_training.manual_overrides import manual_map
import difflib

spell = SpellChecker(language="es")



# Agrega aquí los mapeos manuales que necesites
MANUAL_MAP = {
    "profe": "profesor",
    "gusto": "gustó",
    "dios": "dio",
    "classe": "clase",
    "estuco": "estuvo",
    "mor": "amor",
    "clar": "clara",
    # nlp_training/manual_overrides.py

    # faltas típicas de acento en monosílabos
    "esta": "está",
    "esta noche": "está noche",  # revisa contexto
    "mas": "más",
    "solo": "sólo",
    "si": "sí",
    "te": "té",
    "el": "él",
    "por que": "por qué",
    "porque": "porque",      # dependiendo de contexto
    "aun": "aún",
    "dificil": "difícil",
    "facil": "fácil",
    "tecnica": "técnica",
    "tecnico": "técnico",
    "politica": "política",
    # abreviaturas o jerga
    "prof": "profesor",
    "profe": "profesor",
    "dadoq": "dado que",
    "xq": "porque",
    "k": "que",
    # términos de evaluación docente
    "evaluo": "evaluó",
    "actvidad": "actividad",
    "contendo": "contenido",
    "metodologia": "metodología",
    # Muchas más según vayas detectando…


    # añade más si surge otro patrón
}

def normalize_text(text: str) -> str:
    words = text.lower().split()
    corrected = []
    for w in words:
        # 1) Corrección manual _antes_ de todo
        if w in MANUAL_MAP:
            corrected.append(MANUAL_MAP[w])
            continue

        # 2) SpellChecker sobre versión sin tildes
        w_clean = unidecode(w)
        cand = spell.correction(w_clean)

        # 3) Aceptar solo correcciones muy seguras
        if cand and cand != w:
            # (a) mismo texto solo con/ sin tildes
            if unidecode(cand) == w_clean:
                corrected.append(cand)
            else:
                # (b) Levenshtein muy alto y longitud similar
                ratio = difflib.SequenceMatcher(None, w, cand).ratio()
                if ratio > 0.9 and abs(len(cand) - len(w)) <= 1:
                    corrected.append(cand)
                else:
                    # rechazo de cambios dudosos
                    corrected.append(w)
        else:
            corrected.append(w)

    return " ".join(corrected)
