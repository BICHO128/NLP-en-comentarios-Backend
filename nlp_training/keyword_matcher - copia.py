# C:\PROYECTO DE NLP\BACKEND\nlp_training\keyword_matcher.py
from spacy.language import Language
from spacy.matcher import PhraseMatcher
import json

@Language.factory("keyword_matcher")
def create_keyword_matcher(nlp, name, patterns=None):
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    # Si no pasas patterns en config, usa estos por defecto:
    default = {
        
        "positivo": ["chévere","excelente", "bueno", "claro", "aprendí", "genial", "fantástico",
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
            "chévere clase", "estupenda metodología", "fenomenal explicación", "sensacional organización", "me cae bien", "me cae muy bien", "gran conocimiento de la materia", "gran conocimiento", "clases son inspiradoras", "su clase es inspiradora", "persona a seguir", "persona a admirar", "ligeramente entretenido", "bacano", "bacana", "chévere", "chido", "amigable", "ser de luz", "amor", "lo mejor", "hermosura", "hermoso", "bello", "bella", "precioso", "preciosa", "linda", "lindo", "bonito", "bonita", "agradable",
            "muy buena", "muy bueno", "divertido", "divertida", "divertidas", "es una chimba", "amable", "sinmpatico", "simpatica", "ejemplo a seguir", "ejemplar"
        ],
      
        "negativo": ["deficiente","flojón","malo", "confuso", "pésimo", "nada", "horrible", "terrible",
            "desagradable", "inútil", "negativo", "frustrante", "decepcionante",
            "lento", "ineficiente", "aburrido", "difícil", "problemático",
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
        ],
        
        "neutral": [
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
            "sugerido", "propuesto", "argumentado", "justificado", "explicado", "difíciles de entender", "pero", "aunque", "algunos", "algunas", "no hay", "sin embargo", "no obstante", "por otro lado", 
            "por una parte", "por otra parte", "si bien", "a pesar de", "aun así", "igualmente",
            "tanto como", "parcialmente", "medianamente", "en parte", "a veces",
            "ocasionalmente", "podría mejorar", "quizás", "tal vez", "posiblemente",
            "algunos aspectos", "ciertas cosas", "básico", "adecuado", "suficiente",
            "parchado", "relajado", "relajada", "tranquilo", "tranquila", "normalito", "normalita", "parchada", "tranqui", "relax", "tocado", "tocada", "sensible" 
        ]
    }
    # Validar que patterns sea un diccionario o convertirlo si es una cadena
    if isinstance(patterns, str):
        try:
            patterns = json.loads(patterns)  # Convierte la cadena JSON a un diccionario
        except json.JSONDecodeError:
            raise ValueError(f"El argumento 'patterns' no es un JSON válido: {patterns}")
    
    if patterns is not None and not isinstance(patterns, dict):
        raise TypeError(f"El argumento 'patterns' debe ser un diccionario o None, pero se recibió: {type(patterns)}")
    
    patterns = patterns or default
    for label, terms in patterns.items():
        docs = [nlp.make_doc(text) for text in terms]
        matcher.add(label, docs)
    def pipe(doc):
        matches = matcher(doc)
        scores = {"positivo": 0.00, "negativo": 0.00, "neutral": 0.00}
        for match_id, start, end in matches:
            label = nlp.vocab.strings[match_id]
            # Incrementa el puntaje según la categoría
            if label in scores:
                scores[label] += 1
        # Normaliza los puntajes
        total = sum(scores.values())
        if total > 0:
            for label in scores:
                scores[label] /= total
        # Asigna la categoría con mayor puntaje
        for label, score in scores.items():
            doc.cats[label] = score
        return doc
    return pipe
