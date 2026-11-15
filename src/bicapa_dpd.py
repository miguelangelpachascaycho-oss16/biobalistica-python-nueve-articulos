"""DPD reducido de dos artículos distintos: Zhang 2015 y Yong/Du 2023.

Beads explícitos, resortes, ángulos y cuerpos rígidos con rotación. No es una
réplica de los tiempos, barostatos o diagramas de los artículos. Ver guías.
Unidades reducidas rc=m=kBT=1; se integra con kick-drift de primer orden.
"""
from dataclasses import dataclass, asdict
from pathlib import Path
import json
import numpy as np
from scipy.spatial import cKDTree
from scipy.spatial.transform import Rotation


@dataclass
class Parametros:
    caso: int = 8
    lado: int = 8
    altura: float = 18.
    area_lipido: float = 1.6
    dt: float = .003
    preparar: int = 1600
    pasos: int = 2600
    semilla: int = 2026
    velocidad: float = .7
    resorte_guia: float = 40.
    numero_np: int = 2
    radio_np: float = 1.15


def plantilla(p):
    """Topología H2T5 (08) o H2E2(C5)2 (09); parámetros por artículo."""
    if p.caso == 8:
        # Longitud de reposo y ángulo escogidos para esta reducción: el texto
        # principal no explicita l0 y theta0. K=128, Ktheta=15 sí publicados.
        pos = np.column_stack((np.zeros(7), np.zeros(7), -np.arange(7)*.5))
        tipos = np.array([0, 0, 2, 2, 2, 2, 2])
        b = np.column_stack((np.arange(6), np.arange(1, 7)))
        a = np.column_stack((np.arange(5), np.arange(1, 6), np.arange(2, 7)))
        return pos, tipos, b, a, np.full(5, 15.), np.full(5, np.pi), 128., False
    # Arquitectura factual de la configuración de autores SaIL-Yong/nanotetrahedra.
    # Cabezas H,H; gliceroles E,E; dos colas con cinco C cada una.
    pos = np.array([[0, 0, 0], [0, 0, -.5], [0, 0, -1.],
                    [.5, 0, -1.], [0, 0, -1.5], [0, 0, -2.],
                    [0, 0, -2.5], [0, 0, -3.], [0, 0, -3.5],
                    [.5, 0, -1.5], [.5, 0, -2.], [.5, 0, -2.5],
                    [.5, 0, -3.], [.5, 0, -3.5]])
    tipos = np.array([0, 0, 1, 1]+[2]*10)
    b = np.array([[0, 1], [1, 2], [2, 3], [2, 4], [4, 5], [5, 6], [6, 7], [7, 8],
                  [3, 9], [9, 10], [10, 11], [11, 12], [12, 13]])
    a = np.array([[1, 2, 3], [1, 2, 4], [2, 4, 5], [4, 5, 6], [5, 6, 7], [6, 7, 8],
                  [3, 9, 10], [9, 10, 11], [10, 11, 12], [11, 12, 13]])
    ka = np.array([20, 20, 20, 20, 36, 20, 20, 20, 36, 20.])
    theta = np.array([120, 180, 180, 180, 120, 180, 180, 180, 120, 180])*np.pi/180
    return pos, tipos, b, a, ka, theta, 256., True


def construir(p):
    """Bicapa periódica de dos hojas, con agua a densidad aproximada 3."""
    xyz, typ, b, a, ka, theta, kb, excluir = plantilla(p)
    L = p.lado*np.sqrt(p.area_lipido)
    caja = np.array([L, L, p.altura])
    xs, tipos, bonds, angles, kas, thetas = [], [], [], [], [], []
    tam = len(xyz)
    zhead = 2.6 if p.caso == 8 else 2.75
    rng = np.random.default_rng(p.semilla)
    n = 0
    for signo in (1, -1):
        for i in range(p.lado):
            for j in range(p.lado):
                q = xyz.copy()
                # Azimut aleatorio; las colas conservan su arquitectura.
                ang = rng.uniform(0, 2*np.pi)
                Q = Rotation.from_rotvec([0., 0., ang]).as_matrix()
                q = q@Q.T
                q[:, 2] = signo*(q[:, 2]+zhead)+p.altura/2
                q[:, :2] += [(i+.5)*L/p.lado, (j+.5)*L/p.lado]
                xs.append(q)
                tipos.extend(typ)
                bonds.extend(b+n)
                angles.extend(a+n)
                kas.extend(ka)
                thetas.extend(theta)
                n += tam
    x = np.concatenate(xs) % caja
    nl = len(x)
    sep = 3**(-1/3)
    agua = np.stack(np.meshgrid(*[np.arange(sep/2, l, sep) for l in caja], indexing='ij'), axis=-1).reshape(-1, 3)
    agua = agua[np.abs(agua[:, 2]-p.altura/2) > zhead+.45]
    x = np.r_[x, agua]
    tipos = np.r_[tipos, np.full(len(agua), 3)].astype(int)  # H,E,C,W,P
    v = rng.normal(size=x.shape)
    v -= v.mean(axis=0)
    return (x, v, tipos, np.array(bonds), np.array(angles), np.array(kas),
            np.array(thetas), kb, excluir, caja, nl)


