"""Célula bicapa 2D: implementación didáctica del marco DEM de Campello y Zohdi.

Referencias: 10.1002/cnm.2649 y 10.3970/cmes.2014.098.221.
Unidades nm, ns, fg, nN. No replica las figuras publicadas: discretización y
chorro reducidos, RK2 y contacto unilateral declarados en CASOS_CELULARES.md.
"""
from dataclasses import dataclass, asdict
from pathlib import Path
import json
import numpy as np
from piloto_membrana import fuerzas_enlaces, fuerzas_contacto


@dataclass
class ParametrosCelula:
    articulo: str = "10.1002/cnm.2649"
    radio_externo: float = 50.
    espesor: float = 10.
    nodos_capa: int = 90
    radio_lipido: float = 1.25
    diametro_proyectil: float = 1.25
    velocidad: float = 100.
    numero_proyectiles: int = 12
    ancho_chorro: float = 10.
    semilla: int = 42
    diametros_aleatorios: bool = False
    k: float = .005
    c: float = 1e-5
    E: float = 100.
    nu: float = .25
    xi: float = .1
    friccion: float = .1
    arrastre: float = 5e-6
    presion_por_nodo: float = 6.5e-5
    critica_circunferencial: float = .5
    critica_transversal: float = .5
    dt: float = 2e-5
    tiempo_final: float = 2.


