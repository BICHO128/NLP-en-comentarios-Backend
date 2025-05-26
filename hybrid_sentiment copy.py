
import os
import sys

# 1) Hacer que Python encuentre keyword_matcher.py y registre la fábrica
sys.path.append(os.path.dirname(__file__))
 # ejecuta @Language.factory y registra "keyword_matcher"

from nlp_training.keyword_matcher import create_keyword_matcher

import spacy

# Ruta absoluta al JSON de patrones
PATTERNS_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "patterns.json")
)

# --- CARGA DE MODELOS ---

# Modelo base para reglas (spaCy Transformer o pequeño, a tu gusto)
nlp_base = spacy.load("es_core_news_sm")

# Intentamos cargar el modelo entrenado (con tok2vec → keyword_matcher → textcat)
MODEL_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../BACKEND/models/sentiment/model-best")
)
try:
    modelo_sentiment = spacy.load(MODEL_PATH)
    print(f"✔ Modelo de sentimiento cargado: {MODEL_PATH}")
    print("  Pipeline modelo:", modelo_sentiment.pipe_names)
    MODELO_DISPONIBLE = True
except Exception as e:
    print(f"✘ No se pudo cargar el modelo entrenado: {e}")
    MODELO_DISPONIBLE = False

# --- LISTAS DE PALABRAS PARA REGLAS ---
# Listas de palabras clave
palabras_positivas=["no es"]
palabras_neutrales=[]
palabras_negativas=[]



# --- FUNCIONES DE REGLAS ---   
def detectar_negacion(token):
    negaciones = {"no","ni","nunca","jamas","tampoco","nada","sin","ningún","ninguna","ningunos", "ningunas", "apenas", "raramente", "escasamente", "difícilmente", "lejos de", "en absoluto","agresivo", "despreciable", "egoísta", "vanidoso", "pedante", "caprichoso", "mentiroso", "hipócrita", "desconsiderado", "dañino", "egocéntrico", "resentido", "maleducado", "violento", "engreído", "horrible", "tacaño", "vengativo", "negativo", "insoportable", "feo", "intolerante", "indiscreto", "farsante", "malo", "falso", "antipático", "corrupto", "terco", "aprovechador", "despiadado", "tirano", "pendenciero", "agrandado", "avaro",
    "paila", "chichipato", "chichipata", "sin dar", "sin dar nada", "canson", "cansona", "un culo", "sapo", "sapa", "perra", "perro"
    }
    if token.i > 0 and token.doc[token.i-1].text.lower() in negaciones:
        return True
    if token.i < len(token.doc)-1 and token.doc[token.i+1].text.lower() in negaciones:
        return True
    return False

def analizar_sentimiento_reglas(texto):
    texto_procesado = nlp_base(texto.lower())
    # inicializar contadores
    conteo_positivas = conteo_negativas = conteo_neutrales = 0

    # construir conjuntos de lemas (igual que antes)
    global texto_palabras_positivas, texto_palabras_negativas, texto_palabras_neutrales
    texto_palabras_positivas = {nlp_base(p)[0].lemma_ for p in palabras_positivas}
    texto_palabras_negativas = {nlp_base(p)[0].lemma_ for p in palabras_negativas}
    texto_palabras_neutrales = {nlp_base(p)[0].lemma_ for p in palabras_neutrales}

    # contar palabras clave
    for token in texto_procesado:
        lemma = token.lemma_
        if lemma in texto_palabras_positivas:
            conteo_positivas += (1 if detectar_negacion(token) else 1)
        elif lemma in texto_palabras_negativas:
            conteo_negativas += (3 if detectar_negacion(token) else 2)
        elif lemma in texto_palabras_neutrales:
            conteo_neutrales += (3 if detectar_negacion(token) else 2)

    # ─── Aquí integramos la detección extra neutral ───
    if detectar_palabras_extra_neutrales(texto_procesado):
        # ajusta el peso según tu conveniencia
        conteo_neutrales += 3

    # determinar predominante (igual que antes)
    total = conteo_positivas + conteo_negativas + conteo_neutrales or 1
    if conteo_positivas > conteo_negativas and conteo_positivas > conteo_neutrales:
        return "positivo", conteo_positivas / total
    if conteo_negativas > conteo_positivas and conteo_negativas > conteo_neutrales:
        return "negativo", conteo_negativas / total
    return "neutral", conteo_neutrales / total

