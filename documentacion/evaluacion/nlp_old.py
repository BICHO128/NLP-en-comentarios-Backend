# se implementa un analizador de sentimientos en español utilizando spaCy
import spacy

# Carga del modelo de lenguaje español
nlp = spacy.load("es_core_news_sm")

def detectar_negacion(token):
    # """Detecta negaciones simples en la vecindad de un token."""
    negaciones = ["no", "ni", "nunca", "jamás", "tampoco", "nada", "sin", "ningún", "ninguna", "ningunos", "ningunas", "apenas", "raramente", "escasamente", "difícilmente", "lejos de", "en absoluto"]
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

def analizar_sentimiento(texto):
    texto_procesado = nlp(texto.lower())

    # Inicializar contadores
    conteo_positivas = 0
    conteo_negativas = 0
    conteo_neutrales = 0

    # Crear conjuntos de lemas para cada tipo de palabra clave
    global texto_palabras_positivas, texto_palabras_negativas, texto_palabras_neutrales
    texto_palabras_positivas = {nlp(palabra)[0].lemma_ if nlp(palabra) else palabra for palabra in palabras_positivas}
    texto_palabras_negativas = {nlp(palabra)[0].lemma_ if nlp(palabra) else palabra for palabra in palabras_negativas}
    texto_palabras_neutrales = {nlp(palabra)[0].lemma_ if nlp(palabra) else palabra for palabra in palabras_neutrales}

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
        return "positivo"
    elif conteo_negativas > conteo_positivas and conteo_negativas > conteo_neutrales:
        return "negativo"
    elif conteo_neutrales > conteo_positivas and conteo_neutrales > conteo_negativas:
        return "neutral"
    else:
        # Reglas de desempate
        if conteo_positivas == conteo_negativas or \
        conteo_positivas == conteo_neutrales or \
        conteo_negativas == conteo_neutrales or \
        (conteo_positivas == conteo_negativas == conteo_neutrales):
            return "neutral"
        
    
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
    "chévere clase", "estupenda metodología", "fenomenal explicación", "sensacional organización"
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
    "fatal explicación", "pésima organización", "tóxica", "tóxico", "repugnante", "perjudicial", "dañino", "falta dinamismo", "disnamismo", "no hay suficiente retroalimentación"
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
    "sugerido", "propuesto", "argumentado", "justificado", "explicado"
]   