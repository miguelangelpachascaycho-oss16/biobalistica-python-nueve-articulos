"""Colisión con vesícula HTTT: piloto reducido de Arai et al. (2013).

DOI 10.1039/C3NR02024J, ecuaciones 1-7. Unidades DPD: rc=m=kBT=1.
Leer VESICULA_DPD.md: geometría, integrador y parámetros incompletos del
artículo impiden llamar a este piloto una réplica cuantitativa.
"""
from dataclasses import dataclass, asdict
from pathlib import Path
import argparse
import json
import numpy as np
from scipy.spatial import cKDTree


@dataclass
class Parametros:
    caja: tuple = (14., 14., 18.)
    radio_externo: float = 5.
    radio_interno: float = 2.
    area_lipido: float = .8
    radio_np: float = 1.1
    hueco: float = .65
    velocidad: float = 6.
    rs: float = .86
    C: float = 100.
    gamma: float = 4.5
    sigma: float = 3.
    dt: float = .004
    equilibrar: int = 1200
    pasos: int = 1800
    semilla: int = 2026


def esfera_fibonacci(n):
    """Direcciones aproximadamente uniformes; no añade enlaces entre lípidos."""
    z = 1-2*(np.arange(n)+.5)/n
    a = np.arange(n)*np.pi*(3-np.sqrt(5))
    r = np.sqrt(1-z*z)
    return np.column_stack((r*np.cos(a), r*np.sin(a), z))