def interacciones(p):
    """Matriz simétrica H,E,C,W,P; P hidrofílico en 08 e hidrofóbico en 09."""
    A = np.full((5, 5), 25.)
    valor = 95. if p.caso == 8 else 100.
    A[2, [0, 3]] = valor
    A[[0, 3], 2] = valor
    if p.caso == 8:
        A[4, 2] = A[2, 4] = 95.
    else:
        A[4, [0, 3]] = 100.
        A[[0, 3], 4] = 100.
        A[1, [2, 4]] = 35.
        A[[2, 4], 1] = 35.
    return A


def angulos_fuerzas(x, triples, ka, theta0, caja):
    """-grad de 1/2 K(theta-theta0)^2; conserva fuerza y torque totales."""
    i, j, k = triples.T
    u, v = x[i]-x[j], x[k]-x[j]
    u -= caja*np.rint(u/caja)
    v -= caja*np.rint(v/caja)
    ru, rv = np.linalg.norm(u, axis=1), np.linalg.norm(v, axis=1)
    eu, ev = u/ru[:, None], v/rv[:, None]
    c = np.clip(np.einsum('ij,ij->i', eu, ev), -1+1e-12, 1-1e-12)
    t = np.arccos(c)
    escala = ka*(t-theta0)/np.sqrt(1-c*c)
    fi = escala[:, None]*(ev-c[:, None]*eu)/ru[:, None]
    fk = escala[:, None]*(eu-c[:, None]*ev)/rv[:, None]
    f = np.zeros_like(x)
    np.add.at(f, i, fi)
    np.add.at(f, k, fk)
    np.add.at(f, j, -fi-fk)
    return f, float(.5*np.dot(ka, (t-theta0)**2))


def fuerzas(x, v, tipos, bonds, angles, ka, theta0, kb, excluir, caja, grupos, p, rng, ruido=True):
    """DPD con exclusiones enlazadas; resortes y ángulos de cada lípido."""
    n = len(x)
    pares = cKDTree(x % caja, boxsize=caja).query_pairs(1., output_type='ndarray')
    i, j = pares.T
    valido = ~((grupos[i] >= 0) & (grupos[i] == grupos[j]))
    if excluir:
        cod = bonds[:, 0]*n+bonds[:, 1]
        valido &= ~np.isin(i*n+j, cod)
    i, j = i[valido], j[valido]
    d = x[j]-x[i]
    d -= caja*np.rint(d/caja)
    r = np.linalg.norm(d, axis=1)
    e = d/np.maximum(r[:, None], 1e-12)
    w = np.maximum(1-r, 0.)
    a = interacciones(p)[tipos[i], tipos[j]]
    rel = np.einsum('ij,ij->i', v[j]-v[i], e)
    fn = -a*w+4.5*w*w*rel
    if ruido:
        fn += 3*w*rng.normal(size=len(i))/np.sqrt(p.dt)
    f = np.zeros_like(x)
    np.add.at(f, i, fn[:, None]*e)
    np.add.at(f, j, -fn[:, None]*e)
    U = .5*np.dot(a, w*w)
    i, j = bonds.T
    d = x[j]-x[i]
    d -= caja*np.rint(d/caja)
    r = np.linalg.norm(d, axis=1)
    fb = kb*(r-.5)[:, None]*d/np.maximum(r[:, None], 1e-12)
    np.add.at(f, i, fb)
    np.add.at(f, j, -fb)
    U += .5*kb*np.sum((r-.5)**2)
    fa, ua = angulos_fuerzas(x, angles, ka, theta0, caja)
    return f+fa, float(U+ua)


def geometria_np(p):
    """Esfera en 08; tetraedro FCC de 56 beads y arista 3.08 rc en 09."""
    if p.caso == 8:
        a = np.arange(-p.radio_np, p.radio_np+.01, .45)
        d = np.stack(np.meshgrid(a, a, a, indexing='ij'), axis=-1).reshape(-1, 3)
        d = d[np.linalg.norm(d, axis=1) <= p.radio_np]
    else:
        basis = np.array([[1, 0, 0], [.5, np.sqrt(3)/2, 0], [.5, np.sqrt(3)/6, np.sqrt(2/3)]])*.87/np.sqrt(2)
        d = np.array([np.array([i, j, k])@basis for i in range(6) for j in range(6-i) for k in range(6-i-j)])
        d -= d.mean(axis=0)
        q = d[0]/np.linalg.norm(d[0])
        Q = Rotation.align_vectors(np.array([[0., 0., -1.]]), q[None, :])[0].as_matrix()
        d = d@Q.T
    return d-d.mean(axis=0)


