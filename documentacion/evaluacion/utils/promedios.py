from documentacion.evaluacion.models import Evaluacion
from sqlalchemy import func
from collections import defaultdict

def convertir_calificacion_a_numerica(valor: str) -> int:
    mapa = {
        "Excelente": 5,
        "Bueno": 4,
        "Regular": 3,
        "Malo": 2,
        "Pésimo": 1
    }
    return mapa.get(valor, 0)

def obtener_promedios_por_docente_y_curso(docente_id: int, curso_id: int):
    criterios = [
        "satisfaccion_general", "metodologia", "comunicacion", "material_didactico",
        "puntualidad", "respeto", "organizacion", "claridad", "retroalimentacion", "disponibilidad"
    ]

    evaluaciones = Evaluacion.query.filter_by(docente_id=docente_id, curso_id=curso_id).all()

    if not evaluaciones:
        return {"mensaje": "No se encontraron evaluaciones para ese docente y curso."}

    suma_criterios = defaultdict(int)
    cantidad = len(evaluaciones)

    for eval in evaluaciones:
        for criterio in criterios:
            valor = getattr(eval, criterio)
            suma_criterios[criterio] += convertir_calificacion_a_numerica(valor)

    promedios = {
        criterio: round(suma / cantidad, 2)
        for criterio, suma in suma_criterios.items()
    }

    promedio_general = round(sum(promedios.values()) / len(promedios), 2)

    return {
        "promedios_por_criterio": promedios,
        "promedio_general": promedio_general,
        "total_evaluaciones": cantidad
    }
