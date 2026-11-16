# Colisión de una nanopartícula con una vesícula: piloto DPD

Artículo distinto: N. Arai, K. Yasuoka y X. C. Zeng (2013), *A vesicle cell under collision with a Janus or homogeneous nanoparticle: translocation dynamics and late-stage morphology*, Nanoscale 5, 9089–9100, [DOI 10.1039/C3NR02024J](https://doi.org/10.1039/C3NR02024J). [Texto completo editorial y licencia CC BY 3.0](https://pubs.rsc.org/nr/article/5/19/9089/407469/A-vesicle-cell-under-collision-with-a-Janus-or). [Copia institucional UNL](https://digitalcommons.unl.edu/chemzeng/117/).

El artículo estudia colisiones nanométricas con una vesícula lipídica idealizada; no utiliza una pistola génica ni células completas con orgánulos. Este programa es un **piloto mecánico reducido**, con decisiones complementarias explícitas. Se asigna como actividad exploratoria reducida; no reproduce las fases de penetración del artículo. El control y las comprobaciones forman parte del ejercicio.

## Ejecutar en Visual Studio Code

1. Descarga el repositorio con **Code → Download ZIP**, extráelo y abre esa carpeta en VS Code.
2. Instala Python y la extensión Python de Microsoft. Abre **Terminal → New Terminal**.
3. Ejecuta desde la raíz del repositorio, usando directamente el intérprete del entorno:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe pruebas/verificar_vesicula.py
.\.venv\Scripts\python.exe src/vesicula_dpd.py --animar
```

4. Abre `resultados/vesicula/vesicula_dpd.gif` y `casos/05_gerwins_branco_diaz_delgado/figura.png`. Los dos paneles de posiciones comparan impacto y control sin velocidad inicial. El agua está en el cálculo aunque no se dibuje.
5. Abre `casos/05_gerwins_branco_diaz_delgado/ejemplo/metricas.csv` para analizar desplazamiento RMS alineado sin traslación ni rotación rígida, asfericidad, energía cinética y posición de la nanopartícula. `VESICULA_ESTADOS.npz` conserva las posiciones calculadas. `casos/05_gerwins_branco_diaz_delgado/ejemplo/parametros.json` registra los parámetros ejecutados.
6. Presenta primero el control y explica sus cambios antes de atribuir cambios al impacto. Una vesícula que se desarma espontáneamente no permite interpretar un resultado como perforación causada por el proyectil.

Las longitudes están en radios de corte `rc`, las masas en masa de bead y las energías en `kBT`. **No hay conversión validada a nanómetros, metros por segundo o segundos**. El programa predeterminado usa un hilo y aproximadamente diez mil beads; el tiempo depende del equipo. No ejecuta LAMMPS ni necesita GPU.

## Del artículo al programa

El blanco está formado por cadenas **HTTT**: una cabeza hidrofílica H y tres beads de cola hidrofóbica T. Los beads W representan agua y los B una nanopartícula homogénea hidrofílica. La deformación emerge al integrar las posiciones, sin asignar una forma geométrica a la membrana después del impacto.

Las ecuaciones 1–7 del artículo contienen Newton, repulsión blanda, disipación, ruido térmico y resortes. En unidades reducidas `rc=m=kBT=1`, define `d=xj−xi`, `n=d/r`, `w=max(1−r,0)`:

```text
F_C sobre i = −a_ij w n
F_D sobre i = +gamma w² ((vj−vi)·n) n
F_R sobre i = sigma w xi_ij / sqrt(dt) n
F_S sobre i = C (r/rs−1) n
F sobre j   = −F sobre i
gamma = 4.5; sigma = 3; sigma² = 2 gamma kBT
```

`xi_ij` es normal estándar, independiente para cada par y paso. Las fuerzas aleatorias son opuestas dentro de un par, por lo que no agregan momento lineal neto al sistema.

**Correcciones y decisiones que deben explicarse:**

- Con `d=xj−xi` y `vj−vi`, el signo de disipación impreso en la ecuación 3 sería antidisipativo. Se utiliza el signo que hace que la potencia por par sea `−gamma w² ((vj−vi)·n)² ≤ 0`. No se oculta esta diferencia con el texto.
- La ecuación 7 usa C como amplitud de fuerza, aunque el texto da unidades de rigidez. Aquí C=100 es una amplitud de fuerza reducida; la rigidez del enlace es **C/rs**, no C.
- El artículo enumera a_HH=a_TT=a_WW=a_BW=a_HW=25 y a_BT=a_TW=80. No enumera a_HT ni a_BH: se adoptan 80 y 25 por identidad hidrofóbica/hidrofílica. Son decisiones docentes, no valores comprobados en la publicación.
- Se usa `rs=0.86 rc` como decisión de escala. El artículo da `rs=1.075 nm`, pero no proporciona aquí una conversión inequívoca de rc que permita trasladar toda su calibración física al piloto.
- Se reducen caja, cantidad de lípidos y tamaño de nanopartícula. Se construyen hojas con direcciones de Fibonacci y una NP de malla cúbica, frente a la red diamante y 2149 beads del artículo. No se conserva el tamaño físico ni la relación entre todos los tamaños publicados.
- Se integra con kick-drift explícito; no se implementan el esquema de Lowe ni RATTLE publicados. La NP solo traslada, no rota. Se estudia una NP homogénea y no las orientaciones Janus. No se rompen enlaces ni se calcula el área de poro del artículo.

Por estas diferencias, las cifras del piloto **no deben compararse directamente con los umbrales de velocidad, tamaño de poro o tiempos de Arai et al.**

## Estructura y funciones

| Función | Entrada | Qué calcula y entrega |
|---|---|---|
| `Parametros` | Valores del experimento numérico | Caja, geometría, termostato, paso y semilla; distingue parámetros publicados de elecciones docentes con esta guía |
| `esfera_fibonacci(n)` | Número de cadenas | Direcciones para distribuir cabezas en hojas esféricas; no crea una red elástica entre lípidos |
| `construir(p)` | Parámetros | Beads HTTT, agua, velocidades térmicas, tipos y enlaces de cada cadena |
| `matriz_repulsion()` | Ninguna | Matriz simétrica a_ij; contiene las dos entradas complementarias indicadas arriba |
| `fuerzas(...)` | Posiciones, velocidades, tipos, enlaces y generador aleatorio | Busca vecinos con cKDTree periódico; suma fuerzas por pares y resortes; entrega fuerzas y energía conservativa |
| `paso_dpd(...)` | Estado actual y dt | Actualiza velocidad y posición; distribuye la fuerza total de NP para mantener traslación rígida |
| `agregar_np(...)` | Estado preparado | Inserta NP y elimina solamente agua superpuesta; conserva los índices de lípidos y enlaces |
| `observables(...)` | Estado y referencia | Desplazamiento RMS tras alineación Kabsch, asfericidad del tensor de giro y energía NP |
| `simular(...)` | Parámetros, destino y opción de animación | Preparación común; impacto y control; guarda CSV, JSON y NPZ |
| `dibujar(...)` | Estados y métricas calculados | Corte de espesor finito y curvas; no modifica las posiciones |
| `verificar()` | Ninguna | Pruebas de fuerza/energía, acción/reacción, vuelo libre, potencia disipativa, relación térmica y oscilador analítico |

El algoritmo del paso es: buscar pares → calcular fuerzas → sumar acción/reacción → proyectar fuerza de NP a traslación rígida → actualizar velocidades → actualizar posiciones → aplicar periodicidad. La visualización ocurre después de resolver la dinámica.

## Aprender una simulación analítica

Para dos beads iguales aislados unidos por el resorte del artículo, sin contacto no enlazado ni termostato, la masa reducida es `m/2` y la rigidez es `k=C/rs`. Si parten en reposo con separación r0:

```text
omega = sqrt(2 C / (m rs))
r(t)  = rs + (r0−rs) cos(omega t)
```

Esta solución verifica la integración de un **subproblema**, no toda la membrana. El verificador usa separaciones mayores que rc para que no intervenga repulsión adicional. Al reducir dt a la mitad, el error del integrador explícito debe disminuir aproximadamente a la mitad en este ensayo.

Para la fuerza conservativa no enlazada, `U_C= a_ij/2 (1−r)²` si r<1; para el resorte, `U_S=C/(2rs)(r−rs)²`. Deriva ambas fuerzas antes de pedir a Copilot que las implemente. La prueba por diferencias finitas comprueba `F=−grad(U)`.

## Trabajo con Copilot y defensa

Solicita ayuda en pasos pequeños:

1. «Explícame el signo de cada fuerza usando d=xj−xi. Calcula la potencia de la fuerza disipativa; no modifiques el código todavía».
2. «Deriva la solución de dos beads unidos por un resorte, identifica la masa reducida y explica por qué omega tiene un factor 2».
3. «Muéstrame las dimensiones de C, rs y C/rs en la ecuación 7 y señala la ambigüedad en el texto».
4. «Lee el CSV y compara impacto con control, sin suponer que todo desplazamiento es daño».
5. «Propón una comprobación de convergencia estocástica por conjuntos de semillas; explica por qué no conviene comparar ruido de dos pasos temporales como si fueran la misma trayectoria».

El alumno debe poder explicar por qué se necesita agua explícita, qué representa cada bead, dónde se conserva momento, qué significa asfericidad y por qué una gráfica de energía de la NP no mide por sí sola la deformación del blanco. Debe identificar al menos tres cambios entre artículo y piloto y justificar qué conclusiones impiden.

Entrega el código comentado, parámetros, CSV, animación, derivación del oscilador, comparación con el control y una explicación oral de `fuerzas` y `paso_dpd` sin leer respuestas de Copilot. No presentar el piloto como evidencia experimental o reproducción cuantitativa del artículo.

## Ensayo generado y límites de observación

Se ejecutaron 1200 pasos de preparación y 1800 pasos por condición, dt=0.004 DPD, semilla 2026. La NP tiene 72 beads rígidos y el blanco 456 cadenas HTTT. La asfericidad final fue aproximadamente 0.0111 en impacto y 0.00132 en control. El radio de giro del control cambió de 4.283 a 4.352 rc; el del impacto, de 4.283 a 4.487 rc. Los valores exactos están en [OBSERVACION_VESICULA.json](../../pruebas/evidencia/OBSERVACION_VESICULA.json).

La asfericidad mide desviación global de una forma esférica. El RMS alineado también incluye difusión lateral de los lípidos: no es deformación unitaria ni área de poro. Un solo par de trayectorias no demuestra significación estadística. La preparación no certifica equilibrio termodinámico; faltan ensayos más largos, varias semillas, refinamiento de paso en conjunto y calibración del mapeo a unidades físicas. El piloto sirve para explorar la construcción del modelo, no para afirmar reproducción de resultados publicados.
