"""Impacto temprano en piel: reducción axisimétrica de Shen et al. (2025).

DOI 10.1016/j.taml.2024.100567, ecuación 7 y tablas 1-3.
Conserva la energía de Ogden publicada. Usa triángulos FEM axisimétricos
en lugar del acoplamiento SPH-FEM 3D de RADIOSS. No modela perforación.
Unidades internas SI. Véase PIEL_OGDEN.md antes de interpretar resultados.
"""
from dataclasses import dataclass, asdict
from pathlib import Path
import argparse
import json
import numpy as np


@dataclass
class Parametros:
    diametro: float = 58.5e-6
    velocidad: float = 200.
    mu: float = 10.
    alfa: float = 16.
    nu: float = .48
    radio_dominio: float = 160e-6
    profundidad: float = 200e-6
    nr: int = 24
    nz: int = 30
    hueco: float = 5e-6
    dt: float = 1e-10
    tiempo: float = 4e-8
    penalidad: float = 2e15


def malla(p):
    """Triángulos lineales en (radio, profundidad), con volumen de revolución."""
    rr = np.linspace(0, p.radio_dominio, p.nr+1)
    zz = np.linspace(0, p.profundidad, p.nz+1)
    r, z = np.meshgrid(rr, zz)
    x = np.column_stack((r.ravel(), z.ravel()))
    tri = []
    for j in range(p.nz):
        for i in range(p.nr):
            a = j*(p.nr+1)+i
            b, c, d = a+1, a+p.nr+1, a+p.nr+2
            tri.extend(((a, b, d), (a, d, c)))
    tri = np.asarray(tri)
    xx = x[tri]
    dm = np.stack((xx[:, 1]-xx[:, 0], xx[:, 2]-xx[:, 0]), axis=-1)
    inv = np.linalg.inv(dm)
    grad = np.concatenate((-inv.sum(axis=1)[:, None, :], inv), axis=1)
    radio = xx[:, :, 0].mean(axis=1)
    vol = .5*np.linalg.det(dm)*2*np.pi*radio
    rho = np.where(xx[:, :, 1].mean(axis=1) < 86e-6, 1217., 1116.)
    masa = np.zeros(len(x))
    for k in range(3):
        np.add.at(masa, tri[:, k], rho*vol/3)
    fijos = np.zeros_like(x, dtype=bool)
    fijos[x[:, 0] == 0, 0] = True
    fijos[(x[:, 0] == rr[-1]) | (x[:, 1] == zz[-1])] = True
    # Área anular de cada nodo de la superficie, incluida el área del eje.
    bordes = np.r_[0., (rr[:-1]+rr[1:])/2, rr[-1]]
    area = np.pi*np.diff(bordes**2)
    return x, tri, grad, radio, vol, masa, fijos, area


def energia_tension(F, p):
    """W y primera tensión de Piola: derivada exacta de la energía publicada.

    W = mu/alfa*(sum(lambda_bar**alfa)-3) + K/2*(J-1)**2.
    Se preserva el prefactor mu/alfa del artículo; no se sustituye por
    2*mu/alfa**2. Una inversión de elemento produce una excepción.
    """
    J = np.linalg.det(F)
    if np.any(J <= 0):
        raise ValueError('Inversión de elemento; reducir tiempo o paso y refinar malla')
    U, s, vh = np.linalg.svd(F)
    q = (s/J[:, None]**(1/3))**p.alfa
    K = p.mu*2*(1+p.nu)/(3*(1-2*p.nu))
    W = p.mu/p.alfa*(q.sum(axis=1)-3)+K/2*(J-1)**2
    principal = (p.mu*(q-q.mean(axis=1)[:, None])
                 +K*((J-1)*J)[:, None])/s
    P = (U*principal[:, None, :])@vh
    return W, P, J


