"""Contacto elástico, indentación y rebote.

Ejemplo educativo del submodelo descrito en ALUMNO_09.md.
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



TITULO = 'Contacto elástico, indentación y rebote'
DOI = '10.1007/s40571-024-00742-x'
PARAMETRO = 'K'
VALORES = [0.5, 1.0, 2.0]
COLUMNAS = ['s', 'q', 'w', 'fuerza', 'energia']
XLABEL = 'Tiempo relativo de contacto s'
YLABEL = 'Indentación relativa q=δ/L'

def calcular_modelo(K, paso=0.002):
    """Integra indentación y velocidad hasta la separación tras el rebote."""
    def f(t,y): return [y[1],-K*max(y[0],0.)**1.5]
    t=0.;y=np.array([0.,1.]);ts=[t];ys=[y.copy()]
    for _ in range(int(20/paso)):
        yn=integrar_rk4(f,np.array([t,t+paso]),y)[-1]
        if yn[0]<0 and yn[1]<0:
            a=y[0]/(y[0]-yn[0]);t+=a*paso;y+=a*(yn-y);y[0]=0
            ts.append(t);ys.append(y.copy());break
        t+=paso;y=yn;ts.append(t);ys.append(y.copy())
    else: raise RuntimeError("No se encontró separación")
    ys=np.array(ys);q=ys[:,0];w=ys[:,1]
    fuerza=K*np.maximum(q,0)**1.5
    energia=0.5*w*w+0.4*K*np.maximum(q,0)**2.5
    return np.column_stack((ts,q,w,fuerza,energia))

def verificar():
    """Comprueba energía, indentación máxima y coeficiente de restitución."""
    errores=[]
    for K in VALORES:
        d=calcular_modelo(K);qmax=(5/(4*K))**0.4
        errores.append(abs(d[:,1].max()-qmax))
        assert np.max(abs(d[:,4]-.5))<1e-6
        assert abs(abs(d[-1,2])-1)<1e-6
    assert max(errores)<1e-5
    return {"error_indentacion_maxima":float(max(errores)),"restitucion":float(abs(d[-1,2]))}


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
    parser.add_argument("--salida",type=Path,default=Path("resultados")/"alumno_09")
    parser.add_argument("--verificar",action="store_true")
    parser.add_argument("--animar",action="store_true",help="Genera GIF además del visor HTML y las métricas")
    args=parser.parse_args()
    if args.verificar:
        metricas=verificar()
        print(json.dumps({"verificacion":"OK","metricas":metricas},ensure_ascii=False))
    resultados=comparar_escenarios(args.escenario)
    guardar_resultados(resultados,args.salida)
    graficar_resultados(resultados,args.salida)
    exportar_movimiento("09",resultados,args.salida,args.animar)
    print(f"Alumno 09: {len(resultados)} escenario(s). Resultados en {args.salida}")


if __name__=="__main__":
    main()
