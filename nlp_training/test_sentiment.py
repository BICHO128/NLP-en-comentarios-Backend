# C:\PROYECTO DE NLP\BACKEND\nlp_training\test_sentiment.py

import os
import sys

# 1) Aseguramos que Python encuentre keyword_matcher.py
sys.path.append(os.path.dirname(__file__))

# 2) Importamos el módulo (no solo la función): así se registra la fábrica
import keyword_matcher

import spacy

def main():
    # 3) Ruta al modelo entrenado
    model_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../models/sentiment/model-best")
    )
    # 4) Cargamos el modelo
    nlp = spacy.load(model_dir)
    print("Pipeline original:", nlp.pipe_names)

    # # 5) Movemos nuestro matcher al final, para que corra después de textcat
    # if "keyword_matcher" in nlp.pipe_names:
    #     nlp.remove_pipe("keyword_matcher")
    # nlp.add_pipe("keyword_matcher", last=True)
    # print("Pipeline ajustado:", nlp.pipe_names)

    # 6) Probamos algunos ejemplos
    ejemplos = [
        "¡Qué flojo el curso!, no aprendí prácticamente nada.",
        "Me gustó mucho la dinámica, estuvo súper chévere.",
        "La materia es aceptable, cumple con lo básico.",
        "Lamentablemente, Ana Gabriela es decepcionante como profesora, su ritmo es lento e ineficiente en Base de Datos II."
    ]
    for txt in ejemplos:
        doc = nlp(txt)
        print(f"\nComentario: {txt}")
        print(f"Scores:    {doc.cats}")

if __name__ == "__main__":
    main()
