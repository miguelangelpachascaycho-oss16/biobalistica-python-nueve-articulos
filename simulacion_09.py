"""Transferencia térmica transitoria en dos capas.

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



TITULO = 'Transferencia térmica transitoria en dos capas'
DOI = '10.3923/jbs.2006.231.237'
PARAMETRO = 'Bi'
VALORES = [0.2, 0.5, 1.0]
COLUMNAS = ['s', 'theta_superficie', 'theta_interior']
XLABEL = 'Tiempo relativo s'
YLABEL = 'Temperatura superficial relativa θ'

def calcular_modelo(Bi,nodos=41,pulso=1.):
    """Diferencias finitas explícitas en dos capas; no resuelve el CFD del gas."""
    if Bi<0 or nodos<5:
        raise ValueError("Bi>=0 y nodos>=5")
    x=np.linspace(0,1,nodos);dx=x[1]-x[0]
    capacidad=np.where(x<0.1,1.3,1.)  # Dos capas relativas de práctica.
    dt_limite=0.35*dx*dx/(1+Bi*dx)
    pasos=int(np.ceil(0.3/dt_limite));s=np.linspace(0,0.3,pasos+1)
    dt=s[1]-s[0];theta=np.zeros(nodos);datos=np.zeros((pasos+1,3))
    datos[:,0]=s;interior=int(np.argmin(abs(x-0.25)))
    for i,t in enumerate(s[:-1]):
        gas=pulso if t<0.05 else 0.
        dtheta=np.zeros(nodos)
        dtheta[1:-1]=(theta[2:]-2*theta[1:-1]+theta[:-2])/(capacidad[1:-1]*dx*dx)
        dtheta[0]=2*(theta[1]-theta[0]+Bi*dx*(gas-theta[0]))/(capacidad[0]*dx*dx)
        theta=theta+dt*dtheta
        theta[-1]=0.  # Frontera profunda a la temperatura inicial, supuesto docente.
        datos[i+1,1:]=[theta[0],theta[interior]]
    return datos


def verificar():
    """Comprueba entrada nula, cotas y convergencia del máximo superficial."""
    assert np.max(np.abs(calcular_modelo(1.,pulso=0.)[:,1:]))==0
    a=calcular_modelo(1.,41);b=calcular_modelo(1.,81)
    discrep=abs(np.max(a[:,1])-np.max(b[:,1]))/np.max(b[:,1])
    assert discrep<0.05 and np.min(a[:,1:])>=-1e-12 and np.max(a[:,1:])<=1
    return {"discrepancia_maximo_41_vs_81":float(discrep),"Bi_verificado":1.}


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
    args=parser.parse_args()
    if args.verificar:
        metricas=verificar()
        print(json.dumps({"verificacion":"OK","metricas":metricas},ensure_ascii=False))
    resultados=comparar_escenarios(args.escenario)
    guardar_resultados(resultados,args.salida)
    graficar_resultados(resultados,args.salida)
    print(f"Alumno 09: {len(resultados)} escenario(s). Resultados en {args.salida}")


if __name__=="__main__":
    main()
