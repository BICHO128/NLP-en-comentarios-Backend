import spacy
from spacy.language import Language
from spacy.matcher import PhraseMatcher
import json
from pathlib import Path  # Para manejar rutas de archivos

@Language.factory("keyword_matcher")
def create_keyword_matcher(nlp: Language, name: str, patterns_path: str = None, patterns: dict = None):
    return KeywordMatcher(nlp, patterns_path=patterns_path, patterns=patterns)

class KeywordMatcher:
    def __init__(self, nlp: Language, patterns_path: str = None, patterns: dict = None):
        self.matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
        self.nlp = nlp
        if patterns_path:
            self.patterns = self._load_patterns_from_file(patterns_path)
        elif patterns:
            self.patterns = patterns
        else:
            self.patterns = self._get_default_patterns()  # Carga patrones por defecto si no se proporciona nada
        self._validate_patterns()
        self._add_patterns_to_matcher()

    def _load_patterns_from_file(self, patterns_path: str) -> dict:
        """Carga patrones desde un archivo JSON."""
        path = Path(patterns_path)
        if not path.is_file():
            raise FileNotFoundError(f"No se encontró el archivo de patrones: {patterns_path}")
        with open(path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                raise ValueError(f"El archivo de patrones no contiene JSON válido: {patterns_path}")

    def _get_default_patterns(self) -> dict:
        """Devuelve los patrones por defecto (ahora vacíos, o con patrones mínimos)."""
        return {
            "positivo": [],
            "negativo": [],
            "neutral": []
        }

    def _validate_patterns(self):
        """Valida la estructura del diccionario de patrones."""
        if not isinstance(self.patterns, dict):
            raise ValueError("Los patrones deben ser un diccionario.")
        for label, terms in self.patterns.items():
            if not isinstance(terms, list):
                raise ValueError(f"Los términos para '{label}' deben ser una lista.")
            for term in terms:
                if not isinstance(term, str):
                    raise ValueError(f"Todos los términos para '{label}' deben ser cadenas.")

    def _add_patterns_to_matcher(self):
        """Añade los patrones al PhraseMatcher."""
        for label, terms in self.patterns.items():
            docs = [self.nlp.make_doc(text) for text in terms]
            self.matcher.add(label, docs)

    def __call__(self, doc: spacy.tokens.Doc) -> spacy.tokens.Doc:
        matches = self.matcher(doc)
        scores = {"positivo": 0.0, "negativo": 0.0, "neutral": 0.0}
        for match_id, start, end in matches:
            label = self.nlp.vocab.strings[match_id]
            if label in scores:
                scores[label] += 1
        total = sum(scores.values())
        if total > 0:
            for label in scores:
                scores[label] /= total
        for label, score in scores.items():
            doc.cats[label] = score
        return doc