def fuerzas_internas(x, tri, grad, radio, vol, p):
    """Integra -dW/dx; incorpora el término circunferencial axisimétrico."""
    xx = x[tri]
    F = np.zeros((len(tri), 3, 3))
    F[:, :2, :2] = np.einsum('eia,eib->eab', xx, grad)
    F[:, 2, 2] = xx[:, :, 0].mean(axis=1)/radio
    W, P, J = energia_tension(F, p)
    fe = -vol[:, None, None]*np.einsum('eab,eib->eia', P[:, :2, :2], grad)
    fe[:, :, 0] -= (vol*P[:, 2, 2]/(3*radio))[:, None]
    f = np.zeros_like(x)
    for k in range(3):
        np.add.at(f, tri[:, k], fe[:, k])
    return f, float(vol@W), J


def contacto(x, centro_z, p, areas):
    """Contacto unilateral esfera/superficie; fuerzas opuestas y energía penal."""
    arriba = x[:p.nr+1]
    d = arriba-np.array([0., centro_z])
    distancia = np.linalg.norm(d, axis=1)
    normal = d/np.maximum(distancia[:, None], 1e-30)
    solape = np.maximum(p.diametro/2-distancia, 0.)
    fn = p.penalidad*areas*solape
    f = np.zeros_like(x)
    f[:p.nr+1] = fn[:, None]*normal
    reaccion = -float(f[:, 1].sum())
    energia = float(.5*p.penalidad*np.dot(areas, solape**2))
    return f, reaccion, energia, float(solape.max())


def poncelet(t, p, rho=1217., resistencia=12e6):
    """Solución de las ecuaciones 1-6, solo para una capa homogénea.

    Es una comparación independiente: no calcula la deformación FEM y no
    se suma a las fuerzas de contacto del modelo de Ogden.
    """
    m = 7800*np.pi*p.diametro**3/6
    B = rho*np.pi*p.diametro**2*.35/8
    C = resistencia*np.pi*p.diametro**2/4
    tf = m/np.sqrt(B*C)*np.arctan(p.velocidad*np.sqrt(B/C))
    tt = np.clip(np.asarray(t), 0, tf)
    a = np.sqrt(B*C)/m
    z = m/B*(np.log(np.cos(a*(tf-tt)))-np.log(np.cos(a*tf)))
    v = np.sqrt(C/B)*np.tan(a*(tf-tt))
    return z, v, tf


