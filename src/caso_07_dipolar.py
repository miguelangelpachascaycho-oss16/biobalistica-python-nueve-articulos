"""JCP 2019: cadena dipolar mínima; penetración activa, no biobalística."""
import argparse
from penetracion_activa import Parametros, simular
if __name__ == '__main__':
    a = argparse.ArgumentParser(description=__doc__)
    a.add_argument('--animar', action='store_true')
    a.add_argument('--fuerza', type=float, default=.01)
    a.add_argument('--tiempo', type=float, default=12000.)
    a.add_argument('--salida', default='resultados/caso_07')
    q = a.parse_args()
    print(simular(Parametros(caso=7, actividad=q.fuerza, rigidez_reducida=0., tiempo=q.tiempo), q.salida, q.animar))