def insertar_np(x, v, tipos, caja, p):
    """Inserta cuerpos; elimina únicamente agua solapada, no lípidos."""
    cuerpo = geometria_np(p)
    z = caja[2]/2+(2.6 if p.caso == 8 else 2.75)-cuerpo[:, 2].min()+1.1
    numero = p.numero_np if p.caso == 8 else 1
    centros = [np.array([caja[0]/2+(i-(numero-1)/2)*2.8, caja[1]/2, z]) for i in range(numero)]
    for c in centros:
        dist, _ = cKDTree((cuerpo+c) % caja, boxsize=caja).query(x % caja)
        keep = ~((tipos == 3) & (dist < .7))
        x, v, tipos = x[keep], v[keep], tipos[keep]
    grupos = np.full(len(x), -1)
    cuerpos = []
    for g, c in enumerate(centros):
        ids = np.arange(len(x), len(x)+len(cuerpo))
        x = np.r_[x, (c+cuerpo) % caja]
        v = np.r_[v, np.zeros_like(cuerpo)]
        tipos = np.r_[tipos, np.full(len(cuerpo), 4)]
        grupos = np.r_[grupos, np.full(len(cuerpo), g)]
        I = sum(np.dot(b, b)*np.eye(3)-np.outer(b, b) for b in cuerpo)
        cuerpos.append(dict(ids=ids, b=cuerpo.copy(), centro=c.copy(), origen=c.copy(),
                             Q=np.eye(3), V=np.zeros(3), momento=np.zeros(3), invI=np.linalg.inv(I)))
    return x, v, tipos, grupos, cuerpos


def paso_rigido(f, body, p, t, caja, detener=False):
    """Suma fuerza/torque, integra COM y rotación preservando la geometría."""
    d = body['b']@body['Q'].T
    ff = f[body['ids']]
    F = ff.sum(axis=0)
    tau = np.cross(d, ff).sum(axis=0)
    if p.caso == 8:
        ancla_z = body['origen'][2]-(0 if detener else p.velocidad)*t
        F[2] -= p.resorte_guia*(body['centro'][2]-ancla_z)
    if detener:
        return (body['centro']+d) % caja, np.zeros_like(d)
    body['V'] += p.dt*F/len(d)
    if p.caso == 9:
        body['V'][:2] = 0.  # Restricción lateral publicada para tiempo corto.
    body['momento'] += p.dt*tau
    omega = body['Q']@body['invI']@body['Q'].T@body['momento']
    body['Q'] = Rotation.from_rotvec(p.dt*omega).as_matrix()@body['Q']
    body['centro'] += p.dt*body['V']
    d = body['b']@body['Q'].T
    omega = body['Q']@body['invI']@body['Q'].T@body['momento']
    return (body['centro']+d) % caja, body['V']+np.cross(omega, d)


