# se implementa un analizador de sentimientos en español combinando reglas y modelo de IA
import spacy
import os
import sys
import numpy as np

# 1) Hacer que Python encuentre keyword_matcher.py y registre la fábrica
sys.path.append(os.path.dirname(__file__))
 # ejecuta @Language.factory y registra "keyword_matcher"

from nlp_training.keyword_matcher import create_keyword_matcher

# Carga del modelo de lenguaje español base para las reglas
#nlp_base = spacy.load('es_dep_news_trf') #es_dep_news_trf se toma 38seg por comentario
# --- CARGA DE MODELOS ---

# Modelo base para reglas (spaCy Transformer o pequeño, a tu gusto)
nlp_base = spacy.load("es_core_news_sm")

# Intentamos cargar el modelo entrenado (con tok2vec → keyword_matcher → textcat)
MODEL_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../BACKEND/models/sentiment/model-best")
)
try:
    modelo_sentiment = spacy.load(MODEL_PATH)
    print(f"✅ Modelo de sentimiento cargado: {MODEL_PATH} 🫡")
    print("  Pipeline modelo:", modelo_sentiment.pipe_names)
    MODELO_DISPONIBLE = True
except Exception as e:
    print(f"❌ No se pudo cargar el modelo entrenado: {e} 😢")
    MODELO_DISPONIBLE = False

def detectar_negacion(token):
    """Detecta negaciones simples en la vecindad de un token."""
    negaciones = ["no", "ni", "nunca", "jamás", "tampoco", "nada", "sin", "ningún", "ninguna", "ningunos", "ningunas", "apenas", "raramente", "escasamente", "difícilmente", "lejos de", "en absoluto","agresivo", "despreciable", "egoísta", "vanidoso", "pedante", "caprichoso", "mentiroso", "hipócrita", "desconsiderado", "dañino", "egocéntrico", "resentido", "maleducado", "violento", "engreído", "horrible", "tacaño", "vengativo", "negativo", "insoportable", "feo", "intolerante", "indiscreto", "farsante", "malo", "falso", "antipático", "corrupto", "terco", "aprovechador", "despiadado", "tirano", "pendenciero", "agrandado", "avaro","paila", "chichipato", "chichipata", "sin dar", "sin dar nada", "canson", "cansona", "un culo", "sapo", "sapa", "perra", "perro"
    ]
    for neg in negaciones:
        if token.i > 0 and token.doc[token.i - 1].text.lower() == neg:
            return True
        if token.i < len(token.doc) - 1 and token.doc[token.i + 1].text.lower() == neg and neg not in ["ni"]: # Evitar falsos positivos con "ni ... ni"
            return True
    return False

def detectar_palabras_extra_neutrales(texto_procesado):
    """Identifica palabras o frases que indican fuertemente neutralidad para dar más peso al sentimiento neutral"""
    palabras_extra_neutrales = [
        "pero", "aunque", "algunos", "algunas", "no hay", "sin embargo", "no obstante", "por otro lado", 
        "por una parte", "por otra parte", "si bien", "a pesar de", "aun así", "igualmente",
        "tanto como", "parcialmente", "medianamente", "en parte", "a veces",
        "ocasionalmente", "podría mejorar", "quizás", "tal vez", "posiblemente",
        "algunos aspectos", "ciertas cosas", "básico", "adecuado", "suficiente"
    ]
    
    # Buscar palabras extra neutrales en el texto
    for palabra in palabras_extra_neutrales:
        if palabra in texto_procesado.text.lower():
            return True
    
    # Buscar combinaciones de palabras positivas y negativas en la misma oración
    tiene_positiva = False
    tiene_negativa = False
    
    for sent in texto_procesado.sents:
        for token in sent:
            if token.lemma_ in texto_palabras_positivas:
                tiene_positiva = True
            elif token.lemma_ in texto_palabras_negativas:
                tiene_negativa = True
        
        # Si la misma oración contiene palabras positivas y negativas, indica balance (neutralidad)
        if tiene_positiva and tiene_negativa:
            return True
            
    return False

