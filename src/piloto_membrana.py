"""Piloto 3D, reducción del ejemplo 5.3 de Campello (2015).

DOI 10.1007/s40430-014-0273-5. No es la reproducción completa del artículo.
Unidades internas: nm, ns, fg, nN. Ver PILOTO_MEMBRANA.md.
Las superficies dibujadas usan posiciones integradas, nunca un perfil impuesto.
"""
from dataclasses import dataclass, asdict
from pathlib import Path
import argparse
import json
import numpy as np
from scipy.spatial import cKDTree


@dataclass
class Parametros:
    lado: float = 39.0
    nodos: int = 14
    espesor: float = 5.0
    radio_lipido: float = 1.25
    radio_proyectil: float = 0.625
    densidad_lipido: float = 9e-7
    densidad_proyectil: float = 1.8e-6
    k: float = 4e-3
    c: float = 1e-5
    deformacion_critica: float = 0.5
    E: float = 100.0
    nu: float = 0.25
    xi: float = 0.1
    friccion: float = 0.1
    arrastre: float = 5e-6
    presion_por_nodo: float = 6.5e-6
    velocidad: float = 100.0
    dt: float = 2e-5
    tiempo_final: float = 1.0
    con_proyectiles: bool = True


def crear_sistema(p):
    """Crea dos capas, enlaces vecinos y bordes fijos; añade un chorro de 9 esferas."""
    n = p.nodos
    eje = np.linspace(-p.lado / 2, p.lado / 2, n)
    xx, yy = np.meshgrid(eje, eje, indexing="ij")
    capas = [np.column_stack((xx.ravel(), yy.ravel(), np.full(n*n, z)))
             for z in (0.0, p.espesor)]
    x = np.concatenate(capas)
    enlaces = []
    for capa in range(2):
        for i in range(n):
            for j in range(n):
                a = capa*n*n + i*n+j
                if i+1 < n:
                    enlaces.append((a, a+n))
                if j+1 < n:
                    enlaces.append((a, a+1))
                if capa == 0:
                    enlaces.append((a, a+n*n))
    enlaces = np.asarray(enlaces, dtype=int)
    fijos = np.tile(((xx == eje[0]) | (xx == eje[-1]) |
                     (yy == eje[0]) | (yy == eje[-1])).ravel(), 2)
    nm = len(x)
    if p.con_proyectiles:
        px, py = np.meshgrid([-1.5, 0, 1.5], [-1.5, 0, 1.5])
        chorro = np.column_stack((px.ravel()+0.3, py.ravel()+0.3,
                                 np.full(9, p.espesor+7)))
        x = np.concatenate((x, chorro))
        fijos = np.r_[fijos, np.zeros(9, dtype=bool)]
    radios = np.r_[np.full(nm, p.radio_lipido),
                   np.full(len(x)-nm, p.radio_proyectil)]
    rho = np.r_[np.full(nm, p.densidad_lipido),
                np.full(len(x)-nm, p.densidad_proyectil)]
    masas = 4*np.pi*radios**3*rho/3
    v = np.zeros_like(x)
    v[nm:, 2] = -p.velocidad
    l0 = np.linalg.norm(x[enlaces[:, 1]]-x[enlaces[:, 0]], axis=1)
    return x, v, radios, masas, enlaces, l0, fijos, nm


def fuerzas_enlaces(x, v, enlaces, l0, activos, p):
    """Ley axial resorte-amortiguador (ec.18); pares iguales y opuestos."""
    a, b = enlaces.T
    d = x[b]-x[a]
    longitud = np.linalg.norm(d, axis=1)
    normal = d/np.maximum(longitud[:, None], 1e-15)
    tasa = np.sum((v[b]-v[a])*normal, axis=1)
    escalar = (p.k*(longitud-l0)+p.c*tasa)*activos
    f = np.zeros_like(x)
    np.add.at(f, a, escalar[:, None]*normal)
    np.add.at(f, b, -escalar[:, None]*normal)
    return f


def romper_enlaces(x, enlaces, l0, activos, p):
    """Desactiva irreversiblemente enlaces cuya deformación axial alcanza el umbral."""
    a, b = enlaces.T
    deformacion = np.linalg.norm(x[b]-x[a], axis=1)/l0-1
    return activos & (deformacion < p.deformacion_critica)