def crear_celula(p):
    """Dos anillos sin solapamiento inicial y cinco enlaces por nodo.

    Cada nodo tiene dos vecinos circunferenciales, uno radial y dos cruzados.
    Las longitudes de reposo se calculan de la geometría inicial.
    """
    n = p.nodos_capa
    angulo = np.arange(n)*2*np.pi/n
    er = np.column_stack((np.cos(angulo), np.sin(angulo)))
    rin = p.radio_externo-p.espesor+p.radio_lipido
    rout = p.radio_externo-p.radio_lipido
    x = np.concatenate((rin*er, rout*er))
    pares, criticas = [], []
    for i in range(n):
        for capa in (0, 1):
            pares.append((capa*n+i, capa*n+(i+1) % n))
            criticas.append(p.critica_circunferencial)
        for desplazamiento in (-1, 0, 1):
            pares.append((i, n+(i+desplazamiento) % n))
            criticas.append(p.critica_transversal)
    pares = np.asarray(pares, int)
    radios = np.full(2*n, p.radio_lipido)
    rng = np.random.default_rng(p.semilla)
    m = p.numero_proyectiles
    diam = np.full(m, p.diametro_proyectil)
    if p.diametros_aleatorios:
        diam = rng.normal(p.diametro_proyectil, .1*p.diametro_proyectil, m)
        if np.any(diam <= 0):
            raise ValueError("La muestra incluye diámetro no físico")
    # Chorro pequeño regular; su geometría no es el empaquetamiento original.
    jet = []
    separacion = max(1.5*diam.max(initial=1.), 2.)
    columnas = max(1, int(p.ancho_chorro/separacion))
    for i in range(m):
        jet.append((-p.radio_externo-10-diam[i]/2-(i//columnas)*separacion,
                    (i % columnas-(columnas-1)/2)*separacion))
    if m:
        x = np.concatenate((x, np.asarray(jet)))
        radios = np.r_[radios, diam/2]
    rho = np.r_[np.full(2*n, 9e-7), np.full(m, 1e-6)]
    masas = 4*np.pi*radios**3*rho/3
    v = np.zeros_like(x)
    v[2*n:, 0] = p.velocidad
    l0 = np.linalg.norm(x[pares[:, 1]]-x[pares[:, 0]], axis=1)
    return x, v, radios, masas, pares, l0, np.asarray(criticas)


def normales_internas(x, n):
    """Normal exterior de una curva cerrada antihoraria, actualizada en cada paso."""
    anillo = x[:n]
    tangente = np.roll(anillo, -1, axis=0)-np.roll(anillo, 1, axis=0)
    normal = np.column_stack((tangente[:, 1], -tangente[:, 0]))
    normal /= np.maximum(np.linalg.norm(normal, axis=1)[:, None], 1e-15)
    return normal


def fuerza_pared(x, v, radios, masas, p):
    """Pared rígida a la derecha: Hertz amortiguado y fricción de deslizamiento."""
    f = np.zeros_like(x)
    pared = p.radio_externo+.5
    h = np.maximum(x[:, 0]+radios-pared, 0)
    ee = p.E/(1-p.nu**2)
    d = 2*p.xi*np.sqrt(2*np.sqrt(radios)*ee*masas)*h**.25
    normal = np.maximum(0, 4/3*np.sqrt(radios)*ee*h**1.5+d*v[:, 0])
    f[:, 0] = -normal
    f[:, 1] = -p.friccion*normal*np.sign(v[:, 1])
    return f


def interior_poligono(puntos, poligono):
    """Prueba geométrica por cruces de rayo; no usa un radio celular constante."""
    dentro = np.zeros(len(puntos), dtype=bool)
    if not len(puntos):
        return dentro
    px, py = puntos.T
    for a, b in zip(poligono, np.roll(poligono, -1, axis=0)):
        cruza = (a[1] > py) != (b[1] > py)
        if b[1] != a[1]:
            xx = a[0]+(py-a[1])*(b[0]-a[0])/(b[1]-a[1])
            dentro ^= cruza & (px < xx)
    return dentro


def simular_celula(p):
    """Integra la dinámica acoplada y guarda posiciones, enlaces y métricas."""
    x, v, radios, masas, enlaces, l0, critica = crear_celula(p)
    x0 = x.copy()
    n = p.nodos_capa
    activos = np.ones(len(enlaces), bool)
    pasos = int(np.ceil(p.tiempo_final/p.dt))
    dt = p.tiempo_final/pasos
    indices = set(np.linspace(0, pasos, 101).astype(int))
    ts, xs, es, ms = [], [], [], []

    def fuerza(pos, vel):
        f = fuerzas_enlaces(pos, vel, enlaces, l0, activos, p)
        f += fuerzas_contacto(pos, vel, radios, masas, p)
        f += fuerza_pared(pos, vel, radios, masas, p)-p.arrastre*vel
        f[:n] += p.presion_por_nodo*normales_internas(pos, n)
        return f

    def deformacion(pos):
        return np.linalg.norm(pos[enlaces[:, 1]]-pos[enlaces[:, 0]], axis=1)/l0-1

    for k in range(pasos+1):
        eps = deformacion(x)
        activos &= eps < critica
        if k in indices:
            ts.append(k*dt); xs.append(x.copy()); es.append(activos.copy())
            u = np.linalg.norm(x[:2*n]-x0[:2*n], axis=1).max()
            circ = np.array([i % 5 < 2 for i in range(len(enlaces))])
            # Si hay rotura circunferencial, un contorno cerrado no define una célula sellada.
            unidos = bool(activos[circ].all())
            dr = (interior_poligono(x[2*n:], x[:n]).mean()
                  if p.numero_proyectiles and unidos else np.nan)
            dam = eps[~activos].sum()
            ms.append((k*dt, u, eps.max(), (~activos).sum(), dr, dam))
        if k == pasos:
            break
        a0 = fuerza(x, v)/masas[:, None]
        xm, vm = x+dt*v/2, v+dt*a0/2
        a1 = fuerza(xm, vm)/masas[:, None]
        x += dt*vm; v += dt*a1
        if k % 5000 == 0 and not (np.isfinite(x).all() and np.isfinite(v).all()):
            raise FloatingPointError("Inestabilidad: revisar paso y unidades")
    return dict(t=np.array(ts), x=np.array(xs), activos=np.array(es),
                enlaces=enlaces, radios=radios, metricas=np.array(ms),
                nm=2*n, n=n, parametros=asdict(p))


def guardar_celula(d, carpeta, animar=False):
    """Exporta resultados y, opcionalmente, una animación de la solución calculada."""
    carpeta = Path(carpeta); carpeta.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(carpeta/"estados.npz", **{k:v for k,v in d.items() if k!='parametros'})
    (carpeta/"parametros.json").write_text(json.dumps(d['parametros'], indent=2),encoding='utf8')
    np.savetxt(carpeta/"metricas.csv",d['metricas'],delimiter=',',
               header='t_ns,u_max_nm,eps_max,enlaces_rotos,fraccion_interior_si_cerrada,DAM',comments='')
    if animar:
        animar_celula(d, carpeta/"impacto.gif")


def animar_celula(d, archivo):
    """Nodos deformables y esferas con radio geométrico; no impone perfiles al blanco."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation, PillowWriter
    from matplotlib.collections import LineCollection,PatchCollection
    from matplotlib.patches import Circle
    fig,(ax,curva)=plt.subplots(1,2,figsize=(10,5),layout='constrained')
    nm=d['nm'];x0=d['x'][0];pares=d['enlaces'];R=d['parametros']['radio_externo']
    lineas=LineCollection(x0[pares],colors='#6899b4',linewidths=.6)
    ax.add_collection(lineas)
    vmax=max(float(d['metricas'][:,1].max()),.1)
    nodos=ax.scatter(*x0[:nm].T,c=np.zeros(nm),vmin=0,vmax=vmax,cmap='viridis',s=10)
    esferas=PatchCollection([Circle(tuple(x),r) for x,r in zip(x0[nm:],d['radios'][nm:])],
                             facecolor='#d88919',edgecolor='#9f6106')
    ax.add_collection(esferas)
    ax.axvline(R+.5,color='gray',linewidth=2)
    xmin=min(float(d['x'][:,:,0].min())-5,-R-20)
    ymax=max(R+8,float(np.abs(d['x'][:,:,1]).max())+5)
    ax.set(xlim=(xmin,R+8),ylim=(-ymax,ymax),aspect='equal',xlabel='x (nm)',ylabel='y (nm)')
    curva.plot(d['t'],d['metricas'][:,1],color='#2481a6')
    cursor=curva.axvline(0,color='#d88919')
    curva.set(xlabel='t (ns)',ylabel='Desplazamiento máximo del blanco (nm)')
    fig.colorbar(nodos,ax=ax,shrink=.55,label='Desplazamiento nodal (nm)')
    titulo=fig.suptitle('')
    def actualizar(i):
        x=d['x'][i]
        lineas.set_segments(x[pares[d['activos'][i]]])
        nodos.set_offsets(x[:nm]);nodos.set_array(np.linalg.norm(x[:nm]-x0[:nm],axis=1))
        esferas.set_paths([Circle(tuple(q),r) for q,r in zip(x[nm:],d['radios'][nm:])])
        cursor.set_xdata([d['t'][i]]*2)
        titulo.set_text(f"Célula DEM 2D, reducción didáctica — t={d['t'][i]:.3f} ns\n"
                        f"DOI {d['parametros']['articulo']} | enlaces rotos: {int(d['metricas'][i,3])}")
    cuadros=np.unique(np.linspace(0,len(d['t'])-1,70).astype(int))
    FuncAnimation(fig,actualizar,frames=cuadros,interval=70).save(archivo,writer=PillowWriter(fps=14))
    actualizar(int(np.argmax(d['metricas'][:,1])))
    fig.savefig(Path(archivo).with_suffix('.png'),dpi=130)
    plt.close(fig)
