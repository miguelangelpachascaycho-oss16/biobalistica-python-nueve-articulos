"""NJP 2019: membrana elástica mínima; penetración activa, no biobalística."""
import argparse
from penetracion_activa import Parametros, simular
if __name__ == '__main__':
    a = argparse.ArgumentParser(description=__doc__)
    a.add_argument('--animar', action='store_true')
    a.add_argument('--fuerza', type=float, default=.4)
    a.add_argument('--tiempo', type=float, default=800.)
    a.add_argument('--salida', default='resultados/caso_06')
    q = a.parse_args()
    print(simular(Parametros(caso=6, actividad=q.fuerza, tiempo=q.tiempo), q.salida, q.animar))
