"""Controles independientes del FEM de piel; ejecutar desde la carpeta del repo."""
from dataclasses import replace
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import numpy as np
from piel_ogden import Parametros, malla, energia_tension, fuerzas_internas, contacto, simular, poncelet


def verificar():
    p = Parametros()
    F = np.array([[[1.12, .03, 0], [0., .94, 0], [0., 0., 1.01]]])
    W, P, _ = energia_tension(F, p)
    errores = []
    for a in range(3):
        for b in range(3):
            h = 1e-6
            fp, fm = F.copy(), F.copy()
            fp[0, a, b] += h
            fm[0, a, b] -= h
            d = (energia_tension(fp, p)[0][0]-energia_tension(fm, p)[0][0])/(2*h)
            errores.append(abs(d-P[0, a, b]))
    assert max(errores) < 1e-6
    # Objetividad frente a una rotación rígida: energía invariante.
    angulo = .37
    Q = np.array([[np.cos(angulo), -np.sin(angulo), 0],
                  [np.sin(angulo), np.cos(angulo), 0], [0, 0, 1]])
    assert np.allclose(energia_tension(Q@F, p)[0], W, atol=1e-10)
    x0, tri, grad, radio, vol, masas, fijos, area = malla(p)
    f0, U0, J0 = fuerzas_internas(x0, tri, grad, radio, vol, p)
    assert np.max(abs(f0)) < 1e-12
    # La fuerza nodal también debe ser la derivada de la energía ensamblada.
    xx = x0.copy()
    nodo = 4*(p.nr+1)+3
    xx[nodo, 1] += 1e-6
    ff, _, _ = fuerzas_internas(xx, tri, grad, radio, vol, p)
    h = 1e-10
    xp, xm = xx.copy(), xx.copy()
    xp[nodo, 1] += h
    xm[nodo, 1] -= h
    derivada = (fuerzas_internas(xp, tri, grad, radio, vol, p)[1]
                -fuerzas_internas(xm, tri, grad, radio, vol, p)[1])/(2*h)
    error_nodal = abs(derivada+ff[nodo, 1])
    assert error_nodal < 1e-10
    fc, fp, _, _ = contacto(x0, -p.diametro/2+1e-6, p, area)
    assert abs(fc[:, 1].sum()+fp) < 1e-12
    # Poncelet: derivar la profundidad analítica debe recuperar la velocidad.
    t = np.linspace(0., 5e-7, 10001)
    z, v, tf = poncelet(t, p)
    error_poncelet = float(np.max(abs(np.gradient(z, t)[1:-1]-v[1:-1])))
    assert error_poncelet < .01
    with TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        d, _ = simular(p, tmp/'base')
        fino, _ = simular(replace(p, dt=p.dt/2), tmp/'dt')
        control, _ = simular(replace(p, velocidad=0.), tmp/'control')
        antes = d[:, 0] < .8*p.hueco/p.velocidad
        error_vuelo = np.max(abs(d[antes, 1]-(-p.diametro/2-p.hueco+p.velocidad*d[antes, 0])))
        relativo = abs(d[-1, 3]-fino[-1, 3])/fino[-1, 3]
        energia = d[:, 4:7].sum(axis=1)
        deriva = np.max(abs(energia/energia[0]-1))
        assert error_vuelo < 1e-12
        assert relativo < .01
        assert deriva < .02
        assert control[:, 3].max() < 1e-12
        assert d[:, 3].max() > 1e-6
        assert d[:, 7].min() > 0
    resultado = {
        'articulo': '10.1016/j.taml.2024.100567',
        'modelo': 'Reducción docente FEM axisimétrica, fase temprana sin perforación',
        'error_derivada_W_P_Pa': float(max(errores)),
        'error_gradiente_nodal_N': float(error_nodal),
        'error_Poncelet_m_s': error_poncelet,
        'error_vuelo_libre_m': float(error_vuelo),
        'cambio_relativo_u_final_al_reducir_dt': float(relativo),
        'deriva_relativa_energia': float(deriva),
        'desplazamiento_maximo_m': float(d[:, 3].max()),
        'J_minimo': float(d[:, 7].min()),
        'solape_contacto_maximo_m': float(d[:, 8].max()),
        'validacion_experimental': False,
        'replica_SPH_FEM_RADIOSS': False,
        'estado': 'Controles numéricos aprobados; convergencia espacial y validación física pendientes'
    }
    Path('VERIFICACION_PIEL.json').write_text(json.dumps(resultado, indent=2, ensure_ascii=False), encoding='utf-8')
    print(json.dumps(resultado, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    verificar()
