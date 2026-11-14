"""Lanzador de las nueve actividades actuales; una simulación por ejecución."""
from pathlib import Path
import argparse
import json
import subprocess
import sys


def main():
    """Lee el índice docente y ejecuta el programa del alumno con su intérprete."""
    raiz = Path(__file__).resolve().parent
    actividades = json.loads((raiz/'ACTIVIDADES.json').read_text(encoding='utf-8'))
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('caso', type=int, nargs='?', choices=range(1, 10))
    parser.add_argument('--listar', action='store_true')
    args, resto = parser.parse_known_args()
    if args.listar:
        for a in actividades:
            print(f"{a['alumno']:02d} | {a['autor']} ({a['year']}) | {a['doi']} | {a['categoria']}")
        return 0
    if args.caso is None:
        parser.print_help()
        return 0
    actividad = next(a for a in actividades if a['alumno'] == args.caso)
    comando = [sys.executable, '-X', 'utf8', str(raiz/actividad['programa']), *actividad.get('argumentos', []), *resto]
    return subprocess.run(comando, cwd=raiz, check=False).returncode


if __name__ == '__main__':
    raise SystemExit(main())
