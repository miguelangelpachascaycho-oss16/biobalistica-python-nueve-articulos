"""Yong y Du 2023: contacto inicial de un nanotetraedro con una bicapa DOPC."""
import argparse
from bicapa_dpd import Parametros, simular
if __name__ == '__main__':
    a = argparse.ArgumentParser(description=__doc__)
    a.add_argument('--animar', action='store_true')
    a.add_argument('--velocidad', type=float, default=5.)
    a.add_argument('--pasos', type=int, default=2600)
    a.add_argument('--preparar', type=int, default=1600)
    a.add_argument('--dt', type=float, default=.002)
    a.add_argument('--semilla', type=int, default=2026)
    a.add_argument('--salida', default='resultados/caso_09')
    q = a.parse_args()
    if not (0 < q.dt <= .004 and 0 < q.pasos <= 50000 and 0 <= q.preparar <= 50000):
        a.error('Usa 0<dt<=0.004 y hasta 50000 pasos por etapa')
    print(simular(Parametros(caso=9, numero_np=1, velocidad=q.velocidad, pasos=q.pasos, preparar=q.preparar, dt=q.dt, semilla=q.semilla), q.salida, q.animar))
