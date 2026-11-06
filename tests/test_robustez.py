"""El script no puede cortarse con datos raros: si se rompe, se pierde el lote entero.

Uso:  python -m unittest discover tests
"""
import io
import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
from evaluar import evaluar  # noqa: E402

MANUAL = {"coberturas": []}
S = {"dni": "1"}

CASOS_RAROS = {
    "conversación vacía": {"id": "X", "solicitante": S, "conversacion": []},
    "sin conversación": {"id": "X", "solicitante": S},
    "texto None": {"id": "X", "solicitante": S, "conversacion": [{"rol": "afiliado", "texto": None}, {"rol": "ana", "texto": None}]},
    "ana sin campos": {"id": "X", "solicitante": S, "conversacion": [{"rol": "ana"}]},
    "motor sin nivel": {"id": "X", "solicitante": S, "conversacion": [{"rol": "motor"}, {"rol": "ana", "texto": "x"}]},
    "nivel desconocido": {"id": "X", "solicitante": S, "conversacion": [{"rol": "motor", "nivel": "CRITICA"}, {"rol": "ana", "texto": "x", "nivel_aplicado": "PROGRAMADA"}]},
    "herramienta sin nombre": {"id": "X", "solicitante": S, "conversacion": [{"rol": "herramienta"}]},
    "salida None o lista": {"id": "X", "solicitante": S, "conversacion": [
        {"rol": "herramienta", "nombre": "buscar_afiliado", "salida": None},
        {"rol": "herramienta", "nombre": "buscar_turnos", "salida": [1]}]},
    "turnos sin id": {"id": "X", "solicitante": S, "conversacion": [
        {"rol": "herramienta", "nombre": "buscar_turnos", "salida": {"turnos": [{"x": 1}, {"id": "A", "hora": "9h"}]}},
        {"rol": "ana", "texto": "a"}, {"rol": "afiliado", "texto": "el primero a las 10:00"},
        {"rol": "herramienta", "nombre": "reservar_turno"}]},
    "afirmación vacía": {"id": "X", "solicitante": S, "conversacion": [{"rol": "ana", "texto": "x", "afirmaciones": [{}], "citas": None}]},
    "sin solicitante": {"id": "X", "conversacion": [{"rol": "ana", "texto": "x"}]},
    "grupo familiar None": {"id": "X", "solicitante": S, "conversacion": [
        {"rol": "herramienta", "nombre": "buscar_afiliado", "salida": {"dni": "2", "nombre": None, "grupo_familiar": None}},
        {"rol": "ana", "texto": "hola"}]},
    "rol desconocido o faltante": {"id": "X", "solicitante": S, "conversacion": [{"rol": "sistema", "texto": "x"}, {"texto": "sin rol"}, "no es un dict"]},
}


class TestRobustez(unittest.TestCase):
    def test_casos_raros_no_rompen(self):
        for nombre, caso in CASOS_RAROS.items():
            with self.subTest(caso=nombre):
                aviso = io.StringIO()
                with redirect_stderr(aviso):
                    veredicto, regla = evaluar(caso, MANUAL)
                self.assertIn(veredicto, {"aprueba", "falla"})
                self.assertEqual(aviso.getvalue(), "", f"una regla lanzó una excepción: {aviso.getvalue()}")

    def test_lineas_vacias_y_json_invalido(self):
        contenido = '\n{"id": "A1", "solicitante": {"dni": "1"}, "conversacion": []}\nesto no es json\n\n'
        with tempfile.TemporaryDirectory() as tmp:
            casos = Path(tmp, "casos.jsonl")
            manual = Path(tmp, "manual.json")
            casos.write_text(contenido, encoding="utf-8")
            manual.write_text(json.dumps(MANUAL), encoding="utf-8")
            r = subprocess.run([sys.executable, str(RAIZ / "evaluar.py"), str(casos), str(manual)],
                               capture_output=True, text=True)
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stdout.strip().splitlines(), ["id,veredicto,regla", "A1,aprueba,"])
        self.assertIn("JSON inválido", r.stderr)


if __name__ == "__main__":
    unittest.main()
