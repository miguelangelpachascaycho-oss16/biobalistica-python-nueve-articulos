# Piloto: nanoesferas contra una bicapa lipídica

**Reducción didáctica 3D, no réplica completa ni modelo calibrado de células reales.** Fuente: Campello (2015), [DOI 10.1007/s40430-014-0273-5](https://doi.org/10.1007/s40430-014-0273-5), exclusivamente el ejemplo biológico 5.3. Se usa el marco de dinámica de partículas de sus secciones 2–4. Véase la [copia pública aportada por el autor](https://www.researchgate.net/publication/269096734_Computational_modeling_and_simulation_of_rupture_of_membranes_and_thin_films).

## Qué representa

Dos capas de nodos con masa, enlazadas dentro de cada capa y entre capas, reciben un pequeño chorro de nanoesferas. Las fuerzas alteran posiciones y velocidades de los nodos. El dibujo conecta esas posiciones calculadas: la superficie no recibe una forma predeterminada. La esfera individual conserva su radio, mientras la bicapa cambia de forma.

## Trazabilidad y diferencias

La geometría de bicapa (39 × 39 nm, separación 5 nm), radios de nodos (1.25 nm) y proyectiles (0.625 nm), constantes de enlaces, densidades y fuerzas provienen del ejemplo 5.3. Están visibles en `Parametros`. Se adoptan **14 × 14 nodos por capa**, una disposición didáctica que debe cotejarse con la discretización del autor.

El chorro contiene **9 proyectiles en una disposición nueva**; el ejemplo publicado tiene 200. La separación inicial y la duración de 1 ns también son elecciones didácticas. Se usa RK2 explícito y `dt=0.00002 ns`, frente a la familia trapezoidal descrita por el autor. Se recorta la fuerza normal a cero para evitar tracción artificial al separarse: es una modificación unilateral declarada. Estas diferencias impiden comparar directamente una tasa de penetración con las figuras del artículo.

Las propiedades son ilustrativas. No se presentan como mediciones biológicas. La presión se aplica desde la configuración inicial sin una relajación previa; por eso debe ejecutarse un control sin proyectiles. Las normales de presión se calculan aquí con tangentes de la cuadrícula. Después de una ruptura extensa, esa aproximación necesita revisión.

## Ecuaciones que implementa el código

Para cada nodo: `m_i * dv_i/dt = suma de fuerzas` y `dx_i/dt = v_i`.

Para un enlace, con `n=(x_j-x_i)/L`, la fuerza sobre i es:

```text
F_ij = [k (L-L0) + c ((v_j-v_i)·n)] n
F_ji = -F_ij
```

El enlace se desactiva irreversiblemente cuando `(L-L0)/L0 >= epsilon_critica`. El arrastre es `-c_env*v`. La presión inferior tiene magnitud constante por nodo y dirección normal a la configuración actual.

En contacto se utiliza solapamiento **positivo** `h=Ri+Rj-L`, con h>0. Definiendo `R*=RiRj/(Ri+Rj)`, `m*=mimj/(mi+mj)` y `E*=E/[2(1-nu²)]`:

```text
d = 2 xi sqrt(2 sqrt(R*) E* m*) h^(1/4)
N = max(0, (4/3) sqrt(R*) E* h^(3/2) - d ((v_j-v_i)·n))
F_normal_sobre_i = -N n
```

La fricción deslizante se opone a la velocidad tangencial relativa. La fuerza de cada par se suma con signos opuestos. Se usa `cKDTree` solo para encontrar vecinos; no determina la física.

Unidades internas: nm, ns, fg y nN. Así, `1 fg·nm/ns² = 1 nN`; una rapidez de `100 nm/ns` equivale a `100 m/s`. No se mezclan densidades SI con posiciones en nanómetros.

## Ejecutar paso a paso

1. Descarga el repositorio, extráelo y abre su carpeta en VS Code.
2. En una terminal PowerShell crea un entorno e instala dependencias:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

3. Elige `.venv` con **Python: Select Interpreter** y lee `Parametros` antes de ejecutar:

   ```powershell
   .\.venv\Scripts\python.exe src/piloto_membrana.py --animar
   ```

4. Abre `resultados/piloto_membrana/piloto_membrana.gif` y el CSV de métricas. `estados.npz` conserva las posiciones y enlaces activos de cada cuadro.
5. Ejecuta el control en otra carpeta y compara desplazamientos. No lo ejecutes simultáneamente si tu equipo tiene pocos recursos:

   ```powershell
   .\.venv\Scripts\python.exe src/piloto_membrana.py --sin-proyectiles --animar --salida resultados/control
   .\.venv\Scripts\python.exe pruebas/verificar_piloto.py
   ```

6. Conserva parámetros y resultados. Un desplazamiento nodal máximo no es una deformación unitaria; calcula la elongación de cada enlace respecto de `L0` para analizar esta última. La altura media de proyectiles no demuestra penetración de todos ellos.

## Estructura y funciones

| Función o clase | Recibe | Produce y responsabilidad |
|---|---|---|
| `Parametros` | Valores físicos y opciones | Configuración explícita con unidades |
| `crear_sistema` | Parámetros | Posiciones, velocidades, masas, radios, enlaces, longitudes iniciales y bordes |
| `fuerzas_enlaces` | Estado y enlaces activos | Fuerzas axiales en pares iguales y opuestos |
| `romper_enlaces` | Posiciones y longitudes iniciales | Máscara de enlaces que siguen activos; sin reparación automática |
| `fuerzas_contacto` | Estado, radios y masas | Repulsión, amortiguamiento y fricción de contactos |
| `fuerzas_presion` | Geometría actual | Fuerzas seguidoras de la capa inferior |
| `integrar` | Parámetros | Trayectoria de todos los nodos mediante RK2; impone bordes fijos |
| `guardar_resultados` | Trayectoria y carpeta | NPZ, CSV y JSON reproducibles |
| `animar` | Estados guardados | GIF y PNG; no modifica la solución |
| `main` | Opciones de terminal | Conecta configuración, simulación y exportación |

Dentro de `integrar`, `aceleracion` reúne fuerzas y divide por masas. Dentro de `animar`, `actualizar` selecciona un estado ya calculado para dibujarlo. En `pruebas/verificar_piloto.py`, `oscilador` es una referencia independiente y `main` ejecuta las comprobaciones.

## Aprender una solución analítica

La simulación acoplada completa no tiene aquí una solución cerrada. Se aprende a derivar y verificar un **límite aislado**: un nodo con masa m, conectado axialmente a un extremo fijo mediante k y c, sin contacto, arrastre externo, presión ni ruptura. Para `q(0)=q0` y `q'(0)=0`:

```text
m q'' + c q' + k q = 0
gamma = c/(2m)
omega_d = sqrt(k/m - gamma²)             [caso subamortiguado]
q(t) = q0 exp(-gamma t) [cos(omega_d t) + gamma/omega_d sin(omega_d t)]
```

Esta deducción es un ejercicio del enlace, no una fórmula publicada para toda la bicapa. Deriva primero la ecuación característica, calcula las constantes iniciales y compara RK2 con la expresión cerrada. Luego reduce `dt` a la mitad y explica el cambio de error. No se debe aplicar esta fórmula al impacto completo.

## Comprobaciones y límites

`pruebas/verificar_piloto.py` comprueba acción y reacción, contacto repulsivo sin fuerza a distancia, convergencia del oscilador y convergencia temporal del impacto hasta 0.16 ns. También mide el control sin proyectiles. Los resultados quedan en `pruebas/evidencia/VERIFICACION_PILOTO.json`.

La convergencia temporal no es convergencia espacial. Aún faltan comparación con datos del autor, revisión del tamaño de malla, auditoría de energía con presión y disipación, y validación de ruptura. La animación de 1 ns no demuestra la respuesta publicada a 5 ns. No se ha calibrado ni validado este piloto con experimentos.

## Uso de Copilot y defensa del código

Trabaja en este orden: unidades → un enlace → dos esferas → bicapa sin proyectiles → impacto → dibujo. Pide a Copilot que explique una función a la vez y comprueba su respuesta con las ecuaciones.

Prompts útiles:

- «Deriva la solución subamortiguada con las condiciones iniciales indicadas. No inventes datos del artículo».
- «Explica las dimensiones de los arrays en `fuerzas_enlaces` y por qué se usa `np.add.at`».
- «Comprueba el signo de amortiguamiento durante aproximación y separación de dos esferas».
- «Señala qué diferencias impiden llamar a este piloto reproducción completa del artículo».

Para la defensa, el alumno debe explicar el flujo completo sin ejecutar Copilot; justificar unidades y signos; distinguir desplazamiento de deformación; comparar con el control; mostrar un error numérico; e indicar qué falta validar. No basta con describir el GIF.
