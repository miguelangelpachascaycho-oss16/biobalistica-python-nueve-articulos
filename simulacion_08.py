"""Arrastre de Clift-Gauvin en un gel.

Ejemplo educativo del submodelo descrito en ALUMNO_08.md.
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



TITULO = 'Arrastre de Clift-Gauvin en un gel'
DOI = '10.1007/s11340-020-00639-9'
PARAMETRO = 'Re0'
VALORES = [5.0, 50.0, 500.0]
COLUMNAS = ['s', 'w', 'z']
XLABEL = 'Tiempo relativo s'
YLABEL = 'Velocidad relativa w'

def arrastre_por_velocidad_cuadrada(w,Re0):
    """Devuelve Cd(Re0*w)*w² usando una forma estable en w=0."""
    w=max(float(w),0.)
    if w==0:return 0.
    Re=Re0*w
    viscoso=24/Re0*w*(1+0.15*Re**0.687)
    inercial=0.42*w*w/(1+42500/Re**1.16)
    return viscoso+inercial


def calcular_modelo(Re0):
    """Resuelve el modelo normalizado con resistencia constante Y=0.1."""
    if Re0<=0:
        raise ValueError("Re0 debe ser positivo")
    s,estado=integrar_hasta_parada(lambda w:0.02*arrastre_por_velocidad_cuadrada(w,Re0)+0.1)
    return np.column_stack((s,estado))


def verificar():
    """Verifica el límite viscoso y un caso independiente de fuerza constante."""
    Re0=1e-4;w=0.7
    ratio=arrastre_por_velocidad_cuadrada(w,Re0)/(24/Re0*w)
    assert abs(ratio-1)<0.001
    assert arrastre_por_velocidad_cuadrada(0,Re0)==0
    t,y=integrar_hasta_parada(lambda w:0.1)
    assert abs(t[-1]-10)<1e-8 and abs(y[-1,1]-5)<1e-6
    for Re0 in VALORES:
        d=calcular_modelo(Re0)
        assert np.min(d[:,1])>=0 and d[-1,1]==0
    return {"factor_limite_viscoso":float(ratio),"parada_fuerza_constante":float(t[-1])}


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
    parser.add_argument("--salida",type=Path,default=Path("resultados")/"alumno_08")
    parser.add_argument("--verificar",action="store_true")
    parser.add_argument("--animar",action="store_true",help="Genera GIF además del visor HTML y las métricas")
    args=parser.parse_args()
    if args.verificar:
        metricas=verificar()
        print(json.dumps({"verificacion":"OK","metricas":metricas},ensure_ascii=False))
    resultados=comparar_escenarios(args.escenario)
    guardar_resultados(resultados,args.salida)
    graficar_resultados(resultados,args.salida)
    exportar_movimiento("08",resultados,args.salida,args.animar)
    print(f"Alumno 08: {len(resultados)} escenario(s). Resultados en {args.salida}")


if __name__=="__main__":
    main()