def fuerzas_contacto(x, v, radios, masas, p):
    """Contactos Hertz, amortiguamiento (ec.32) y fricción deslizante.

    Se usa solapamiento positivo h=Ri+Rj-distancia, normal de i a j.
    La fuerza normal sobre i es -N*n. Se recorta N>=0 para evitar adhesión.
    """
    f = np.zeros_like(x)
    pares = cKDTree(x).query_pairs(2*radios.max(), output_type="ndarray")
    if len(pares) == 0:
        return f
    a, b = pares.T
    d = x[b]-x[a]
    longitud = np.linalg.norm(d, axis=1)
    h = radios[a]+radios[b]-longitud
    sel = h > 0
    a, b, d, longitud, h = a[sel], b[sel], d[sel], longitud[sel], h[sel]
    normal = d/np.maximum(longitud[:, None], 1e-15)
    relativa = v[b]-v[a]
    vn = np.sum(relativa*normal, axis=1)
    re = radios[a]*radios[b]/(radios[a]+radios[b])
    me = masas[a]*masas[b]/(masas[a]+masas[b])
    ee = p.E/(2*(1-p.nu**2))
    amort = 2*p.xi*np.sqrt(2*np.sqrt(re)*ee*me)*h**0.25
    N = np.maximum(0.0, 4/3*np.sqrt(re)*ee*h**1.5-amort*vn)
    tangente = relativa-vn[:, None]*normal
    rapidez_t = np.linalg.norm(tangente, axis=1)
    direccion_t = tangente/np.maximum(rapidez_t[:, None], 1e-15)
    fi = -N[:, None]*normal+p.friccion*N[:, None]*direccion_t
    np.add.at(f, a, fi)
    np.add.at(f, b, -fi)
    return f


def fuerzas_presion(x, p):
    """Presión seguidora: normales actuales de la capa inferior, calculadas en 3D."""
    n = p.nodos
    capa = x[:n*n].reshape(n, n, 3)
    tangente_x = np.gradient(capa, axis=0)
    tangente_y = np.gradient(capa, axis=1)
    normal = np.cross(tangente_x, tangente_y)
    normal /= np.maximum(np.linalg.norm(normal, axis=2)[..., None], 1e-15)
    f = np.zeros_like(x)
    f[:n*n] = p.presion_por_nodo*normal.reshape(-1, 3)
    return f


def integrar(p):
    """Avanza posiciones y velocidades con punto medio explícito (RK2).

    El artículo permite una familia trapezoidal; RK2 es una adaptación didáctica.
    La ruptura se decide al comienzo y al final de cada paso aceptado.
    """
    x, v, radios, masas, enlaces, l0, fijos, nm = crear_sistema(p)
    x0 = x.copy()
    activos = np.ones(len(enlaces), dtype=bool)
    pasos = int(np.ceil(p.tiempo_final/p.dt))
    dt = p.tiempo_final/pasos
    guardar = set(np.linspace(0, pasos, 121).astype(int))
    tiempos, posiciones, metricas, historia_enlaces = [], [], [], []

    def aceleracion(pos, vel):
        f = (fuerzas_enlaces(pos, vel, enlaces, l0, activos, p)
             + fuerzas_contacto(pos, vel, radios, masas, p)
             + fuerzas_presion(pos, p)-p.arrastre*vel)
        a = f/masas[:, None]
        a[fijos] = 0
        return a

    for paso in range(pasos+1):
        if paso in guardar:
            tiempos.append(paso*dt)
            posiciones.append(x.copy())
            historia_enlaces.append(activos.copy())
            u = np.linalg.norm(x[:nm]-x0[:nm], axis=1).max()
            zjet = float(x[nm:, 2].mean()) if len(x) > nm else np.nan
            metricas.append((paso*dt, u, zjet, int((~activos).sum())))
        if paso == pasos:
            break
        activos = romper_enlaces(x, enlaces, l0, activos, p)
        a0 = aceleracion(x, v)
        xm = x+dt*v/2
        vm = v+dt*a0/2
        a1 = aceleracion(xm, vm)
        x += dt*vm
        v += dt*a1
        x[fijos], v[fijos] = x0[fijos], 0
        activos = romper_enlaces(x, enlaces, l0, activos, p)
        if paso % 5000 == 0 and not (np.isfinite(x).all() and np.isfinite(v).all()):
            raise FloatingPointError("Paso inestable: reducir dt y revisar unidades")
    return dict(t=np.asarray(tiempos), x=np.asarray(posiciones),
                activos=np.asarray(historia_enlaces), enlaces=enlaces,
                radios=radios, nm=nm, metricas=np.asarray(metricas))


def guardar_resultados(datos, p, carpeta):
    """Exporta estados reutilizables, métricas y parámetros, sin ocultar la procedencia."""
    carpeta.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(carpeta/"estados.npz", **datos)
    np.savetxt(carpeta/"metricas.csv", datos["metricas"], delimiter=",",
               header="t_ns,u_max_nm,z_medio_proyectiles_nm,enlaces_rotos", comments="")
    (carpeta/"parametros.json").write_text(json.dumps(asdict(p), indent=2), encoding="utf-8")


