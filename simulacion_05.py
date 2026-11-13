"""Simulación estadística de una razón y su incertidumbre.

Ejemplo educativo del submodelo descrito en ALUMNO_05.md.
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



TITULO = 'Simulación estadística de una razón y su incertidumbre'
DOI = '10.1038/s41598-021-86549-9'
PARAMETRO = 'CV'
VALORES = [0.02, 0.05, 0.1]
COLUMNAS = ['repeticion', 'Q']
XLABEL = 'Razón Q=a/b'
YLABEL = 'Densidad de probabilidad simulada'

def muestrear_positivo(rng,media,cv,n):
    """Lognormal docente de media y CV dados; devuelve n valores positivos."""
    sigma=np.sqrt(np.log1p(cv*cv))
    mu=np.log(media)-sigma*sigma/2
    return rng.lognormal(mu,sigma,n)


def calcular_modelo(CV,n=10000,semilla=42):
    """Simula una razón de variables independientes; devuelve repetición,Q."""
    if CV<=0 or n<2:
        raise ValueError("CV debe ser positivo y n>=2")
    rng=np.random.default_rng(semilla)
    a=muestrear_positivo(rng,100.,CV,n)
    b=muestrear_positivo(rng,100.,CV,n)
    return np.column_stack((np.arange(n),a/b))


def verificar():
    """Compara Monte Carlo y propagación de primer orden a CV pequeño."""
    d=calcular_modelo(0.02,n=40000)
    sd=float(np.std(d[:,1],ddof=1));pred=np.sqrt(2)*0.02
    error=abs(sd/pred-1)
    assert error<0.04 and np.min(d[:,1])>0
    assert np.array_equal(calcular_modelo(0.05),calcular_modelo(0.05))
    return {"sd_MC":sd,"sd_primer_orden":float(pred),"discrepancia_relativa":float(error)}


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
        ax.hist(datos[:,1],bins=60,density=True,histtype="step",linewidth=1.5,label=f"{etiqueta}: CV={valor:g}")
    ax.set(xlabel=XLABEL,ylabel=YLABEL,title=TITULO)
    ax.grid(alpha=0.25);ax.legend()
    fig.text(0.5,0.01,"Ejemplo docente: valores relativos de práctica; no reproduce mediciones",ha="center",fontsize=8)
    fig.tight_layout(rect=[0,0.03,1,1]);fig.savefig(carpeta/"comparacion.png",dpi=160);plt.close(fig)


def main():
    """Lee opciones, verifica, calcula, exporta y grafica en ese orden."""
    parser=argparse.ArgumentParser(description=TITULO)
    parser.add_argument("--escenario",choices=["A","B","C","todos"],default="todos")
    parser.add_argument("--salida",type=Path,default=Path("resultados")/"alumno_05")
    parser.add_argument("--verificar",action="store_true")
    args=parser.parse_args()
    if args.verificar:
        metricas=verificar()
        print(json.dumps({"verificacion":"OK","metricas":metricas},ensure_ascii=False))
    resultados=comparar_escenarios(args.escenario)
    guardar_resultados(resultados,args.salida)
    graficar_resultados(resultados,args.salida)
    print(f"Alumno 05: {len(resultados)} escenario(s). Resultados en {args.salida}")


if __name__=="__main__":
    main()
