"""Modelos publicados de penetración activa; no son impactos inerciales.

Caso 06: Daddi-Moussa-Ider et al., NJP 21 083014 (2019), ec. 1-3, 20,24.
Caso 07: Daddi-Moussa-Ider et al., JCP 150 064906 (2019), ec. 1-11,43.
Unidades a=epsilon=movilidad traslacional=1. Agua implícita de Stokes.
"""
from dataclasses import dataclass, asdict
from pathlib import Path
import json
import numpy as np
from scipy.spatial import cKDTree
from scipy.integrate import solve_ivp


@dataclass
class Parametros:
    caso: int = 6
    n_lado: int = 14
    n_cadena: int = 20
    radio_np: float = 1.
    actividad: float = .4
    rigidez_reducida: float = 1.
    preestres: float = .9
    dipolo: float = 1.
    tiempo: float = 800.
    rtol: float = 2e-6
    atol: float = 1e-8


def construir(p):
    """Hoja cuadrada 3D o cadena dipolar 2D, con extremos fijos."""
    h = 2**(7/6)
    if p.caso == 6:
        q = (np.arange(p.n_lado)-(p.n_lado-1)/2)*h
        a, b = np.meshgrid(q, q)
        x = np.column_stack((a.ravel(), b.ravel(), np.zeros(a.size)))
        pares = cKDTree(x).query_pairs(1.45*h, output_type='ndarray')
        fijos = (np.abs(x[:, :2]) >= q[-1]-1e-8).any(axis=1)
    else:
        q = (np.arange(p.n_cadena)-(p.n_cadena-1)/2)*h
        x = np.column_stack((q, np.zeros_like(q)))
        pares = np.column_stack((np.arange(len(x)-1), np.arange(1, len(x))))
        fijos = np.zeros(len(x), dtype=bool)
        fijos[[0, -1]] = True
    r0 = np.linalg.norm(x[pares[:, 0]]-x[pares[:, 1]], axis=1)
    centro = np.zeros(x.shape[1])
    centro[-1] = -2**(1/6)*(1+p.radio_np)-.5
    return x, pares, r0, fijos, centro, h


def wca(d, sigma):
    """Repulsión WCA desplazada: fuerzas y energía, cero fuera de rc."""
    r = np.linalg.norm(d, axis=1)
    activo = r < 2**(1/6)*sigma
    rr = np.maximum(r, 1e-9)
    q = (sigma/rr)**6
    U = np.where(activo, 4*(q*q-q)+1, 0.)
    f = np.where(activo, 24*(2*q*q-q)/rr**2, 0.)[:, None]*d
    return f, float(U.sum())


def fuerzas(x, phi, centro, enlaces, r0, p, h):
    """Calcula gradientes de WCA, resortes y, en 07, energía dipolar."""
    n = len(x)
    f = np.zeros_like(x)
    torque = np.zeros(n)
    U = 0.
    pares = cKDTree(x).query_pairs(2**(7/6), output_type='ndarray')
    if len(pares):
        i, j = pares.T
        ff, u = wca(x[i]-x[j], 2.)
        np.add.at(f, i, ff)
        np.add.at(f, j, -ff)
        U += u
    k = 2*p.rigidez_reducida/h if p.caso == 6 else 24*p.rigidez_reducida*p.dipolo/h**5
    i, j = enlaces.T
    d = x[i]-x[j]
    r = np.linalg.norm(d, axis=1)
    activo = r < 1.5*h
    reposo = (p.preestres if p.caso == 6 else 1.)*r0
    ff = -k*np.where(activo, (r-reposo)/r, 0.)[:, None]*d
    np.add.at(f, i, ff)
    np.add.at(f, j, -ff)
    # Energía desplazada al corte: el gradiente interior no cambia.
    U += float(np.sum(np.where(activo, .5*k*((r-reposo)**2-(1.5*h-reposo)**2), 0.)))
    if p.caso == 7:
        pares = cKDTree(x).query_pairs(1.5*h, output_type='ndarray')
        if len(pares):
            i, j = pares.T
            d = x[i]-x[j]
            r = np.linalg.norm(d, axis=1)
            e = d/r[:, None]
            m = np.column_stack((np.cos(phi), np.sin(phi)))
            a = np.einsum('ij,ij->i', m[i], e)
            b = np.einsum('ij,ij->i', m[j], e)
            dot = np.einsum('ij,ij->i', m[i], m[j])
            ff = 3*p.dipolo/r[:, None]**4*(b[:, None]*m[i]+a[:, None]*m[j]+(dot-5*a*b)[:, None]*e)
            np.add.at(f, i, ff)
            np.add.at(f, j, -ff)
            ci = m[j]-3*b[:, None]*e
            cj = m[i]-3*a[:, None]*e
            ti = -p.dipolo/r**3*(m[i, 0]*ci[:, 1]-m[i, 1]*ci[:, 0])
            tj = -p.dipolo/r**3*(m[j, 0]*cj[:, 1]-m[j, 1]*cj[:, 0])
            np.add.at(torque, i, ti)
            np.add.at(torque, j, tj)
            U += float(np.sum(p.dipolo/r**3*(dot-3*a*b)))
    ff, u = wca(x-centro, 1+p.radio_np)
    f += ff
    fp = -ff.sum(axis=0)
    U += u
    return f, torque, fp, U


