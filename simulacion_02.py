"""MATERIAL AUXILIAR DE CONTACTO 02; no es la actividad actual del alumno.

Actividad actual: ALUMNO_02.md; ejecutar: python ejecutar_caso.py 2 --animar.

Modelo escalar normalizado: no son propiedades medidas de un organismo.
El proyectil es rígido; q es la indentación global del blanco fijo.
"""
from pathlib import Path
import argparse,csv,json
import numpy as np
from motor_contacto import (COLUMNAS,integrar_contacto,completar_referencia,
                           metricas_contacto,RADIO_RELATIVO)
from animaciones import exportar_movimiento,graficar_comparacion

NUMERO='02'
TIPO='hc'
DOI='10.1115/1.3423596'
VALORES=[0.1, 0.4, 0.8]
PARAMETRO='beta'


def parametros_escenario(valor):
    """Recibe el parámetro A/B/C y devuelve constantes adimensionales de la ley."""
    p=dict(k=1.,n=1.5,beta=0.,eta=0.,d=0.,zeta=0.)
    p["beta"]=valor
    return p


def fuerza_contacto(q,v,p):
    """Ecuación del artículo: q=indentación, v=velocidad, p=constantes; retorna F."""
    q=max(float(q),0.)
    return p["k"]*q**1.5*(1+p["beta"]*v)


def solucion_analitica(datos,valor,p):
    """Construye la referencia independiente; distingue exacta, cuadratura y serie."""
    return completar_referencia(datos,TIPO,valor,k=p['k'],beta=p['beta'],eta=p['eta'])


def calcular_modelo(valor,paso=.002):
    """Integra el contacto, añade referencia y calcula métricas de un escenario."""
    p=parametros_escenario(valor)
    f=lambda q,v:fuerza_contacto(q,v,p)
    d=integrar_contacto(f,k=p['k'],n=p['n'],paso=paso,criterio='fuerza')
    d,ref=solucion_analitica(d,valor,p)
    if TIPO in ('serie','recuperacion'):
        antiguo=integrar_contacto(f,k=p['k'],n=p['n'],paso=paso,criterio='q')
        ref['e_criterio_antiguo_q0']=float(-antiguo[-1,2])
        ref['advertencia_criterio']='q=0 puede incluir fuerza atractiva; no se anima ese tramo'
    return dict(datos=d,parametros=p,referencia=ref,metricas=metricas_contacto(d,ref))


def comparar_escenarios(seleccion='todos',paso=.002):
    """Retorna un diccionario A/B/C con datos, constantes, referencia y métricas."""
    etiquetas='ABC' if seleccion=='todos' else seleccion
    return {e:calcular_modelo(VALORES['ABC'.index(e)],paso) for e in etiquetas}


def verificar():
    """Comprueba soluciones, energía, fuerzas y refinamiento; no valida un tejido."""
    errores=[]
    for valor in VALORES:
        r=calcular_modelo(valor);d=r['datos'];m=r['metricas'];ref=r['referencia']
        assert np.isfinite(d[:,:7]).all() and np.min(d[:,1])>=0
        assert np.min(d[:,3])>-1e-8 and 0<m['restitucion']<=1.000001
        assert m['error_balance_energia']<2e-5
        assert np.min(d[:,5])>-1e-8
        assert m['indentacion_maxima_sobre_R']<.06
        assert m['error_q_referencia']<2e-5,(valor,m['error_q_referencia'])
        if 'restitucion' in ref:
            assert abs(m['restitucion']-ref['restitucion'])<2e-5
        if TIPO=='serie':
            assert abs(ref['e_criterio_antiguo_q0']-ref['e_serie_orden2'])<3e-4
        if TIPO=='recuperacion':
            assert abs(d[-1,1]+valor*d[-1,2])<1e-8
            assert m['restitucion']>=ref['e_criterio_antiguo_q0']-1e-7
        errores.append(m['error_q_referencia'])
    if TIPO in ('visco','serie','recuperacion'):
        elastico=integrar_contacto(lambda q,v:q**1.5)
        elastico,limite=completar_referencia(elastico,'hertz',1.)
        assert np.max(abs(elastico[:,1]-elastico[:,7]))<2e-5
        assert abs(elastico[-1,2]+1)<1e-6
    a=calcular_modelo(VALORES[1],.002)['metricas']
    b=calcular_modelo(VALORES[1],.001)['metricas']
    refinamiento=abs(a['indentacion_maxima_L']-b['indentacion_maxima_L'])
    assert refinamiento<1e-5
    return dict(error_q_referencia=max(errores),diferencia_refinamiento=refinamiento)


def guardar_resultados(resultados,carpeta):
    """Guarda columnas, métricas y parámetros; deja vacía la serie no válida."""
    carpeta.mkdir(parents=True,exist_ok=True)
    for e,r in resultados.items():
        with (carpeta/f'escenario_{e}.csv').open('w',newline='',encoding='utf8') as f:
            writer=csv.writer(f);writer.writerow(COLUMNAS)
            writer.writerows([[float(v) if np.isfinite(v) else '' for v in fila] for fila in r['datos']])
    (carpeta/'metricas.json').write_text(json.dumps({e:r['metricas'] for e,r in resultados.items()},ensure_ascii=False,indent=2),encoding='utf8')
    meta=dict(doi=DOI,tipo=TIPO,parametro=PARAMETRO,escenarios=dict(zip('ABC',VALORES)),
              radio_sobre_L=RADIO_RELATIVO,escala='m=v0=1, q=delta/L, s=t*v0/L',
              alcance='Indentación global del blanco; perfil espacial Hertz adoptado, sin cálculo de daño celular')
    (carpeta/'parametros.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf8')


def main():
    print("MATERIAL AUXILIAR DE CONTACTO 02. Actividad actual: python ejecutar_caso.py 2 --animar (ver ALUMNO_02.md).")
    """Opciones → verificación → modelo → exportación → gráficas y animación."""
    parser=argparse.ArgumentParser(description='MATERIAL AUXILIAR DE CONTACTO; para la actividad actual consulta README.md. ' + 'Coefficient of Restitution Interpreted as Damping in Vibroimpact')
    parser.add_argument('--escenario',choices=['A','B','C','todos'],default='todos')
    parser.add_argument('--paso',type=float,default=.002)
    parser.add_argument('--salida',type=Path,default=Path('resultados')/('alumno_'+NUMERO))
    parser.add_argument('--verificar',action='store_true')
    parser.add_argument('--animar',action='store_true',help='Genera GIF del escenario B, o el único seleccionado')
    args=parser.parse_args()
    if args.verificar: print(json.dumps(dict(verificacion='OK',metricas=verificar())))
    resultados=comparar_escenarios(args.escenario,args.paso)
    guardar_resultados(resultados,args.salida)
    graficar_comparacion(NUMERO,resultados,args.salida)
    exportar_movimiento(NUMERO,resultados,args.salida,args.animar)
    print(f'Auxiliar de contacto {NUMERO}: abre {args.salida / "visor.html"}')


if __name__=='__main__':main()