def analizar_sentimiento_reglas(texto):
    """Analiza el sentimiento basado en reglas (palabras clave)"""
    texto_procesado = nlp_base(texto.lower())

    # Inicializar contadores
    conteo_positivas = 0
    conteo_negativas = 0
    conteo_neutrales = 0

    # Crear conjuntos de lemas para cada tipo de palabra clave
    global texto_palabras_positivas, texto_palabras_negativas, texto_palabras_neutrales
    texto_palabras_positivas = {nlp_base(palabra)[0].lemma_ if nlp_base(palabra) else palabra for palabra in palabras_positivas}
    texto_palabras_negativas = {nlp_base(palabra)[0].lemma_ if nlp_base(palabra) else palabra for palabra in palabras_negativas}
    texto_palabras_neutrales = {nlp_base(palabra)[0].lemma_ if nlp_base(palabra) else palabra for palabra in palabras_neutrales}

    # Contar palabras clave en el texto
    for token in texto_procesado:
        texto = token.lemma_
        
        # Si el texto entra positivo y detecta negacion pongale 2, sino pongale 1
        if texto in texto_palabras_positivas:
            if detectar_negacion(token):
                conteo_negativas += 1  # Si hay negación, cuenta como negativa
            else:
                conteo_positivas += 0.5
                
        elif texto in texto_palabras_negativas:
            if detectar_negacion(token):
                conteo_negativas += 3  # Si hay negación, cuenta como negativa
            else:
                conteo_negativas += 2
                
        elif texto in texto_palabras_neutrales:
            if detectar_negacion(token):
                conteo_negativas += 3  # Si hay negación, cuenta como negativa
            else:
                conteo_neutrales += 2
    
    # Aplicar la nueva lógica para detección de neutralidad mejorada
    if detectar_palabras_extra_neutrales(texto_procesado):
        conteo_neutrales += 3
    
    # Determinar el sentimiento predominante con reglas de desempate
    if conteo_positivas > conteo_negativas and conteo_positivas > conteo_neutrales:
        return "positivo", conteo_positivas / (conteo_positivas + conteo_negativas + conteo_neutrales)
    elif conteo_negativas > conteo_positivas and conteo_negativas > conteo_neutrales:
        return "negativo", conteo_negativas / (conteo_positivas + conteo_negativas + conteo_neutrales)
    elif conteo_neutrales > conteo_positivas and conteo_neutrales > conteo_negativas:
        return "neutral", conteo_neutrales / (conteo_positivas + conteo_negativas + conteo_neutrales)
    else:
        # Reglas de desempate
        if conteo_positivas == conteo_negativas or \
        conteo_positivas == conteo_neutrales or \
        conteo_negativas == conteo_neutrales or \
        (conteo_positivas == conteo_negativas == conteo_neutrales):
            return "neutral", 0.5  # Confianza media para los casos de empate
        
    return "neutral", 0.33  # Por defecto

def analizar_sentimiento_modelo(texto):
    """Analiza el sentimiento usando el modelo de IA entrenado"""
    if not MODELO_DISPONIBLE:
        return None, 0
    
    doc = modelo_sentiment(texto)
    
    # Extraer la categoría con mayor puntuación
    if hasattr(doc, "cats") and doc.cats:
        mejor_categoria = max(doc.cats.items(), key=lambda x: x[1])
        return mejor_categoria[0], mejor_categoria[1]
    
    return None, 0

def analizar_sentimiento(texto, peso_modelo=0.6):
    """
    Combina los resultados del análisis basado en reglas y del modelo entrenado.
    
    Args:
        texto: El texto a analizar
        peso_modelo: Qué tanto peso dar al modelo (0-1), donde 1 significa confiar totalmente en el modelo
                    y 0 significa confiar totalmente en las reglas
    
    Returns:
        string: La etiqueta de sentimiento ("positivo", "negativo", "neutral")
    """
    # Obtener resultados del análisis basado en reglas
    sentimiento_reglas, confianza_reglas = analizar_sentimiento_reglas(texto)
    
    # Si el modelo está disponible, obtener su análisis
    if MODELO_DISPONIBLE:
        sentimiento_modelo, confianza_modelo = analizar_sentimiento_modelo(texto)
        
        # Normalizar las etiquetas del modelo a nuestras categorías ("positivo", "negativo", "neutral")
        # Ajusta esto según las etiquetas que tenga tu modelo entrenado
        if sentimiento_modelo in ["POSITIVE", "positive", "pos"]:
            sentimiento_modelo = "positivo"
        elif sentimiento_modelo in ["NEGATIVE", "negative", "neg"]:
            sentimiento_modelo = "negativo"
        else:
            sentimiento_modelo = "neutral"
        
        # Si hay alta confianza en alguno de los métodos, priorizarlo
        if confianza_reglas > 0.8:
            peso_modelo = min(peso_modelo, 0.4)  # Reducir influencia del modelo si las reglas tienen alta confianza
        elif confianza_modelo > 0.8:
            peso_modelo = max(peso_modelo, 0.7)  # Aumentar influencia del modelo si tiene alta confianza
        
        # Si ambos métodos coinciden, devolver ese resultado
        if sentimiento_modelo == sentimiento_reglas:
            return sentimiento_modelo
        
        # Si no coinciden, decidir en función del peso y la confianza
        if (confianza_modelo * peso_modelo) > (confianza_reglas * (1 - peso_modelo)):
            return sentimiento_modelo
        else:
            return sentimiento_reglas
    
    # Si el modelo no está disponible, usar solo las reglas
    return sentimiento_reglas

