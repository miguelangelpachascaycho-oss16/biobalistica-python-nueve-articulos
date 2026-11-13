"""Desaceleración y evento de parada.

Ejemplo educativo del submodelo descrito en ALUMNO_03.md.
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


def integrar_hasta_parada(resistencia, paso=0.005, horizonte=40.0):
    """Integra (velocidad, posición) y localiza v=0 por interpolación lineal."""
    def f(t, y):
        return np.array([-resistencia(max(float(y[0]), 0.0)), y[0]])
    t, y = 0.0, np.array([1.0, 0.0])
    tiempos, estados = [t], [y.copy()]
    for _ in range(int(np.ceil(horizonte/paso))):
        siguiente = integrar_rk4(f, np.array([t, t+paso]), y)[-1]
        if siguiente[0] <= 0:
            fraccion = y[0] / (y[0] - siguiente[0])
            final = y + fraccion*(siguiente-y)
            final[0] = 0.0
            tiempos.append(t + fraccion*paso)
            estados.append(final)
            return np.array(tiempos), np.array(estados)
        t += paso
        y = siguiente
        tiempos.append(t)
        estados.append(y.copy())
    raise RuntimeError("No hubo parada: revisa horizonte y parámetros")



TITULO = 'Desaceleración y evento de parada'
DOI = '10.1016/j.ces.2014.06.031'
PARAMETRO = 'A'
VALORES = [0.5, 1.0, 2.0]
COLUMNAS = ['s', 'w', 'z']
XLABEL = 'Tiempo relativo s'
YLABEL = 'Velocidad relativa w'

def calcular_modelo(A):
    """Resuelve tres resistencias positivas con parada; devuelve s,w,z."""
    if A <= 0:
        raise ValueError("A debe ser positivo")
    s,estado=integrar_hasta_parada(lambda w:A*w+0.2*w*w+0.1)
    return np.column_stack((s,estado))


def verificar():
    """Compara parada con cuadraturas en velocidad, independientes de RK4."""
    errores=[]
    for A in VALORES:
        d=calcular_modelo(A)
        v=np.linspace(0,1,10001);den=A*v+0.2*v*v+0.1
        def integral(y):return np.sum((y[:-1]+y[1:])*np.diff(v)/2)
        t_ref,z_ref=integral(1/den),integral(v/den)
        errores.append(abs(d[-1,0]-t_ref))
        assert abs(d[-1,2]-z_ref) < 2e-4
        assert d[-1,1]==0 and np.min(d[:,1])>=0
    assert max(errores) < 2e-4
    return {"error_maximo_tiempo_parada":float(max(errores))}


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
    parser.add_argument("--salida",type=Path,default=Path("resultados")/"alumno_03")
    parser.add_argument("--verificar",action="store_true")
    args=parser.parse_args()
    if args.verificar:
        metricas=verificar()
        print(json.dumps({"verificacion":"OK","metricas":metricas},ensure_ascii=False))
    resultados=comparar_escenarios(args.escenario)
    guardar_resultados(resultados,args.salida)
    graficar_resultados(resultados,args.salida)
    print(f"Alumno 03: {len(resultados)} escenario(s). Resultados en {args.salida}")


if __name__=="__main__":
    main()