def referencia_analitica(x, h, p, t=np.inf, modos=24):
    """Soluciones de pequeña deformación publicadas; no fuerzan la animación."""
    L = np.ptp(x[:, 0])
    if p.caso == 7:
        P0 = h**4*p.actividad/(12*p.dipolo)
        return P0*(L/2-np.abs(x[:, 0]))
    k = 2*p.rigidez_reducida/h
    P0 = 2*p.actividad/(k*h)
    H = (2*np.arange(1, modos+1)-1)*np.pi/L
    l2 = H[:, None]**2+H[None, :]**2
    coef = h*P0/(6*(1-p.preestres)*l2)
    if np.isfinite(t):
        coef *= -np.expm1(-3*k*h*h*(1-p.preestres)*l2*t)
    return 4/L**2*np.einsum('ip,pq,iq->i', np.cos(x[:, 0, None]*H), coef, np.cos(x[:, 1, None]*H))


def orientar_extremos(x, phi):
    """Dipolos de extremos sin torque: mínimo local de energía dipolar."""
    phi = phi.copy()
    for i, j in ((0, 1), (len(x)-1, len(x)-2)):
        e = x[i]-x[j]
        e /= np.linalg.norm(e)
        m = np.array([np.cos(phi[j]), np.sin(phi[j])])
        campo = 3*np.dot(m, e)*e-m
        phi[i] = np.arctan2(campo[1], campo[0])
    return phi


def simular(p, salida, animar=False):
    """Integra posiciones + orientaciones con reacción sobre la partícula."""
    x0, enlaces, r0, fijos, centro, h = construir(p)
    n, dim = x0.shape
    inicial = np.r_[x0.ravel(), np.zeros(n), centro]
    def rhs(t, y):
        x = y[:n*dim].reshape(n, dim)
        phi = y[n*dim:n*dim+n]
        if p.caso == 7:
            phi = orientar_extremos(x, phi)
        c = y[-dim:]
        f, torque, fp, _ = fuerzas(x, phi, c, enlaces, r0, p, h)
        f[fijos] = 0.
        torque[fijos] = 0.
        fp[-1] += p.actividad
        return np.r_[f.ravel(), .75*torque, fp/p.radio_np]
    tiempos = np.linspace(0, p.tiempo, 121)
    sol = solve_ivp(rhs, (0, p.tiempo), inicial, method='LSODA' if p.caso == 7 else 'RK45',
                    t_eval=tiempos, rtol=p.rtol, atol=p.atol,
                    max_step=min(5., .15*p.radio_np/max(p.actividad, 1e-6)))
    if not sol.success:
        raise RuntimeError(sol.message)
    estados = sol.y[:n*dim].T.reshape(-1, n, dim)
    centros = sol.y[-dim:].T
    phi = sol.y[n*dim:n*dim+n].T
    if p.caso == 7:
        phi = np.array([orientar_extremos(xx, aa) for xx, aa in zip(estados, phi)])
    desplazamiento = estados-x0
    maximo = np.max(np.abs(desplazamiento[:, :, -1]), axis=1)
    carga = []
    for x, a, c in zip(estados, phi, centros):
        carga.append(-fuerzas(x, a, c, enlaces, r0, p, h)[2][-1])
    salida = Path(salida)
    salida.mkdir(parents=True, exist_ok=True)
    np.savetxt(salida/'metricas.csv', np.c_[tiempos, maximo, centros[:, -1], carga], delimiter=',',
               comments='', header='t_reducido,desplazamiento_maximo,centro_np,reaccion_membrana')
    np.savez_compressed(salida/'estados.npz', x=estados, centro=centros, phi=phi, referencia=x0)
    (salida/'parametros.json').write_text(json.dumps(asdict(p), indent=2), encoding='utf-8')
    resumen = dict(desplazamiento_maximo=float(maximo.max()), centro_final=centros[-1].tolist(),
                   evaluaciones=sol.nfev, unidades='a=epsilon=movilidad=1',
                   alcance='Modelo mínimo de membrana; penetración activa, sin inercia ni fluctuación térmica')
    (salida/'resumen.json').write_text(json.dumps(resumen, indent=2), encoding='utf-8')
    dibujar(estados, centros, phi, x0, enlaces, tiempos, maximo, carga, h, p, salida, animar)
    return resumen