def construir(p):
    """Vesícula de cadenas HTTT y agua explícita en una caja periódica."""
    centro = np.array(p.caja)/2
    cadenas = []
    for radio, signo in ((p.radio_externo, -1), (p.radio_interno, 1)):
        n = round(4*np.pi*radio**2/p.area_lipido)
        normal = esfera_fibonacci(n)
        radios = radio+signo*np.arange(4)*.75
        cadenas.append(centro+normal[:, None, :]*radios[None, :, None])
    lipidos = np.concatenate(cadenas).reshape(-1, 3)
    tipo = np.tile([0, 1, 1, 1], len(lipidos)//4)  # H=0, T=1, W=2, B=3
    base = np.arange(0, len(lipidos), 4)
    enlaces = np.column_stack((np.repeat(base, 3)+np.tile([0, 1, 2], len(base)),
                               np.repeat(base, 3)+np.tile([1, 2, 3], len(base))))
    paso = (1/3)**(1/3)
    ejes = [np.arange(paso/2, L, paso) for L in p.caja]
    agua = np.stack(np.meshgrid(*ejes, indexing='ij'), axis=-1).reshape(-1, 3)
    r = np.linalg.norm(agua-centro, axis=1)
    agua = agua[(r < p.radio_interno-.45) | (r > p.radio_externo+.45)]
    x = np.concatenate((lipidos, agua))
    tipo = np.r_[tipo, np.full(len(agua), 2)]
    v = np.random.default_rng(p.semilla).normal(size=x.shape)
    v -= v.mean(axis=0)
    return x, v, tipo, enlaces, len(lipidos)


def matriz_repulsion():
    """a_ij del artículo; H-T y H-B completados por identidad hidrofílica.

    Estas dos entradas no se enumeran en la publicación. La guía las marca
    como elecciones docentes, no como datos reproducidos del artículo.
    """
    A = np.full((4, 4), 25.)
    A[1, [0, 2, 3]] = 80.
    A[[0, 2, 3], 1] = 80.
    return A


def fuerzas(x, v, tipo, enlaces, p, rng, ruido=True):
    """Fuerzas DPD por pares + resortes HTTT; acción y reacción exactas.

    d apunta de i hacia j. La fuerza disipativa sobre i lleva signo positivo
    con esta convención: su potencia por par es -gamma*w²*(dv.n)² <= 0.
    Se corrige la incompatibilidad de signo de la ec. 3 del texto.
    C se interpreta como la amplitud de fuerza de la ec. 7 en unidades DPD.
    """
    caja = np.array(p.caja)
    pares = cKDTree(x % caja, boxsize=caja).query_pairs(1., output_type='ndarray')
    i, j = pares.T
    d = x[j]-x[i]
    d -= caja*np.rint(d/caja)
    r = np.linalg.norm(d, axis=1)
    n = d/np.maximum(r[:, None], 1e-12)
    w = np.maximum(1-r, 0.)
    dv = np.einsum('ij,ij->i', v[j]-v[i], n)
    a = matriz_repulsion()[tipo[i], tipo[j]]
    fn = -a*w+p.gamma*w*w*dv
    if ruido:
        fn += p.sigma*w*rng.normal(size=len(i))/np.sqrt(p.dt)
    f = np.zeros_like(x)
    np.add.at(f, i, fn[:, None]*n)
    np.add.at(f, j, -fn[:, None]*n)
    U = float(np.sum(.5*a*w*w))
    i, j = enlaces.T
    d = x[j]-x[i]
    d -= caja*np.rint(d/caja)
    r = np.linalg.norm(d, axis=1)
    fb = p.C*(r/p.rs-1)[:, None]*d/np.maximum(r[:, None], 1e-12)
    np.add.at(f, i, fb)
    np.add.at(f, j, -fb)
    U += float(np.sum(p.C/(2*p.rs)*(r-p.rs)**2))
    return f, U


def paso_dpd(x, v, tipo, enlaces, p, rng, np_inicio=None):
    """Paso kick-drift DPD explícito; proyecta la NP a traslación rígida.

    No implementa RATTLE ni Lowe. Su convergencia debe medirse bajando dt.
    La suma de las fuerzas sobre sus beads determina la aceleración COM.
    """
    f, U = fuerzas(x, v, tipo, enlaces, p, rng)
    if np_inicio is not None:
        f[np_inicio:] = f[np_inicio:].mean(axis=0)
    v = v+p.dt*f
    x = (x+p.dt*v) % np.array(p.caja)
    return x, v, U


def agregar_np(x, v, tipo, p):
    """NP hidrofílica rígida de beads, con hueco medido desde la superficie."""
    centro = np.array(p.caja)/2
    centro[2] += p.radio_externo+p.radio_np+p.hueco
    # Malla cúbica reducida: no es la red diamante de 2149 beads publicada.
    a = np.arange(-p.radio_np, p.radio_np+.01, .42)
    d = np.stack(np.meshgrid(a, a, a, indexing='ij'), axis=-1).reshape(-1, 3)
    d = d[np.linalg.norm(d, axis=1) <= p.radio_np]
    d -= d.mean(axis=0)
    radio = np.linalg.norm(x-centro, axis=1)
    quitar = (tipo == 2) & (radio < p.radio_np+.25)
    x, v, tipo = x[~quitar], v[~quitar], tipo[~quitar]
    inicio = len(x)
    return (np.concatenate((x, centro+d)), np.concatenate((v, np.zeros_like(d))),
            np.r_[tipo, np.full(len(d), 3)], inicio)


def observables(x, v, nl, inicio, xref, p):
    """Mide desplazamiento no rígido, asfericidad y energía de la NP."""
    caja = np.array(p.caja)
    # Coordenadas continuas de la vesícula respecto al centro original.
    xx = x[:nl]-caja/2
    xx -= caja*np.rint(xx/caja)
    xx -= xx.mean(axis=0)
    ref = xref[:nl]-caja/2
    ref -= caja*np.rint(ref/caja)
    ref -= ref.mean(axis=0)
    # Kabsch: elimina también la mejor rotación rígida. La difusión de
    # lípidos aún contribuye al RMS; no es una deformación unitaria local.
    a, _, bh = np.linalg.svd(xx.T@ref)
    rot = a@np.diag([1., 1., np.linalg.det(a@bh)])@bh
    u = np.sqrt(np.mean(np.sum((xx@rot-ref)**2, axis=1)))
    eig = np.linalg.eigvalsh(xx.T@xx/nl)
    asp = 1-3*(eig[0]*eig[1]+eig[1]*eig[2]+eig[2]*eig[0])/eig.sum()**2
    return float(u), float(asp), float(.5*np.sum(v[inicio:]**2))


def simular(p, salida, animar=False):
    """Equilibra una vez y ejecuta impacto + control desde el mismo estado."""
    salida = Path(salida)
    salida.mkdir(parents=True, exist_ok=True)
    x, v, tipo, enlaces, nl = construir(p)
    rng = np.random.default_rng(p.semilla+1)
    for _ in range(p.equilibrar):
        x, v, _ = paso_dpd(x, v, tipo, enlaces, p, rng)
    x, v, tipo, inicio = agregar_np(x, v, tipo, p)
    xref, vref = x.copy(), v.copy()
    estados, controles, datos = [], [], []
    for nombre, vel in (('impacto', p.velocidad), ('control', 0.)):
        xx, vv = xref.copy(), vref.copy()
        vv[inicio:, 2] = -vel
        rng = np.random.default_rng(p.semilla+2)
        serie = []
        for k in range(p.pasos+1):
            if k % max(1, p.pasos//90) == 0 or k == p.pasos:
                u, asp, ec = observables(xx, vv, nl, inicio, xref, p)
                serie.append([k*p.dt, u, asp, ec, xx[inicio:, 2].mean()])
                (estados if nombre == 'impacto' else controles).append(xx.copy())
            if k < p.pasos:
                xx, vv, _ = paso_dpd(xx, vv, tipo, enlaces, p, rng, inicio)
                if not np.isfinite(xx).all():
                    raise ValueError('Estado no finito; reducir dt')
        datos.append(np.array(serie))
    imp, ctrl = datos
    tabla = np.column_stack((imp, ctrl[:, 1:]))
    np.savetxt(salida/'VESICULA_METRICAS.csv', tabla, delimiter=',', comments='',
               header='t_DPD,u_rms_impacto,asfericidad_impacto,Ec_NP_impacto,z_NP_impacto,u_rms_control,asfericidad_control,Ec_NP_control,z_NP_control')
    np.savez_compressed(salida/'VESICULA_ESTADOS.npz', impacto=estados, control=controles,
                        tipo=tipo, nl=nl, inicio=inicio, referencia=xref)
    (salida/'VESICULA_PARAMETROS.json').write_text(json.dumps(asdict(p), indent=2), encoding='utf-8')
    dibujar(estados, controles, tipo, nl, inicio, imp, ctrl, p, salida, animar)
    return tabla


def dibujar(estados, controles, tipo, nl, inicio, imp, ctrl, p, salida, animar):
    """Dibuja coordenadas calculadas; el agua no se muestra para ver la bicapa."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation, PillowWriter
    fig, ax = plt.subplots(1, 3, figsize=(13, 4), layout='constrained')
    colores = np.array(['#2563a6', '#de8441', '#999999', '#333333'])
    def cuadro(k):
        for a, lista, titulo in zip(ax[:2], (estados, controles), ('Impacto', 'Control: velocidad inicial cero')):
            a.clear()
            x = lista[k]
            # Corte de espesor finito, no toda la vesícula superpuesta.
            mascara = (np.abs(x[:, 1]-p.caja[1]/2) < 1.) & (tipo != 2)
            a.scatter(x[mascara, 0], x[mascara, 2], s=8, c=colores[tipo[mascara]])
            a.set(xlim=(0, p.caja[0]), ylim=(0, p.caja[2]), xlabel='x / rc', ylabel='z / rc',
                  title=titulo+f'\nt = {imp[k, 0]:.2f} DPD')
            a.set_aspect('equal')
        return []
    ax[2].plot(imp[:, 0], imp[:, 2], label='Impacto')
    ax[2].plot(ctrl[:, 0], ctrl[:, 2], label='Control')
    ax[2].set(xlabel='Tiempo DPD', ylabel='Asfericidad (adimensional)',
              title='Cambio de forma global calculado')
    ax[2].legend()
    cuadro(len(estados)-1)
    fig.savefig(salida/'vesicula_dpd.png', dpi=140)
    if animar:
        FuncAnimation(fig, cuadro, frames=len(estados), interval=60).save(
            salida/'vesicula_dpd.gif', writer=PillowWriter(fps=15))
    plt.close(fig)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--salida', default='resultados/vesicula')
    parser.add_argument('--animar', action='store_true')
    parser.add_argument('--velocidad', type=float, default=6.)
    parser.add_argument('--pasos', type=int, default=1800)
    parser.add_argument('--equilibrar', type=int, default=1200)
    parser.add_argument('--dt', type=float, default=.004)
    args = parser.parse_args()
    p = Parametros(velocidad=args.velocidad, pasos=args.pasos, equilibrar=args.equilibrar, dt=args.dt)
    print(simular(p, args.salida, args.animar)[-1])
