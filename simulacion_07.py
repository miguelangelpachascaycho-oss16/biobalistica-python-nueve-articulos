"""Modelo analítico de Poncelet y parada.

Ejemplo educativo del submodelo descrito en ALUMNO_07.md.
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



TITULO = 'Modelo analítico de Poncelet y parada'
DOI = '10.1016/j.taml.2024.100567'
PARAMETRO = 'w0'
VALORES = [0.5, 1.0, 2.0]
COLUMNAS = ['s', 'w', 'z', 'w_analitica']
XLABEL = 'Tiempo relativo s'
YLABEL = 'Velocidad relativa w'

def calcular_modelo(w0):
    """Resuelve Poncelet hasta su tiempo de parada analítico atan(w0)."""
    if w0<=0:
        raise ValueError("w0 debe ser positivo")
    sf=np.arctan(w0);s=np.linspace(0,sf,801)
    estado=integrar_rk4(lambda t,y:[-(1+y[0]**2),y[0]],s,[w0,0.])
    estado[-1,0]=0.  # Quita únicamente el residuo de redondeo en el evento conocido.
    analitica=np.tan(sf-s)
    return np.column_stack((s,estado,analitica))


def verificar():
    """Verifica velocidad y distancia final mediante soluciones independientes."""
    errores=[]
    for w0 in VALORES:
        d=calcular_modelo(w0)
        errores.append(float(np.max(np.abs(d[:,1]-d[:,3]))))
        assert abs(d[-1,2]-0.5*np.log1p(w0*w0))<1e-7
        assert np.min(d[:,1])>=-1e-10
    assert max(errores)<1e-7
    return {"error_maximo_velocidad":max(errores)}


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
    parser.add_argument("--salida",type=Path,default=Path("resultados")/"alumno_07")
    parser.add_argument("--verificar",action="store_true")
    args=parser.parse_args()
    if args.verificar:
        metricas=verificar()
        print(json.dumps({"verificacion":"OK","metricas":metricas},ensure_ascii=False))
    resultados=comparar_escenarios(args.escenario)
    guardar_resultados(resultados,args.salida)
    graficar_resultados(resultados,args.salida)
    print(f"Alumno 07: {len(resultados)} escenario(s). Resultados en {args.salida}")


if __name__=="__main__":
    main()
