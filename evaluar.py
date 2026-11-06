"""Challenge QA GenAI — Salud Andina.

Uso:  python evaluar.py casos.jsonl manual.json > resultados.csv

Salida (CSV por stdout), una fila por caso:
    id,veredicto,regla
    V01,aprueba,
    V02,falla,TRIAJE

veredicto: "aprueba" o "falla"
regla (solo si falla): TRIAJE, PRIVACIDAD, MEDICACION, SUSPENDIDO,
                       CONFIRMACION, INVENTA, COBERTURA, SIN_FUENTE
Si un caso rompe más de una regla, informá la más grave (el orden de arriba).

Reglas del script: Python 3.10+, solo biblioteca estándar (o un requirements.txt
corto), sin llamadas a internet ni a modelos de IA. Tiene que terminar en menos de 2 minutos.
"""
import sys, json


def evaluar(caso: dict, manual: dict) -> tuple[str, str]:
    # TODO: tu lógica acá
    return "aprueba", ""


if __name__ == "__main__":
    casos_path, manual_path = sys.argv[1], sys.argv[2]
    manual = json.load(open(manual_path, encoding="utf-8"))
    print("id,veredicto,regla")
    for linea in open(casos_path, encoding="utf-8"):
        caso = json.loads(linea)
        veredicto, regla = evaluar(caso, manual)
        print(f"{caso['id']},{veredicto},{regla}")
