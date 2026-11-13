"""Aceleración por arrastre a Reynolds intermedio.

Ejemplo educativo del submodelo descrito en ALUMNO_04.md.
Los parámetros relativos son docentes; no es calibración experimental.
"""
from pathlib import Path
import argparse
import csv
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from animaciones import exportar_movimiento


def integrar_rk4(derivadas, tiempos, estado_inicial):
    """Integra y'=f(t,y). Recibe malla 1D y estado; devuelve matriz (n,m)."""
    estados = np.empty((len(tiempos), len(estado_inicial)), dtype=float)
    estados[0] = estado_inicial
    for i, dt in enumerate(np.diff(tiempos)):
        t, y = tiempos[i], estados[i]
        k1 = np.asarray(derivadas(t, y))
        k2 = np.asarray(derivadas(t + dt/2, y + dt*k1/2))
        k3 = np.asarray(derivadas(t + dt/2, y + dt*k2/2))
        k4 = np.asarray(derivadas(t + dt, y + dt*k3))
        estados[i+1] = y + dt*(k1 + 2*k2 + 2*k3 + k4)/6
    return estados



TITULO = 'Aceleración por arrastre a Reynolds intermedio'
DOI = '10.1080/21645515.2015.1029211'
PARAMETRO = 'Re0'
VALORES = [0.1, 1.0, 10.0]
COLUMNAS = ['s', 'w', 'z']
XLABEL = 'Tiempo relativo s=t/τ'
YLABEL = 'Velocidad relativa w=v/u'

def calcular_modelo(Re0):
    """Integra la ecuación de arrastre intermedio para Re0>=0."""
    if Re0 < 0:
        raise ValueError("Re0 no puede ser negativo")
    s=np.linspace(0,6,601)
    def f(t,y):
        relativa=1-y[0]
        aceleracion=relativa*(1+(Re0*abs(relativa))**(2/3)/6)
        return [aceleracion,y[0]]
    estado=integrar_rk4(f,s,[0.,0.])
    return np.column_stack((s,estado))


def verificar():
    """Re0=0 debe recuperar Stokes; verifica también cotas del caso intermedio."""
    d=calcular_modelo(0.)
    err=float(np.max(np.abs(d[:,1]-(1-np.exp(-d[:,0])))))
    assert err<1e-8
    for Re0 in VALORES:
        v=calcular_modelo(Re0)[:,1]
        assert np.min(v)>=0 and np.max(v)<=1+1e-10 and np.min(np.diff(v))>=-1e-10
    return {"error_limite_stokes":err}


def comparar_escenarios(seleccion="todos"):
    """Devuelve un diccionario etiqueta -> matriz calculada para A, B o C."""
    etiquetas=list("ABC") if seleccion=="todos" else [seleccion]
    return {etiqueta:calcular_modelo(VALORES["ABC".index(etiqueta)]) for etiqueta in etiquetas}


def guardar_resultados(resultados,carpeta):
    """Exporta cada escenario a CSV, con nombres de columnas y parámetros."""
    carpeta.mkdir(parents=True,exist_ok=True)
    for etiqueta,datos in resultados.items():
        with (carpeta/f"escenario_{etiqueta}.csv").open("w",newline="",encoding="utf-8") as f:
            writer=csv.writer(f);writer.writerow(COLUMNAS);writer.writerows(datos)
    metadatos={"DOI":DOI,"parametro":PARAMETRO,"valores_docentes":dict(zip("ABC",VALORES)),
               "alcance":"Simulación de un submodelo; parámetros de práctica, sin calibración física"}
    (carpeta/"parametros.json").write_text(json.dumps(metadatos,indent=2,ensure_ascii=False),encoding="utf-8")


def graficar_resultados(resultados,carpeta):
    """Crea una figura comparativa; separa las gráficas del cálculo del modelo."""
    fig,ax=plt.subplots(figsize=(8,4.8))
    for etiqueta,datos in resultados.items():
        valor=VALORES["ABC".index(etiqueta)]
        ax.plot(datos[:,0],datos[:,1],label=f"{etiqueta}: {PARAMETRO}={valor:g}")
    ax.set(xlabel=XLABEL,ylabel=YLABEL,title=TITULO)
    ax.grid(alpha=0.25);ax.legend()
    fig.text(0.5,0.01,"Ejemplo docente: valores relativos de práctica; no reproduce mediciones",ha="center",fontsize=8)
    fig.tight_layout(rect=[0,0.03,1,1]);fig.savefig(carpeta/"comparacion.png",dpi=160);plt.close(fig)


def main():
    """Lee opciones, verifica, calcula, exporta y grafica en ese orden."""
    parser=argparse.ArgumentParser(description=TITULO)
    parser.add_argument("--escenario",choices=["A","B","C","todos"],default="todos")
    parser.add_argument("--salida",type=Path,default=Path("resultados")/"alumno_04")
    parser.add_argument("--verificar",action="store_true")
    parser.add_argument("--animar",action="store_true",help="Genera GIF además del visor HTML y las métricas")
    args=parser.parse_args()
    if args.verificar:
        metricas=verificar()
        print(json.dumps({"verificacion":"OK","metricas":metricas},ensure_ascii=False))
    resultados=comparar_escenarios(args.escenario)
    guardar_resultados(resultados,args.salida)
    graficar_resultados(resultados,args.salida)
    exportar_movimiento("04",resultados,args.salida,args.animar)
    print(f"Alumno 04: {len(resultados)} escenario(s). Resultados en {args.salida}")


if __name__=="__main__":
    main()
