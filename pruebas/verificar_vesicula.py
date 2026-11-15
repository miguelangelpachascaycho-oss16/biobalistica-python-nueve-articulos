"""Comprobaciones mecánicas del piloto DPD; no validación biológica."""
import sys
from pathlib import Path as _Path
sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "src"))
_evidencia = _Path(__file__).resolve().parent / "resultados"
_evidencia.mkdir(exist_ok=True)
from dataclasses import replace
from pathlib import Path
import json
import numpy as np
from vesicula_dpd import Parametros, fuerzas, paso_dpd, observables


def verificar():
    p = Parametros(caja=(10., 10., 10.), sigma=0., gamma=0.)
    x = np.array([[4., 5., 5.], [4.73, 5.1, 5.], [5.48, 4.95, 5.], [6.1, 5.1, 5.]])
    v = np.zeros_like(x)
    tipo = np.array([0, 1, 1, 1])
    enlaces = np.array([[0, 1], [1, 2], [2, 3]])
    rng = np.random.default_rng(2)
    f, U = fuerzas(x, v, tipo, enlaces, p, rng, ruido=False)
    error_accion = np.linalg.norm(f.sum(axis=0))
    eps = 1e-6
    fd = np.zeros_like(f)
    for i in range(4):
        for j in range(3):
            dx = np.zeros_like(x)
            dx[i, j] = eps
            up = fuerzas(x+dx, v, tipo, enlaces, p, rng, ruido=False)[1]
            um = fuerzas(x-dx, v, tipo, enlaces, p, rng, ruido=False)[1]
            fd[i, j] = -(up-um)/(2*eps)
    error_gradiente = np.max(np.abs(fd-f))
    libre = np.empty((0, 2), dtype=int)
    # Apaga repulsión por separación > rc; un bead debe viajar en línea recta.
    a = np.array([[2., 2., 2.]])
    b = np.array([[.2, -.1, .3]])
    aa, bb = a.copy(), b.copy()
    for _ in range(100):
        aa, bb, _ = paso_dpd(aa, bb, np.array([2]), libre, p, rng)
    error_vuelo = np.max(np.abs(aa-(a+100*p.dt*b)))
    # Con la convención d=xj-xi, la diferencia entre gamma>0 y gamma=0
    # debe disipar potencia para todas las velocidades, también con traslación.
    vel = rng.normal(size=x.shape)
    fdamp = fuerzas(x, vel, tipo, libre, replace(p, gamma=4.5), rng, ruido=False)[0]
    fc = fuerzas(x, vel, tipo, libre, p, rng, ruido=False)[0]
    potencia = np.sum((fdamp-fc)*vel)
    error_fdt = abs(Parametros().sigma**2-2*Parametros().gamma)
    # Convergencia temporal de un oscilador HTTT, sin termostato ni
    # conservativa no enlazada (beads separados más de rc).
    xx = np.array([[3., 5., 5.], [4.1, 5., 5.]])
    vv = np.zeros_like(xx)
    pp = replace(p, rs=1.2)
    T = .04
    def integrar(dt):
        q, w = xx.copy(), vv.copy()
        for _ in range(round(T/dt)):
            q, w, _ = paso_dpd(q, w, np.array([2, 2]), np.array([[0, 1]]), replace(pp, dt=dt), rng)
        return q
    omega = np.sqrt(2*p.C/pp.rs)
    r = pp.rs+(1.1-pp.rs)*np.cos(omega*T)
    exacto = xx.mean(axis=0)+np.array([[-r/2, 0., 0.], [r/2, 0., 0.]])
    e1, e2 = (float(np.max(np.abs(integrar(dt)-exacto))) for dt in (.004, .002))
    # La métrica alineada no debe llamar deformación a una rotación rígida.
    ang = .3
    Q = np.array([[np.cos(ang), -np.sin(ang), 0.],
                  [np.sin(ang), np.cos(ang), 0.], [0., 0., 1.]])
    original = np.array([[4., 5., 5.], [5., 4., 5.], [5., 5., 6.], [6., 6., 5.]])
    rotado = (original-5)@Q+5.2
    original = np.r_[original, [[8., 8., 8.]]]
    rotado = np.r_[rotado, [[8., 8., 8.]]]
    error_rigido = observables(rotado, np.zeros_like(rotado), 4, 4, original, p)[0]
    assert error_accion < 1e-11
    assert error_gradiente < 1e-5
    assert error_vuelo < 1e-12
    assert potencia < 0
    assert error_fdt < 1e-12
    assert e2 < .6*e1
    assert error_rigido < 1e-12
    return dict(accion_reaccion=error_accion, gradiente_energia=error_gradiente,
                vuelo_libre=error_vuelo, potencia_disipativa=potencia,
                fluctuacion_disipacion=error_fdt, error_oscilador_dt=e1,
                error_oscilador_dt_mitad=e2,
                error_desplazamiento_rigido=error_rigido,
                alcance='Fuerzas y límite analítico conservativo; no certifica equilibrio de vesícula ni fases de Arai')


if __name__ == '__main__':
    r = verificar()
    (_evidencia / "VERIFICACION_VESICULA.json").write_text(json.dumps(r, indent=2, ensure_ascii=False), encoding='utf-8')
    print(json.dumps(r, indent=2, ensure_ascii=False))
