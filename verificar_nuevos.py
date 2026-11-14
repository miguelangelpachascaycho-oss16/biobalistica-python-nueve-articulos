"""Verificación independiente de fuerzas y límites analíticos de casos 06-09."""
from dataclasses import replace
from pathlib import Path
import json
import numpy as np
from scipy.spatial.transform import Rotation
import penetracion_activa as act
import bicapa_dpd as dpd


def gradiente_numerico(energia, x, eps=1e-6):
    """Derivada central de energía: prueba independiente de fuerzas codificadas."""
    f = np.zeros_like(x)
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            d = np.zeros_like(x)
            d[i, j] = eps
            f[i, j] = -(energia(x+d)-energia(x-d))/(2*eps)
    return f


def verificar_activos():
    salida = {}
    for caso in (6, 7):
        p = act.Parametros(caso=caso, actividad=0, n_lado=4, n_cadena=6, rigidez_reducida=.2)
        x, b, r0, fijo, c, h = act.construir(p)
        f, tor, fp, U = act.fuerzas(x, np.zeros(len(x)), c, b, r0, p, h)
        reposo = np.max(np.abs(f[~fijo]))
        assert reposo < 1e-12
        x = x+np.random.default_rng(2).normal(size=x.shape)*.01
        phi = np.linspace(-.02, .02, len(x))
        # Alejar NP para comprobar cada energía sin cruce de cortes.
        c[-1] = -6
        f, tor, fp, U = act.fuerzas(x, phi, c, b, r0, p, h)
        def energia(xx):
            return act.fuerzas(xx, phi, c, b, r0, p, h)[3]
        err = float(np.max(np.abs(f-gradiente_numerico(energia, x))))
        assert err < 2e-6
        err_torque = 0.
        if caso == 7:
            tt = np.zeros(len(phi))
            for i in range(len(phi)):
                ph = phi.copy()
                ph[i] += 1e-6
                up = act.fuerzas(x, ph, c, b, r0, p, h)[3]
                ph[i] -= 2e-6
                um = act.fuerzas(x, ph, c, b, r0, p, h)[3]
                tt[i] = -(up-um)/2e-6
            err_torque = float(np.max(np.abs(tt-tor)))
            assert err_torque < 1e-7
        balance = float(np.linalg.norm(f.sum(axis=0)+fp))
        assert balance < 1e-12
        salida[str(caso)] = dict(control_reposo=float(reposo), fuerza_gradiente=err,
                                 torque_gradiente=err_torque, accion_reaccion=balance)
    return salida


def verificar_dpd():
    p = dpd.Parametros(caso=9)
    x = np.array([[3., 3., 3.], [3.45, 3.12, 3.], [3.65, 3.53, 3.1], [4.2, 3.6, 3.], [4.5, 4.1, 3.2]])
    v = np.zeros_like(x)
    tipos = np.array([0, 1, 2, 3, 4])
    bonds = np.array([[0, 1], [1, 2]])
    angles = np.array([[0, 1, 2]])
    ka, theta, caja = np.array([20.]), np.array([2.1]), np.array([10., 10., 10.])
    grupos = np.full(len(x), -1)
    rng = np.random.default_rng(4)
    def evaluar(xx, vv=v):
        return dpd.fuerzas(xx, vv, tipos, bonds, angles, ka, theta, 256., True, caja, grupos, p, rng, ruido=False)
    f, U = evaluar(x)
    err = float(np.max(np.abs(f-gradiente_numerico(lambda xx: evaluar(xx)[1], x))))
    assert err < 3e-6
    balance = float(np.linalg.norm(f.sum(axis=0)))
    assert balance < 1e-10
    vel = np.random.default_rng(3).normal(size=x.shape)
    fd, _ = evaluar(x, vel)
    potencia = float(np.sum((fd-f)*vel))
    assert potencia < 0
    # Tetraedro regular: tensor de inercia isotrópico y rotación libre exacta.
    b = dpd.geometria_np(p)
    I = sum(np.dot(q, q)*np.eye(3)-np.outer(q, q) for q in b)
    omega = np.array([.2, .3, .1])
    body = dict(b=b, ids=np.arange(len(b)), centro=np.array([5., 5., 8.]), origen=np.array([5., 5., 8.]),
                Q=np.eye(3), V=np.array([0., 0., -.5]), momento=I@omega, invI=np.linalg.inv(I))
    total = 1.
    for j in range(round(total/p.dt)):
        xx, vv = dpd.paso_rigido(np.zeros_like(b), body, p, j*p.dt, caja)
    T = round(total/p.dt)*p.dt
    exacto = b@Rotation.from_rotvec(T*omega).as_matrix().T+np.array([5., 5., 8.-.5*T])
    err_rot = float(np.max(np.abs(xx-exacto)))
    assert len(b) == 56
    assert err_rot < 1e-10
    # Resorte móvil en ausencia de medio: solución z0-Vt+(V/omega)sin(omega*t).
    def oscilador(dt):
        pp = replace(p, caso=8, dt=dt, velocidad=.7)
        c = np.array([5., 5., 5.])
        body = dict(b=b, ids=np.arange(len(b)), centro=c.copy(), origen=c.copy(),
                    Q=np.eye(3), V=np.zeros(3), momento=np.zeros(3), invI=np.linalg.inv(I))
        for j in range(round(1.2/dt)):
            dpd.paso_rigido(np.zeros_like(b), body, pp, j*dt, caja)
        w = np.sqrt(pp.resorte_guia/len(b))
        z = 5-pp.velocidad*1.2+pp.velocidad/w*np.sin(w*1.2)
        return abs(body['centro'][2]-z)
    e1, e2 = oscilador(.006), oscilador(.003)
    assert e2 < .6*e1
    return dict(fuerza_gradiente=err, accion_reaccion=balance, potencia_disipativa=potencia,
                error_rotacion_libre=err_rot, beads_tetraedro=len(b),
                error_resorte_movil_dt=e1, error_resorte_movil_dt_mitad=e2)


if __name__ == '__main__':
    r = dict(activos=verificar_activos(), dpd=verificar_dpd(),
             alcance='Verificación mecánica y límites analíticos; no validación de modelos biológicos ni reproducción de fases publicadas')
    Path('VERIFICACION_NUEVOS.json').write_text(json.dumps(r, indent=2, ensure_ascii=False), encoding='utf-8')
    print(json.dumps(r, indent=2, ensure_ascii=False))