def simular(p, salida, animar=False):
    """Velocity Verlet acoplado: posiciones de piel y esfera integradas juntas."""
    x0, tri, grad, radio, vol, masas, fijos, areas = malla(p)
    x, v = x0.copy(), np.zeros_like(x0)
    cz, vz = -p.diametro/2-p.hueco, p.velocidad
    mp = 7800*np.pi*p.diametro**3/6
    pasos = round(p.tiempo/p.dt)
    cada = max(1, pasos//100)
    estados, centros, datos = [], [], []
    def evaluar(xx, z):
        fi, U, J = fuerzas_internas(xx, tri, grad, radio, vol, p)
        fc, fp, uc, solape = contacto(xx, z, p, areas)
        f = fi+fc
        f[fijos] = 0.
        return f/masas[:, None], fp/mp, U, uc, J, solape
    a, ap, U, uc, J, solape = evaluar(x, cz)
    for k in range(pasos+1):
        if k % cada == 0 or k == pasos:
            ec = .5*np.sum(masas[:, None]*v*v)+.5*mp*vz*vz
            u = np.linalg.norm(x-x0, axis=1).max()
            datos.append((k*p.dt, cz, vz, u, U, uc, ec, J.min(), solape))
            estados.append(x.copy())
            centros.append(cz)
        if k == pasos:
            break
        v += .5*p.dt*a
        vz += .5*p.dt*ap
        x += p.dt*v
        x[fijos] = x0[fijos]
        cz += p.dt*vz
        a, ap, U, uc, J, solape = evaluar(x, cz)
        v += .5*p.dt*a
        vz += .5*p.dt*ap
    salida = Path(salida)
    salida.mkdir(parents=True, exist_ok=True)
    datos = np.asarray(datos)
    np.savetxt(salida/'PIEL_METRICAS.csv', datos, delimiter=',',
               header='t_s,centro_z_m,v_m_s,u_max_m,U_J,U_contacto_J,Ec_J,J_min,solape_max_m', comments='')
    (salida/'PIEL_PARAMETROS.json').write_text(json.dumps(asdict(p), indent=2), encoding='utf-8')
    np.savez_compressed(salida/'PIEL_ESTADOS.npz', x=estados, x0=x0, tri=tri,
                        centro_z=centros, t=datos[:, 0])
    if animar:
        representar(np.asarray(estados), x0, tri, np.asarray(centros), datos, p, salida)
    return datos, np.asarray(estados)


def representar(estados, x0, tri, centros, datos, p, salida):
    """Dibuja coordenadas integradas y desplazamiento; jamás prescribe la forma."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation, PillowWriter
    from matplotlib.patches import Circle
    fig, (ax, curva) = plt.subplots(1, 2, figsize=(10, 5))
    # Corte meridional: media esfera y tejido axisimétrico, escala 1:1.
    desplazamientos = np.linalg.norm(estados-x0, axis=2)*1e6
    maxu = max(1., desplazamientos.max())
    def cuadro(i):
        ax.clear()
        im = ax.tripcolor(estados[i, :, 0]*1e6, estados[i, :, 1]*1e6,
                          tri, desplazamientos[i], shading='gouraud',
                          vmin=0, vmax=maxu, cmap='viridis')
        ax.triplot(estados[i, :, 0]*1e6, estados[i, :, 1]*1e6, tri,
                   color='white', lw=.2, alpha=.3)
        ax.add_patch(Circle((0, centros[i]*1e6), p.diametro*5e5, color='tomato'))
        ax.set(xlim=(0, 100), ylim=(120, -75), xlabel='Radio (µm)',
               ylabel='Profundidad (µm)', title=f'Ogden axisimétrico | t={datos[i,0]*1e9:.1f} ns')
        ax.set_aspect('equal')
        curva.clear()
        curva.plot(datos[:, 0]*1e9, datos[:, 3]*1e6, color='steelblue')
        curva.axvline(datos[i, 0]*1e9, color='tomato')
        curva.set(xlabel='Tiempo (ns)', ylabel='Desplazamiento máximo (µm)',
                  title='Deformación calculada del tejido')
        curva.grid(alpha=.25)
        return im,
    cuadro(len(estados)-1)
    fig.suptitle('Shen et al. 2025: reducción docente FEM; fase temprana sin perforación')
    fig.tight_layout()
    fig.savefig(salida/'piel_ogden.png', dpi=150)
    FuncAnimation(fig, cuadro, frames=len(estados), interval=60).save(
        salida/'piel_ogden.gif', writer=PillowWriter(fps=16))
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--animar', action='store_true')
    parser.add_argument('--control', action='store_true', help='Esfera inmóvil sin contacto')
    parser.add_argument('--dt', type=float, default=1e-10)
    parser.add_argument('--mu', type=float, choices=(7., 10., 12.), default=10.)
    parser.add_argument('--alfa', type=float, choices=(14., 16., 23.), default=16.)
    parser.add_argument('--salida', default='resultados/piel_ogden')
    args = parser.parse_args()
    if not 0 < args.dt <= 2e-10:
        parser.error('Usar 0 < dt <= 2e-10 s')
    p = Parametros(dt=args.dt, mu=args.mu, alfa=args.alfa,
                   velocidad=0. if args.control else 200.)
    datos, _ = simular(p, args.salida, args.animar)
    print(f'u_max={datos[:,3].max()*1e6:.6g} µm; J_min={datos[:,7].min():.6g}')


if __name__ == '__main__':
    main()