def dibujar(estados, centros, phi, x0, enlaces, tiempos, maximo, carga, h, p, salida, animar):
    """Muestra posiciones calculadas, control inmóvil y referencia analítica."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation, PillowWriter
    fig = plt.figure(figsize=(14, 4.5), layout='constrained')
    ax = fig.add_subplot(131, projection='3d' if p.caso == 6 else None)
    curva = fig.add_subplot(132)
    perfil = fig.add_subplot(133)
    curva.plot(tiempos, maximo, label='Modelo no lineal')
    curva.axhline(0, color='gray', ls=':', label='Control sin fuerza activa')
    curva.set(xlabel='Tiempo reducido', ylabel='Desplazamiento normal máximo / a')
    curva.legend()
    L = np.ptp(x0[:, 0])
    seleccion = np.ones(len(x0), dtype=bool)
    if p.caso == 6:
        seleccion = np.isclose(x0[:, 1], np.unique(x0[:, 1])[p.n_lado//2])
    final = estados[-1, seleccion]
    orden = np.argsort(x0[seleccion, 0])
    xx = x0[seleccion][orden]
    perfil.plot(xx[:, 0], final[orden, -1], 'o-', ms=3, label='Modelo no lineal')
    perfil.plot(xx[:, 0], referencia_analitica(xx, h, p), '--', label='Límite analítico publicado')
    perfil.set(xlabel='x/a', ylabel='Desplazamiento normal / a', title='Perfil final y referencia independiente')
    perfil.legend(fontsize=8)
    def cuadro(i):
        ax.clear()
        x = estados[i]
        c = centros[i]
        if p.caso == 6:
            for j in range(p.n_lado):
                z = x[j*p.n_lado:(j+1)*p.n_lado]
                ax.plot(*z.T, lw=.6, c='#2360a0')
                z = x[j::p.n_lado]
                ax.plot(*z.T, lw=.6, c='#2360a0')
            u = np.linspace(0, 2*np.pi, 16)
            v = np.linspace(0, np.pi, 9)
            ax.plot_wireframe(c[0]+p.radio_np*np.outer(np.cos(u), np.sin(v)),
                              c[1]+p.radio_np*np.outer(np.sin(u), np.sin(v)),
                              c[2]+p.radio_np*np.outer(np.ones_like(u), np.cos(v)), color='#b64036', lw=.6)
            ax.set(zlim=(-4, max(3., maximo.max()*1.2)), xlabel='x/a', ylabel='y/a', zlabel='')
        else:
            from matplotlib.patches import Circle
            ax.plot(x0[:, 0], x0[:, 1], ':', color='gray', label='Control')
            ax.plot(x[:, 0], x[:, 1], 'o-', ms=4, label='Cadena dipolar')
            ax.quiver(x[:, 0], x[:, 1], np.cos(phi[i]), np.sin(phi[i]), angles='xy', scale_units='xy', scale=1, width=.003)
            ax.plot(x0[:, 0], referencia_analitica(x0, h, p), '--', label='Ec. 43: límite pequeño')
            ax.add_patch(Circle(c, p.radio_np, color='#b64036', alpha=.7))
            ax.set(xlim=(-6, 6), ylim=(-4, max(3, maximo.max()*1.3)), xlabel='x/a (zona central)', ylabel='y/a')
            ax.set_aspect('equal')
            ax.legend(fontsize=8)
        ax.set_title(f'Caso {p.caso:02d}: contacto activo; t={tiempos[i]:.1f}'+('\nEje z/a ampliado' if p.caso == 6 else ''))
        return []
    cuadro(len(estados)-1)
    fig.savefig(salida/'simulacion.png', dpi=140)
    if animar:
        FuncAnimation(fig, cuadro, frames=len(estados), interval=50).save(salida/'simulacion.gif', writer=PillowWriter(fps=20))
    plt.close(fig)
