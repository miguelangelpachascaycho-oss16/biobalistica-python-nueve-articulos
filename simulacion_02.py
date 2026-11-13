"""Trabajo del gas y velocidad normalizada.

Ejemplo educativo del submodelo descrito en ALUMNO_02.md.
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



TITULO = 'Trabajo del gas y velocidad normalizada'
DOI = '10.3109/10717544.2014.887158'
PARAMETRO = 'gamma'
VALORES = [1.2, 1.4, 1.6]
COLUMNAS = ['s', 'J', 'U', 'J_analitica']
XLABEL = 'Expansión relativa s=V2/V1'
YLABEL = 'Trabajo relativo J=E/(P1 V1)'

def calcular_modelo(gamma):
    """Integra presión relativa y devuelve s, J, U y referencia cerrada."""
    if gamma <= 0:
        raise ValueError("gamma debe ser positivo")
    s=np.linspace(0,1,501)
    presion=(1+s)**(-gamma)
    J=np.r_[0.,np.cumsum((presion[1:]+presion[:-1])*np.diff(s)/2)]
    referencia=np.log1p(s) if abs(gamma-1)<1e-10 else np.expm1((1-gamma)*np.log1p(s))/(1-gamma)
    return np.column_stack((s,J,np.sqrt(np.maximum(J,0)),referencia))


def verificar():
    """Compara cuadratura y forma cerrada, incluyendo el límite gamma=1."""
    errores=[]
    for gamma in list(VALORES)+[1.]:
        d=calcular_modelo(gamma)
        errores.append(float(np.max(np.abs(d[:,1]-d[:,3]))))
        assert np.max(np.abs(d[:,2]**2-d[:,1])) < 1e-12
    assert max(errores) < 1e-6
    return {"error_maximo_trabajo":max(errores)}


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
    parser.add_argument("--salida",type=Path,default=Path("resultados")/"alumno_02")
    parser.add_argument("--verificar",action="store_true")
    args=parser.parse_args()
    if args.verificar:
        metricas=verificar()
        print(json.dumps({"verificacion":"OK","metricas":metricas},ensure_ascii=False))
    resultados=comparar_escenarios(args.escenario)
    guardar_resultados(resultados,args.salida)
    graficar_resultados(resultados,args.salida)
    print(f"Alumno 02: {len(resultados)} escenario(s). Resultados en {args.salida}")


if __name__=="__main__":
    main()
