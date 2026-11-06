"""Compara la salida de evaluar.py contra una clave.

Uso:  python medir.py casos.jsonl manual.json clave.csv

Muestra la exactitud (veredicto + regla) y el detalle de cada discrepancia.
Herramienta de desarrollo: no forma parte de la entrega evaluada.
"""
import csv
import json
import sys

from evaluar import evaluar


def main(casos_path, manual_path, clave_path):
    manual = json.load(open(manual_path, encoding="utf-8"))
    clave = {r["id"]: (r["veredicto"], r["regla"]) for r in csv.DictReader(open(clave_path, encoding="utf-8"))}

    aciertos, errores = 0, []
    for linea in open(casos_path, encoding="utf-8"):
        caso = json.loads(linea)
        obtenido = evaluar(caso, manual)
        esperado = clave[caso["id"]]
        if obtenido == esperado:
            aciertos += 1
        else:
            errores.append((caso["id"], esperado, obtenido))

    total = aciertos + len(errores)
    print(f"Exactitud: {aciertos}/{total} ({aciertos / total:.0%})")
    for cid, esp, obt in errores:
        print(f"  {cid}: esperado {esp[0]} {esp[1] or '-'}  |  obtenido {obt[0]} {obt[1] or '-'}")
    return 0 if not errores else 1


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:4]))