def altura_membrana(x, nl, p, caja):
    """Mapa local de cabezas; medias por celda reducen ruido de beads."""
    nlip = 7 if p.caso == 8 else 14
    cabezas = np.arange(0, nl, nlip)  # Primera H por lípido, ambas hojas.
    ids = cabezas[:len(cabezas)//2]  # La hoja inicialmente superior.
    xx = x[ids].copy()
    xx[:, 2] = caja[2]/2+(xx[:, 2]-caja[2]/2+caja[2]/2) % caja[2]-caja[2]/2
    n = 8
    ij = np.minimum((xx[:, :2]/caja[:2]*n).astype(int), n-1)
    S, C = np.zeros((n, n)), np.zeros((n, n))
    np.add.at(S, (ij[:, 0], ij[:, 1]), xx[:, 2])
    np.add.at(C, (ij[:, 0], ij[:, 1]), 1)
    mapa = np.divide(S, C, out=np.full_like(S, np.nan), where=C > 0)
    return mapa


def simular(p, salida, animar=False):
    """Preparación; contacto y control con NPs fijas desde un estado común."""
    import copy
    x, v, tipos, bonds, angles, ka, theta, kb, excluir, caja, nl = construir(p)
    rng = np.random.default_rng(p.semilla+1)
    grupos = np.full(len(x), -1)
    for i in range(p.preparar):
        f, _ = fuerzas(x, v, tipos, bonds, angles, ka, theta, kb, excluir, caja, grupos, p, rng)
        v += p.dt*f
        x = (x+p.dt*v) % caja
    x, v, tipos, grupos, cuerpos = insertar_np(x, v, tipos, caja, p)
    datos, estados, cnps = [], [], []
    final_n = len(x)
    for control in (False, True):
        xx, vv, bs = x.copy(), v.copy(), copy.deepcopy(cuerpos)
        rng = np.random.default_rng(p.semilla+2)
        if p.caso == 9 and not control:
            bs[0]['V'][2] = -p.velocidad
            vv[bs[0]['ids'], 2] = -p.velocidad
        serie, frames, centers = [], [], []
        for i in range(p.pasos+1):
            if i % max(1, p.pasos//100) == 0 or i == p.pasos:
                mapa = altura_membrana(xx, nl, p, caja)
                # Heterogeneidad de la superficie: quita desplazamiento medio.
                rug = float(np.nanstd(mapa))
                cc = np.array([b['centro'] for b in bs])
                serie.append([i*p.dt, rug, cc[0, 2], np.linalg.norm(cc[-1]-cc[0]) if len(cc)>1 else 0.])
                frames.append(xx[:nl].astype(np.float32).copy())
                centers.append(np.concatenate([xx[b['ids']] for b in bs]))
            if i == p.pasos:
                break
            f, U = fuerzas(xx, vv, tipos, bonds, angles, ka, theta, kb, excluir, caja, grupos, p, rng)
            libre = grupos < 0
            vv[libre] += p.dt*f[libre]
            xx[libre] = (xx[libre]+p.dt*vv[libre]) % caja
            for body in bs:
                pos, vel = paso_rigido(f, body, p, i*p.dt, caja, detener=control)
                xx[body['ids']], vv[body['ids']] = pos, vel
            if not np.isfinite(xx).all() or np.max(np.abs(vv)) > 150:
                raise ValueError('Inestabilidad: bajar dt o mejorar preparación')
        datos.append(np.array(serie))
        estados.append(np.array(frames))
        cnps.append(np.array(centers))
    salida = Path(salida)
    salida.mkdir(parents=True, exist_ok=True)
    tabla = np.c_[datos[0], datos[1][:, 1:]]
    np.savetxt(salida/'metricas.csv', tabla, delimiter=',', comments='',
               header='t,rugosidad_contacto,z_np_contacto,separacion_np_contacto,rugosidad_control,z_np_control,separacion_np_control')
    np.savez_compressed(salida/'estados.npz', contacto=estados[0], control=estados[1],
                        np_contacto=cnps[0], np_control=cnps[1], tipos=tipos[:nl], caja=caja)
    (salida/'parametros.json').write_text(json.dumps(asdict(p), indent=2), encoding='utf-8')
    resumen = dict(beads_totales=final_n, lipidos=nl//(7 if p.caso == 8 else 14),
                   beads_np_por_cuerpo=len(cuerpos[0]['ids']), rugosidad_final_contacto=float(tabla[-1, 1]),
                   rugosidad_final_control=float(tabla[-1, 4]), z_np_final=float(tabla[-1, 2]),
                   alcance='DPD reducido; no certifica fases, poros ni equilibrio de los artículos')
    (salida/'resumen.json').write_text(json.dumps(resumen, indent=2), encoding='utf-8')
    dibujar(estados, cnps, tipos[:nl], datos, caja, p, salida, animar)
    return resumen


def dibujar(estados, cnps, tipos, datos, caja, p, salida, animar):
    """Corte de la bicapa y curva de rugosidad, todos desde estados integrados."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation, PillowWriter
    fig, ax = plt.subplots(1, 3, figsize=(13, 4.5), layout='constrained')
    colors = np.array(['#2372af', '#42b79f', '#df913b', '#aaaaaa'])
    def cuadro(i):
        for k in range(2):
            ax[k].clear()
            q = estados[k][i]
            mask = np.abs(q[:, 1]-caja[1]/2) < 1.3
            ax[k].scatter(q[mask, 0], q[mask, 2], s=9, c=colors[tipos[mask]])
            nn = cnps[k][i]
            ax[k].scatter(nn[:, 0], nn[:, 2], c='#3f3f3f', s=9)
            ax[k].set(xlim=(0, caja[0]), ylim=(caja[2]/2-5, caja[2]/2+8), xlabel='x/rc', ylabel='z/rc',
                      title=('Contacto mecánico' if k==0 else 'Control: NP fija')+f'\nt={datos[k][i,0]:.2f} DPD')
            ax[k].set_aspect('equal')
        return []
    for d, nombre in zip(datos, ['Contacto', 'Control']):
        ax[2].plot(d[:, 0], d[:, 1], label=nombre)
    ax[2].set(xlabel='Tiempo DPD', ylabel='Desviación de altura de cabezas / rc', title='Deformación y fluctuación de la hoja')
    ax[2].legend()
    cuadro(len(estados[0])-1)
    fig.savefig(salida/'simulacion.png', dpi=140)
    if animar:
        FuncAnimation(fig, cuadro, frames=len(estados[0]), interval=60).save(salida/'simulacion.gif', writer=PillowWriter(fps=15))
    plt.close(fig)
