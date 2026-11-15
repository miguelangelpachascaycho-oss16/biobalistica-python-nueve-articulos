"""Verificaciones físicas y numéricas de las dos reducciones celulares DEM."""
import sys
from pathlib import Path as _Path
sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "src"))
_evidencia = _Path(__file__).resolve().parent / "resultados"
_evidencia.mkdir(exist_ok=True)
from dataclasses import replace
from pathlib import Path
import json
import numpy as np
from celula_dem import (ParametrosCelula, crear_celula, normales_internas,
    simular_celula, interior_poligono)
from piloto_membrana import fuerzas_enlaces, fuerzas_contacto


def comprobar(p):
    x,v,r,m,enlaces,l0,criticas=crear_celula(p)
    n=p.nodos_capa; nm=2*n
    grado=np.bincount(enlaces.ravel(),minlength=nm)
    assert np.all(grado==5)
    normals=normales_internas(x,n)
    assert np.all(np.sum(normals*x[:n],axis=1)>0)
    # Estado sin deformación: los enlaces no ejercen fuerza elástica inicial.
    f0=fuerzas_enlaces(x,v,enlaces,l0,np.ones(len(enlaces),bool),p)
    assert np.max(np.abs(f0))<1e-14
    x[3]+=[.07,-.03]
    fe=fuerzas_enlaces(x,v,enlaces,l0,np.ones(len(enlaces),bool),p)
    balance=float(np.linalg.norm(fe.sum(axis=0)))
    assert balance<1e-12
    desplazado=x+[17.,-9.]
    desplazamiento_error=float(np.max(np.abs(fe-fuerzas_enlaces(desplazado,v,enlaces,l0,np.ones(len(enlaces),bool),p))))
    assert desplazamiento_error<1e-12
    fc=fuerzas_contacto(x,v,r,m,p)
    assert np.linalg.norm(fc.sum(axis=0))<1e-10
    # Movimiento libre previo al impacto: solución exacta del arrastre lineal.
    libre=simular_celula(replace(p,tiempo_final=.04))
    tau=m[nm:]/p.arrastre
    xe=libre['x'][0,nm:,0]+p.velocidad*tau*(1-np.exp(-.04/tau))
    error_libre=float(np.max(np.abs(xe-libre['x'][-1,nm:,0])))
    assert error_libre<1e-6
    grueso=simular_celula(replace(p,tiempo_final=.3))
    fino=simular_celula(replace(p,tiempo_final=.3,dt=p.dt/2))
    cambio=np.linalg.norm(fino['x'][-1,:nm]-fino['x'][0,:nm])
    error_refinado=float(np.linalg.norm(grueso['x'][-1,:nm]-fino['x'][-1,:nm])/cambio)
    assert error_refinado<.02,error_refinado
    control=simular_celula(replace(p,numero_proyectiles=0,tiempo_final=.3))
    assert np.all(np.diff(grueso['metricas'][:,3])>=0)
    # Prueba del indicador interior independiente del radio inicial.
    caja=np.array([[-1,-1],[1,-1],[1,1],[-1,1]])
    assert interior_poligono(np.array([[0.,0.],[2.,0.]]),caja).tolist()==[True,False]
    return {'doi':p.articulo,'nodos':nm,'cinco_enlaces_por_nodo':True,
       'balance_enlaces_nN':balance,'invariancia_traslacion_nN':desplazamiento_error,
       'error_vuelo_libre_nm':error_libre,'error_relativo_blanco_dt_mitad_t_0_3_ns':error_refinado,
       'u_max_impacto_nm':float(grueso['metricas'][:,1].max()),
       'u_max_control_nm':float(control['metricas'][:,1].max())}


def main():
    configuraciones=[ParametrosCelula(),ParametrosCelula(articulo='10.3970/cmes.2014.098.221',
        radio_externo=60.,nodos_capa=120,diametro_proyectil=2.5,
        diametros_aleatorios=True,presion_por_nodo=32.7e-5,critica_transversal=.1)]
    resultados=[comprobar(p) for p in configuraciones]
    salida={'alcance':'Verificación de implementaciones didácticas reducidas; sin validación biológica',
        'resultados':resultados}
    (_evidencia / "VERIFICACION_CELULAS.json").write_text(json.dumps(salida,indent=2,ensure_ascii=False),encoding='utf8')
    print(json.dumps(salida,indent=2,ensure_ascii=False))


if __name__=='__main__':
    main()
