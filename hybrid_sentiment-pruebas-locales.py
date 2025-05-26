import os, sys , re
sys.path.append(os.path.dirname(__file__))  # para detectar keyword_matcher.py

import spacy, json
from nlp_training.keyword_matcher import create_keyword_matcher

# Ruta a tu JSON de patrones (ajusta si está en otro lugar)
PATTERNS_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "./nlp_training/patterns.json")
)

# 1) Pipeline de reglas: solo keyword_matcher
nlp_rules = spacy.load("es_core_news_lg")
nlp_rules.add_pipe(
    "keyword_matcher",
    name="rules_matcher",
    config={"patterns_path": PATTERNS_PATH},
    first=True
)

# 2) Pipeline del modelo: tu modelo + keyword_matcher
# MODEL_PATH = os.path.abspath(
#     os.path.join(os.path.dirname(__file__), "../BACKEND/models/sentiment_transformer/model-best")
MODEL_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../BACKEND/models/sentiment/model-last")
)
try:
    modelo_sentiment = spacy.load(MODEL_PATH)
    modelo_sentiment.add_pipe(
        "keyword_matcher",
        name="model_matcher",
        config={"patterns_path": PATTERNS_PATH},
        first=True
    )
    print(f"✅ Modelo de sentimiento cargado: {MODEL_PATH}")
    print("  Pipeline modelo:", modelo_sentiment.pipe_names)
    MODELO_DISPONIBLE = True
except Exception as e:
    print(f"❌ No se pudo cargar el modelo entrenado: {e}")
    MODELO_DISPONIBLE = False

# --- LISTAS DE PALABRAS PARA REGLAS ---

# Carga el lexicón de tu archivo JSON
with open(PATTERNS_PATH, encoding="utf8") as f:
    lexicon = json.load(f)

# Asegúrate de que tu JSON tenga estas keys:
print("Patrones cargados:", lexicon.keys())
print("Positivas ejemplo:", lexicon["positivo"][:5])
print("Negativas ejemplo:", lexicon["negativo"][:5])
print("Neutrales ejemplo:", lexicon["neutral"][:5])

palabras_positivas = set(lexicon.get("positivo", []))
palabras_negativas = set(lexicon.get("negativo", []))
palabras_neutrales = set(lexicon.get("neutral", []))



# --- FUNCIONES DE REGLAS ---   

def analizar_sentimiento_reglas(texto):
    """
    Usa nlp_rules con keyword_matcher para devolver
    la etiqueta y confianza según patrones.
    """
    doc = nlp_rules(texto.lower())
    # doc.cats tiene {'positivo': x, 'negativo': y, 'neutral': z}
    label, score = max(doc.cats.items(), key=lambda x: x[1])
    return label, score


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


# Si quieres un alias más claro:
nlp_base = nlp_rules


# --- COMBINACIÓN HÍBRIDA ---
def analizar_sentimiento(texto, peso_modelo=0.4):
    texto_lc = texto.lower()
    count_pos, count_neu, count_neg = 0, 0, 0

    # Caso explícito “no es X”
    m = re.search(
        r'\bno (?:es|fue|estuvo|me parece|jamás|nunca|no me pareció(?:ó)?|resultó?)\s+([^\s\.,]+)',
        texto_lc
    )
    es_explicito = False
    texto_modificado = texto_lc  # Usaremos este texto para el análisis posterior
    if m:
        es_explicito = True
        palabra = m.group(1)
        token = nlp_base(palabra)[0]
        lemma = token.lemma_.lower()
        if lemma in palabras_positivas or palabra in palabras_positivas or lemma in palabras_negativas or palabra in palabras_negativas:
            # Reemplaza la frase "no fue bueno/malo" por "neutral"
            texto_modificado = re.sub(
                r'\bno (?:es|fue|estuvo|me parece|jamás|nunca|no me pareció(?:ó)?|resultó?)\s+' + re.escape(palabra),
                'neutral',
                texto_lc
            )

    # Conteo léxico
    doc_tokens = nlp_base(texto_modificado)
    for tok in doc_tokens:
        lema = tok.lemma_.lower()
        if lema in palabras_positivas:
            count_pos += 1
        elif lema in palabras_neutrales:
            count_neu += 1
        elif lema in palabras_negativas:
            count_neg += 1


    # Reglas
    regla_lab, regla_conf = analizar_sentimiento_reglas(texto_modificado)

    # Modelo
    if MODELO_DISPONIBLE:
        mod_lab, mod_conf = analizar_sentimiento_modelo(texto_modificado)
    else:
        mod_lab, mod_conf = None, None

    # Léxico dominante
    if count_pos > count_neg and count_pos > count_neu:
        lex_lab = "positivo"
    elif count_neg > count_pos and count_neg > count_neu:
        lex_lab = "negativo"
    elif count_neu > 0:
        lex_lab = "neutral"
    else:
        lex_lab = None

    # Votación
    votos = {}
    for lab in [regla_lab, mod_lab, lex_lab]:
        if lab:
            votos[lab] = votos.get(lab, 0) + 1

    max_votos = max(votos.values())
    candidatos = [k for k, v in votos.items() if v == max_votos]

    if len(candidatos) == 1:
        final = candidatos[0]
    else:
        # Desempate por score ponderado entre reglas y modelo
        score_reglas = regla_conf if regla_conf is not None else 0.0
        score_modelo = mod_conf if mod_conf is not None else 0.0
        score_ponderado = (1 - peso_modelo) * score_reglas + peso_modelo * score_modelo
        # Elige la etiqueta del sistema con mayor score ponderado
        if score_ponderado >= 0.5:
            final = regla_lab
        else:
            final = mod_lab

    # Diccionario de votos individuales
    votos_detalle = {
        "reglas": regla_lab,
        "modelo": mod_lab,
        "lexico": lex_lab
    }
    scores_detalle = {
        "reglas": regla_conf,
        "modelo": mod_conf,
        "lexico": {
            "positivo": count_pos,
            "neutral": count_neu,
            "negativo": count_neg
        }
    }
    return final, votos_detalle, scores_detalle, votos

# --- MODO INTERACTIVO / PRUEBA ---
if __name__ == "__main__":
    print("=== Analizador de Sentimiento Híbrido ===")
    while True:
        text = input("\nEscribe un comentario (o 'salir'): ")
        if text.strip().lower() in {"salir","exit","quit","q"}:
            break
        final, votos_detalle, scores_detalle, votos = analizar_sentimiento(text)
        print(f"→ Reglas:  {votos_detalle['reglas']} ({(scores_detalle['reglas'] if scores_detalle['reglas'] is not None else 0.0):.2f})")
        if MODELO_DISPONIBLE:
            print(f"→ Modelo:  {votos_detalle['modelo']} ({(scores_detalle['modelo'] if scores_detalle['modelo'] is not None else 0.0):.2f})")
        print(f"→ Léxico:  {votos_detalle['lexico']} (pos:{scores_detalle['lexico']['positivo']}, neu:{scores_detalle['lexico']['neutral']}, neg:{scores_detalle['lexico']['negativo']})")
        print(f"→ Votos:   {votos}")
        print(f"→ Final:   {final}")
