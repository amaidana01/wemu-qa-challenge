"""Pruebas de respuestas sueltas del afiliado para CONFIRMACION (D6).

Uso:  python -m unittest discover tests
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from evaluar import rompe_confirmacion  # noqa: E402

OPCIONES = {"turnos": [
    {"id": "A", "dia": "lunes", "hora": "15:00"},
    {"id": "B", "dia": "martes", "hora": "09:30"},
    {"id": "C", "dia": "miércoles", "hora": "17:00"},
]}

# (respuesta del afiliado, id reservado, ¿debe fallar?)
CASOS = [
    ("Sí, el del lunes.", "A", False),
    ("¿Puede ser el del lunes?", "A", False),        # pregunta que elige una opción ofrecida
    ("El segundo", "B", False),
    ("El último", "C", False),
    ("Sí, el miércoles a las 17:00", "C", False),
    ("Dale", "A", False),                            # indeterminada: no se marca
    ("El segundo", "A", True),                       # eligió una, se reservó otra
    ("Ninguno me sirve", "A", True),                 # rechazo
    ("Prefiero otro horario", "A", True),            # pide otra opción
    ("¿No tenés algo el jueves?", "A", True),        # pregunta por un día no ofrecido
]


def _caso(respuesta, reservado):
    return {"conversacion": [
        {"rol": "herramienta", "nombre": "buscar_turnos", "entrada": {}, "salida": OPCIONES},
        {"rol": "ana", "texto": "Tengo estas opciones. ¿Cuál te sirve?"},
        {"rol": "afiliado", "texto": respuesta},
        {"rol": "herramienta", "nombre": "reservar_turno", "entrada": {"id_turno": reservado}},
    ]}


class TestConfirmacion(unittest.TestCase):
    def test_respuestas(self):
        for respuesta, reservado, falla in CASOS:
            with self.subTest(respuesta=respuesta, reservado=reservado):
                self.assertEqual(rompe_confirmacion(_caso(respuesta, reservado)), falla)

    def test_reserva_sin_respuesta(self):
        caso = _caso("x", "A")
        del caso["conversacion"][2]
        self.assertTrue(rompe_confirmacion(caso))


if __name__ == "__main__":
    unittest.main()
