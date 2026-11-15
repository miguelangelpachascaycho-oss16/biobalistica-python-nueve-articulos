"""Controles independientes del piloto; no validación biológica del artículo."""
import sys
from pathlib import Path as _Path
sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "src"))
_evidencia = _Path(__file__).resolve().parent / "resultados"
_evidencia.mkdir(exist_ok=True)
import json
from dataclasses import replace
from pathlib import Path
import numpy as np
from piloto_membrana import (Parametros, crear_sistema, fuerzas_enlaces,
                             fuerzas_contacto, integrar)


def oscilador(dt):
    """Un enlace axial: compara RK2 con la solución cerrada subamortiguada."""
    p = Parametros(k=4e-3, c=1e-5)
    m = 4*np.pi*p.radio_lipido**3*p.densidad_lipido/3
    q, v, q0 = .03, 0., .03
    gamma = p.c/(2*m)
    wd = np.sqrt(p.k/m-gamma**2)
    tiempo = .2
    pasos = round(tiempo/dt)
    dt = tiempo/pasos
    for _ in range(pasos):
        a = -(p.k*q+p.c*v)/m
        qm, vm = q+dt*v/2, v+dt*a/2
        q, v = q+dt*vm, v-dt*(p.k*qm+p.c*vm)/m
    exacta = q0*np.exp(-gamma*tiempo)*(np.cos(wd*tiempo)
              +gamma/wd*np.sin(wd*tiempo))
    return abs(q-exacta)/q0


def main():
    p = Parametros(tiempo_final=.16)
    x, v, radios, masas, enlaces, l0, fijos, nm = crear_sistema(p)
    x[100, 2] += .1
    f = fuerzas_enlaces(x, v, enlaces, l0, np.ones(len(enlaces), bool), p)
    accion_reaccion = np.linalg.norm(f.sum(axis=0))
    # Colisión aislada: comprueba repulsión, ausencia de fuerza a distancia y balance.
    xx = np.array([[0., 0., 0.], [1.8, 0., 0.]])
    vv = np.array([[1., 0., 0.], [-1., 0., 0.]])
    ff = fuerzas_contacto(xx, vv, np.array([1., 1.]), np.array([1., 1.]), p)
    assert ff[0, 0] < 0 and ff[1, 0] > 0
    assert np.allclose(ff.sum(axis=0), 0)
    ff_lejos = fuerzas_contacto(xx*10, vv, np.array([1., 1.]), np.array([1., 1.]), p)
    assert np.all(ff_lejos == 0)
    e1, e2 = oscilador(.001), oscilador(.0005)
    assert e2 < e1/3
    assert accion_reaccion < 1e-12
    # El impacto converge al reducir dt; posiciones del blanco, no píxeles del dibujo.
    grueso = integrar(p)
    fino = integrar(replace(p, dt=p.dt/2))
    escala = np.linalg.norm(fino["x"][-1, :nm]-fino["x"][0, :nm])
    error = np.linalg.norm(grueso["x"][-1, :nm]-fino["x"][-1, :nm])/escala
    assert error < .02, error
    # La presión ya mueve la membrana sin impacto: este control debe declararse.
    control = integrar(replace(p, con_proyectiles=False))
    resultado = {
        "accion_reaccion_enlaces_nN": float(accion_reaccion),
        "contacto_repulsivo_y_sin_fuerza_a_distancia": True,
        "error_oscilador_dt_0_001": float(e1),
        "error_oscilador_dt_0_0005": float(e2),
        "error_relativo_posiciones_blanco_dt_mitad_t_0_16_ns": float(error),
        "u_max_control_sin_proyectiles_nm": float(control["metricas"][:, 1].max()),
        "u_max_con_impacto_nm": float(grueso["metricas"][:, 1].max()),
        "alcance": "Verificación numérica de reducción didáctica; no réplica validada del artículo"
    }
    (_evidencia / "VERIFICACION_PILOTO.json").write_text(json.dumps(resultado, indent=2), encoding="utf-8")
    print(json.dumps(resultado, indent=2))


if __name__ == "__main__":
    main()