# Listas de palabras clave
palabras_positivas = [
    "excelente", "bueno", "claro", "aprendí", "genial", "fantástico",
    "maravilloso", "útil", "positivo", "agradable", "satisfactorio",
    "perfecto", "feliz", "contento", "increíble", "eficiente", "asombroso",
    "brillante", "maravilla", "espectacular", "emocionante", "grandioso",
    "inspirador", "motivador", "constructivo", "enriquecedor", "oportuno",
    "acertado", "valioso", "provechoso", "interesante", "dinámico",
    "participativo", "organizado", "bien_estructurado", "innovador",
    "creativo", "reconfortante", "dedicado", "comprometido",
    "accesible", "atento", "paciente", "guía", "facilitador",
    "experto", "conocedor", "didáctico", "ilustrativo",
    "relevante", "significativo", "fundamental", "sobresaliente", "óptimo",
    "fabuloso", "fue un buen aprendizaje", "encantador", "precioso conocimiento",
    "estimulante", "agradable experiencia", "placentero aprendizaje", "gozoso descubrimiento",
    "animado ambiente", "radiante explicación", "vibrante", "espléndido material",
    "supremo entendimiento", "culminante aprendizaje", "la clase es muy chimba, la mejor", "el docente es chimba de persona, el mejor",
    "majestuoso conocimiento", "sublime enseñanza", "admirable gestión",
    "reconocible mejora", "notable avance", "buen contenido", "apetitoso tema",
    "buen debate", "grata experiencia", "correcto enfoque", "chido curso",
    "bacano profesor", "bacana profesora","puro aprendizaje", "rico en conocimiento", "guay dinámica",
    "chévere clase", "estupenda metodología", "fenomenal explicación", "sensacional organización", "gran conocimiento", "clases son inspiradoras", "su clase es inspiradora", "persona a seguir", "persona a admirar", "ligeramente entretenido", "bacano", "bacana", "chévere", "chido", "amigable", "ser de luz", "amor", "lo mejor", "hermosura", "hermoso", "bello", "bella", "precioso", "preciosa", "linda", "lindo", "bonito", "bonita", "agradable",
    "muy buena", "muy bueno", "divertido", "divertida", "divertidas", "es una chimba", "amable", "sinmpatico", "simpatica", "ejemplo a seguir", "ejemplar"
]

