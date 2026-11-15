"""Campello y Zohdi 2014, cnm.2649: célula circular, reducción didáctica."""
import argparse
from pathlib import Path
from celula_dem import ParametrosCelula, simular_celula, guardar_celula


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--velocidad',type=float,choices=[50.,100.,150.],default=100.)
    parser.add_argument('--tiempo',type=float,default=2.)
    parser.add_argument('--dt',type=float,default=2e-5)
    parser.add_argument('--control',action='store_true')
    parser.add_argument('--animar',action='store_true')
    parser.add_argument('--salida',type=Path,default=Path('resultados/celular_01'))
    a=parser.parse_args()
    if not (0<a.dt<=2e-4 and 0<a.tiempo<=15):
        parser.error('dt debe estar en (0,0.0002] ns y tiempo en (0,15] ns')
    p=ParametrosCelula(velocidad=a.velocidad,tiempo_final=a.tiempo,dt=a.dt,
                       numero_proyectiles=0 if a.control else 12)
    d=simular_celula(p)
    guardar_celula(d,a.salida,a.animar)
    print({'salida':str(a.salida),'u_max_nm':float(d['metricas'][:,1].max())})


if __name__=='__main__':
    main()