# --- FUNCIÓN DE MODELO ---
def analizar_sentimiento_modelo(texto):
    if not MODELO_DISPONIBLE:
        return None, 0.0
    doc = modelo_sentiment(texto)
    # extraer etiqueta de mayor score
    etiqueta, score = max(doc.cats.items(), key=lambda x: x[1])
    # normalizar nombres
    etiqueta = etiqueta.lower()
    return etiqueta, score

# dectecta si hay palabras neutrales en le texto
def detectar_palabras_extra_neutrales(texto_procesado):
    """Identifica pistas de neutralidad para reforzar el conteo neutral."""
    palabras_extra_neutrales = [
        "pero", "aunque", "algunos", "algunas", "no hay", "sin embargo", 
        "no obstante", "por otro lado", "por una parte", "por otra parte",
        "si bien", "a pesar de", "aun así", "igualmente", "tanto como", 
        "parcialmente", "medianamente", "en parte", "a veces", 
        "ocasionalmente", "podría mejorar", "quizás", "tal vez", "posiblemente",
        "algunos aspectos", "ciertas cosas", "básico", "adecuado", "suficiente"
    ]
    text = texto_procesado.text.lower()
    # 1) Si contiene alguna de estas frases, es indicador de neutralidad
    if any(phrase in text for phrase in palabras_extra_neutrales):
        return True

    # 2) O bien, si en la misma oración hay lemas positivos y negativos
    for sent in texto_procesado.sents:
        pos_flag = any(tok.lemma_ in texto_palabras_positivas for tok in sent)
        neg_flag = any(tok.lemma_ in texto_palabras_negativas for tok in sent)
        if pos_flag and neg_flag:
            return True

    return False

# --- COMBINACIÓN HÍBRIDA ---
def analizar_sentimiento(texto, peso_modelo=0.5):
    # regla_lab, regla_conf = analizar_sentimiento_reglas(texto) sin normalizar
    # 0) Normalizar ortografía y tildes
    texto_norm = (texto)

    # 1) análisis por reglas sobre el texto corregido
    regla_lab, regla_conf = analizar_sentimiento_reglas(texto_norm)
    if MODELO_DISPONIBLE:
        # mod_lab, mod_conf = analizar_sentimiento_modelo(texto) sin normalizar
        # 2) análisis del modelo spaCy sobre el texto corregido
        mod_lab, mod_conf = analizar_sentimiento_modelo(texto_norm)
        # si coinciden o alta confianza, elegimos
        if regla_lab == mod_lab or mod_conf > 0.8 or regla_conf > 0.8:
            return regla_lab if regla_conf >= mod_conf else mod_lab
        # si no, ponderamos
        
        return mod_lab if (mod_conf * peso_modelo) > (regla_conf * (1-peso_modelo)) else regla_lab
    return regla_lab

# --- MODO INTERACTIVO / PRUEBA ---
if __name__ == "__main__":
    print("=== Analizador de Sentimiento Híbrido ===")
    while True:
        text = input("\nEscribe un comentario (o 'salir'): ")
        if text.strip().lower() in {"salir","exit","quit","q"}:
            break
        lab, conf = None, None
        # mostrar detalle
        regla, rconf = analizar_sentimiento_reglas(text)
        modelo, mconf = analizar_sentimiento_modelo(text)
        final = analizar_sentimiento(text)
        print(f"→ Reglas:  {regla} ({rconf:.2f})")
        if MODELO_DISPONIBLE:
            print(f"→ Modelo:  {modelo} ({mconf:.2f})")
        print(f"→ Final:   {final}")
