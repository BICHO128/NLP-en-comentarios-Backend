# ejemplo_nlp.py
from nlp_training.text_normalizer import normalize_text
from hybrid_sentiment import analizar_sentimiento

def main():
    ejemplos = [
        "El profe tiene una gran esperiencia en la meteria, susu clases son aceptavles"
    ]

    for texto in ejemplos:
        # 1) Normalizamos ortografía y acentos
        normalizado = normalize_text(texto)
        # 2) Analizamos sentimiento con tu función híbrida
        sentimiento = analizar_sentimiento(normalizado)
        print(f"Original:     {texto}")
        print(f"Normalizado:  {normalizado}")
        print(f"Sentimiento:  {sentimiento}")
        print("-" * 60)

if __name__ == "__main__":
    main()