palabras_negativas = [
    "malo", "confuso", "pésimo", "nada", "horrible", "terrible",
    "desagradable", "inútil", "negativo", "frustrante", "decepcionante",
    "lento", "ineficiente", "aburrido", "difícil", "problemático", "difíciles", "no explica bien", "deficiente", "incumplido", "incumplida", "no se le entiende",
    "desastroso", "horrendo", "insatisfactorio", "irritante", "molesto",
    "paupérrimo", "nefasto", "lamentable", "deplorable", "funesto",
    "no aprendí nada", "pésima enseñanza", "mal método de enseñanza", "tóxico ambiente",
    "repugnante explicación", "detestable actitud", "odioso el docente", "aborrecible evaluación",
    "infernal ritmo de la clase", "atroz organización", "espantoso material", "repelente dinámica",
    "desolador aprendizaje", "no da explicaión del tema muy bien", "falta de claridad",
    "inquietante desinterés", "desesperanzador progreso", "contraproducente actividad",
    "el docente llega tarde", "es impuntual", "llega tarde", "docente malgenioso", "improductivo", "aveces no hace nada en clase",
    "tedioso contenido", "pesado de recocha", "fastidioso", "complicado el tema",
    "engorroso proceso", "tortuoso aprendizaje", "desordenamiento del curso", "caótico ambiente",
    "inconvenientes con el horario", "desgraciado" "mala experiencia",
    "no se esfuerza", "amargo resultado", "desalentador avance",
    "sombrío panorama", "oscuro entendimiento", "feo material", "cutre presentación",
    "chafa explicación", "paila de clase", 
    "cagada evaluación", "mierda de metodología", "asco las actividades",
    "fatal explicación", "pésima organización", "tóxica", "tóxico", "repugnante", "perjudicial", "dañino", "falta dinamismo", "disnamismo", "no hay suficiente retroalimentación", "chimbo", "muy chimbo", "muy malo", "muy mala", "maluco", "maluca", "no me gusta", "lo peor", "no", "no me cae"
]

palabras_neutrales = [
    "normal", "neutral", "regular", "promedio", "suave", "aceptable", "suficiente", "estándar", "común", "ordinario", "pasable", "moderado", "tolerable",
    "simple", "sencillo", "habitual", "corriente", "típico",
    "característico", "usual", "frecuente", "general", "medio",
    "intermedio", "equilibrado", "balanceado", "el objetivo de la clase es regular", "imparcial",
    "indiferente", "indefinido", "quizás",
    "tal vez", "aparente", "supuesto", "presunto", "existente", "presente", "concreto", "específico",
    "particular", "puntual", "detallado", "observado", "percibido",
    "mencionado", "referido", "aludido", "tratado", "discutido",
    "analizado", "estudiado", "considerado", "evaluado", "interpretado",
    "entendido", "comprendido", "conocido", "informado", "descrito",
    "expresado", "manifestado", "señalado", "indicado", "mostrado",
    "revelado", "afirmado", "declarado", "expuesto", "planteado",
    "sugerido", "propuesto", "argumentado", "justificado", "explicado", "difíciles de entender", "pero", "aunque", "algunos", "algunas", "no hay", "sin embargo", "no obstante", "por otro lado", "por una parte", "por otra parte", "si bien", "a pesar de", "aun así", "igualmente",
    "tanto como", "parcialmente", "medianamente", "en parte", "a veces",
    "ocasionalmente", "podría mejorar", "quizás", "tal vez", "posiblemente",
    "algunos aspectos", "ciertas cosas", "básico", "adecuado", "suficiente",
    "parchado", "relajado", "relajada", "tranquilo", "tranquila", "normalito", "normalita", "parchada", "tranqui", "relax", "tocado", "tocada", "sensible" 
]

def mostrar_detalles_analisis(texto):
    """Muestra detalles completos del análisis para fines de depuración"""
    print(f"\nAnálisis detallado para: '{texto}'")
    
    # Análisis basado en reglas
    sentimiento_reglas, confianza_reglas = analizar_sentimiento_reglas(texto)
    print(f"- Análisis por reglas: {sentimiento_reglas} (confianza: {confianza_reglas:.2f})")
    
    # Análisis basado en modelo
    if MODELO_DISPONIBLE:
        sentimiento_modelo, confianza_modelo = analizar_sentimiento_modelo(texto)
        print(f"- Análisis por modelo: {sentimiento_modelo} (confianza: {confianza_modelo:.2f})")
    else:
        print("- Análisis por modelo: No disponible")
    
    # Análisis combinado
    sentimiento_final = analizar_sentimiento(texto)
    print(f"- Resultado final: {sentimiento_final}")
    
    return sentimiento_final

# Pruebas del analizador híbrido
if __name__ == "__main__":
    print("=== Sistema de Análisis de Sentimientos Híbrido ===")
    print("Combinando análisis basado en reglas y modelo de IA\n")
    

    print("\n=== Modo interactivo ===")
    print("Ingresa un comentario para analizar (o 'salir' para terminar):")
    
    while True:
        texto_usuario = input("> ")
        if texto_usuario.lower() in ["salir", "exit", "q", "quit"]:
            break
        
        resultado = mostrar_detalles_analisis(texto_usuario)