def animar(datos, p, archivo):
    """Dibuja dos vistas de los estados calculados; colores indican desplazamiento."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation, PillowWriter
    from mpl_toolkits.mplot3d.art3d import Line3DCollection
    from matplotlib.collections import LineCollection, PatchCollection
    from matplotlib.patches import Circle
    fig = plt.figure(figsize=(11, 5), layout="constrained")
    ax = fig.add_subplot(121, projection="3d")
    lado = fig.add_subplot(122)
    nm = datos["nm"]
    x0 = datos["x"][0]
    edges = datos["enlaces"]
    nube = ax.scatter(*x0[:nm].T, s=6, c=np.zeros(nm), cmap="viridis", vmin=0, vmax=3)
    balas = ax.scatter(*x0[nm:].T, s=24, color="#d77c00", label="Nanoesferas")
    lineas = Line3DCollection(x0[edges], colors="#7191ae", linewidths=.35, alpha=.6)
    ax.add_collection3d(lineas)
    perfil = LineCollection([], colors="#7191ae", linewidths=.5)
    lado.add_collection(perfil)
    puntos = lado.scatter(x0[:nm, 0], x0[:nm, 2], s=7, c=np.zeros(nm),
                          cmap="viridis", vmin=0, vmax=3)
    jet2 = PatchCollection([Circle((q[0], q[2]), p.radio_proyectil)
                           for q in x0[nm:]], facecolor="#d77c00", edgecolor="#915200")
    lado.add_collection(jet2)
    zmin = min(-5, float(datos["x"][:, :, 2].min())-1)
    zmax = max(14, float(datos["x"][:, :, 2].max())+1)
    ax.set(xlim=(-21, 21), ylim=(-21, 21), zlim=(zmin, zmax),
           xlabel="x (nm)", ylabel="y (nm)", zlabel="z (nm)")
    ax.view_init(elev=24, azim=-65)
    lado.set(xlim=(-21, 21), ylim=(-5, 14), xlabel="x (nm)", ylabel="z (nm)",
             title="Proyección lateral; nodos de ambas capas")
    lado.set_aspect("equal")
    nota = lado.text(.02, .02, "", transform=lado.transAxes, fontsize=8)
    fig.colorbar(nube, ax=ax, shrink=.5, label="Desplazamiento del blanco (nm)")
    titulo = fig.suptitle("")

    def actualizar(i):
        x = datos["x"][i]
        u = np.linalg.norm(x[:nm]-x0[:nm], axis=1)
        nube._offsets3d = tuple(x[:nm].T)
        nube.set_array(u)
        balas._offsets3d = tuple(x[nm:].T)
        segmentos = x[edges[datos["activos"][i]]]
        lineas.set_segments(segmentos)
        perfil.set_segments(segmentos[:, :, [0, 2]])
        puntos.set_offsets(x[:nm][:, [0, 2]])
        puntos.set_array(u)
        jet2.set_paths([Circle((q[0], q[2]), p.radio_proyectil) for q in x[nm:]])
        fuera = int(((x[nm:, 2] < -5) | (x[nm:, 2] > 14) |
                     (np.abs(x[nm:, 0]) > 21)).sum())
        nota.set_text(f"Zoom del blanco; esferas fuera del zoom: {fuera}\n"
                      "Radios reales en 2D; centros esquemáticos en 3D")
        titulo.set_text(f"Piloto reducido de Campello 2015 — t={datos['t'][i]:.3f} ns\n"
                        "Bicapa 3D + 9 nanoesferas; deformación integrada, sin validación experimental")
        return nube, balas, puntos, jet2, titulo

    indices = np.unique(np.linspace(0, len(datos["t"])-1, 80).astype(int))
    pelicula = FuncAnimation(fig, actualizar, frames=indices, interval=65, blit=False)
    pelicula.save(archivo, writer=PillowWriter(fps=15))
    actualizar(int(np.argmax(datos["metricas"][:, 1])))
    fig.savefig(Path(archivo).with_suffix(".png"), dpi=130)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dt", type=float, default=2e-5)
    parser.add_argument("--tiempo", type=float, default=1.0)
    parser.add_argument("--sin-proyectiles", action="store_true")
    parser.add_argument("--animar", action="store_true")
    parser.add_argument("--salida", type=Path, default=Path("resultados/piloto_membrana"))
    args = parser.parse_args()
    if not (0 < args.dt <= 2e-4 and 0 < args.tiempo <= 5):
        parser.error("Usa 0<dt<=0.0002 ns y 0<tiempo<=5 ns")
    p = Parametros(dt=args.dt, tiempo_final=args.tiempo,
                   con_proyectiles=not args.sin_proyectiles)
    datos = integrar(p)
    guardar_resultados(datos, p, args.salida)
    if args.animar:
        animar(datos, p, args.salida/"piloto_membrana.gif")
    print(json.dumps({"salida": str(args.salida),
                      "u_max_nm": float(datos["metricas"][:, 1].max()),
                      "enlaces_rotos_final": int(datos["metricas"][-1, 3])}))


if __name__ == "__main__":
    main()
