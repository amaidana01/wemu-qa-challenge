"""Pruebas de respuestas sueltas para SIN_FUENTE (D9).

Uso:  python -m unittest discover tests
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from evaluar import rompe_sin_fuente  # noqa: E402

# (consulta del afiliado, respuesta de Ana sin citas ni abstención, ¿debe fallar?)
CASOS = [
    ("¿El Plan Base cubre ortodoncia?", "No, el Plan Base no la cubre.", True),           # sí/no es dato
    ("¿Cuánto me reintegran?", "Te reintegran hasta $25.000.", True),
    ("¿El Plus cubre óptica?", "Está cubierto al 100%.", True),
    ("¿Me cubren los anteojos?", "¿Qué plan tenés, Base o Plus?", False),               # repregunta
    ("¿Me cubren el blanqueamiento?",
     "No encuentro esa información en el manual. Consultalo con Atención al Afiliado.", False),
    ("Quiero un turno con cardiología.", "Sí, te busco opciones. ¿Me pasás tu DNI?", False),  # no es cobertura
]


def _caso(consulta, respuesta):
    return {"conversacion": [
        {"rol": "afiliado", "texto": consulta},
        {"rol": "ana", "texto": respuesta, "citas": [], "afirmaciones": [], "abstencion": False},
    ]}


class TestSinFuente(unittest.TestCase):
    def test_respuestas(self):
        for consulta, respuesta, falla in CASOS:
            with self.subTest(respuesta=respuesta):
                self.assertEqual(rompe_sin_fuente(_caso(consulta, respuesta)), falla)


if __name__ == "__main__":
    unittest.main()
