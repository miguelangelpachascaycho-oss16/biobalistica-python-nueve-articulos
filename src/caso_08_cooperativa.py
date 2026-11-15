"""Zhang et al. 2015: dos NPs hidrofílicas guiadas por resortes móviles."""
import argparse
from bicapa_dpd import Parametros, simular
if __name__ == '__main__':
    a = argparse.ArgumentParser(description=__doc__)
    a.add_argument('--animar', action='store_true')
    a.add_argument('--numero-np', type=int, default=2, choices=[1, 2])
    a.add_argument('--velocidad', type=float, default=.7)
    a.add_argument('--pasos', type=int, default=2600)
    a.add_argument('--preparar', type=int, default=1600)
    a.add_argument('--dt', type=float, default=.003)
    a.add_argument('--semilla', type=int, default=2026)
    a.add_argument('--salida', default='resultados/caso_08')
    q = a.parse_args()
    if not (0 < q.dt <= .004 and 0 < q.pasos <= 50000 and 0 <= q.preparar <= 50000):
        a.error('Usa 0<dt<=0.004 y hasta 50000 pasos por etapa')
    print(simular(Parametros(caso=8, numero_np=q.numero_np, velocidad=q.velocidad, pasos=q.pasos, preparar=q.preparar, dt=q.dt, semilla=q.semilla), q.salida, q.animar))
