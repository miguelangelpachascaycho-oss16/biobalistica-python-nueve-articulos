"""Campello y Zohdi 2014 CMES: variabilidad sobre dinámica celular DEM.

Muestreo pequeño para aprender el flujo; no reproduce las 400 simulaciones.
"""
import argparse
import json
from pathlib import Path
import numpy as np
from celula_dem import ParametrosCelula,simular_celula,guardar_celula


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--muestras',type=int,default=3)
    parser.add_argument('--tiempo',type=float,default=2.)
    parser.add_argument('--dt',type=float,default=2e-5)
    parser.add_argument('--semilla',type=int,default=42)
    parser.add_argument('--animar',action='store_true')
    parser.add_argument('--salida',type=Path,default=Path('resultados/celular_02'))
    a=parser.parse_args()
    if not(1<=a.muestras<=6 and 0<a.dt<=2e-4 and 0<a.tiempo<=10):
        parser.error('Usa 1–6 muestras, 0<dt<=0.0002 ns y 0<tiempo<=10 ns')
    rng=np.random.default_rng(a.semilla)
    filas=[]
    for i in range(a.muestras):
        # Rangos docentes; la distribución de diámetros dentro del chorro sí sigue sigma=0.1 media.
        diametro,velocidad,ancho=rng.uniform([2.,75.,8.],[3.,125.,12.])
        p=ParametrosCelula(articulo='10.3970/cmes.2014.098.221',radio_externo=60.,
             nodos_capa=120,diametro_proyectil=float(diametro),velocidad=float(velocidad),
             ancho_chorro=float(ancho),diametros_aleatorios=True,semilla=a.semilla+i,
             presion_por_nodo=32.7e-5,critica_transversal=.1,dt=a.dt,tiempo_final=a.tiempo)
        d=simular_celula(p)
        guardar_celula(d,a.salida/f'muestra_{i+1:02d}',a.animar and i==0)
        final=d['metricas'][-1]
        filas.append([diametro,velocidad,ancho,final[4],final[5],d['metricas'][:,1].max()])
    filas=np.array(filas)
    a.salida.mkdir(parents=True,exist_ok=True)
    np.savetxt(a.salida/'muestras.csv',filas,delimiter=',',comments='',
         header='diametro_medio_nm,velocidad_nm_ns,ancho_nm,fraccion_interior_si_cerrada,DAM,u_max_nm')
    # Pocas muestras sirven para mostrar el procedimiento, no para inferencia estadística.
    resumen={'muestras':a.muestras,'semilla':a.semilla,
             'media_u_max_nm':float(filas[:,-1].mean()),
             'alcance':'Exploración didáctica reducida; no reproduce tablas de correlación del artículo'}
    (a.salida/'resumen.json').write_text(json.dumps(resumen,indent=2,ensure_ascii=False),encoding='utf8')
    print(resumen)


if __name__=='__main__':
    main()
