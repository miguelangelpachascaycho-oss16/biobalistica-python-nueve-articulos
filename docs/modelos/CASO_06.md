# Caso 06 — contacto activo con una hoja elástica

**Categoría: penetración mecánica, no biobalística inercial.** Se incluye por la ampliación de tema autorizada por el docente. El blanco es un modelo mínimo de membrana artificial inspirado en membranas celulares; no una célula real ni una bicapa molecular.

Lectura: A. Daddi-Moussa-Ider, B. Liebchen, A. M. Menzel y H. Löwen (2019), *Theory of active particle penetration through a planar elastic membrane*, New Journal of Physics 21, 083014. [DOI 10.1088/1367-2630/ab35d2](https://doi.org/10.1088/1367-2630/ab35d2). [Texto completo abierto de autores, CC BY 3.0](https://user.thphy.uni-duesseldorf.de/hlowen/doc/op/op0409.pdf). [Repositorio institucional alternativo](https://tuprints.ulb.tu-darmstadt.de/bitstreams/dfaf6b5e-354f-412f-92ee-db1910f6ab68/download).

## Ejecutar

Desde la carpeta del repositorio en VS Code:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe src/caso_06_plana.py --animar
.\.venv\Scripts\python.exe pruebas/verificar_nuevos.py
```

Abre `resultados/caso_06/simulacion.gif`, `simulacion.png`, `metricas.csv`, `parametros.json` y `resumen.json`. El NPZ contiene las coordenadas de cada instante. La figura muestra contacto, desplazamiento máximo y perfil normal con referencia analítica independiente. La vista 3D amplía visualmente el eje z; las coordenadas y métricas conservan sus unidades.

Para investigar el efecto de la carga, ejecuta otro directorio y compara curvas:

```powershell
.\.venv\Scripts\python.exe src/caso_06_plana.py --fuerza 0.2 --salida resultados/caso_06_menor --animar
```

## Modelo del artículo

Las ecuaciones 1–3 combinan energía WCA y resortes entre ocho vecinos. WCA usa `sigma=2a` para beads de membrana y `sigma=a+R` para contacto con la partícula. La energía elástica es `k/2 (r−xi*r0)^2`, con `xi=0.9`. Los resortes se desactivan al superar `ell=1.5h` y pueden volver a actuar al acercarse. No se introduce una rotura irreversible adicional.

El artículo trabaja en régimen sobreamortiguado: `dr/dt=mu*F`, con `mu=1/(6*pi*eta*a)`. La partícula tiene movilidad `mu*a/R` y siente la reacción de los mismos contactos que deforman el blanco, más la fuerza activa constante F0. **No se usa m*d²r/dt² ni una velocidad balística inicial.**

En unidades `a=epsilon=mu=1`, se usan `h=2^(7/6)`, `R=1`, `k=2*kappa/h`, `kappa=1`, `F0=0.4`. La dimensión temporal física, si se dispusiera de a, eta y epsilon calibrados, sería `a²/(mu*epsilon)`. Aquí no se asignan unidades SI a estos números.

## Reducciones declaradas

El artículo suele usar 450 beads en una malla girada 45° y condiciones laterales periódicas con bordes sujetos. El ejercicio usa 196 beads en una malla cuadrada sin ese giro, con periferia fija y sin imágenes periódicas. Conserva fuerzas, ocho vecinos, preestrés y corte, pero cambia tamaño y geometría de borde. Integra con RK45 adaptativo en vez del Euler adaptativo del artículo. El paso máximo impide saltarse el contacto durante el vuelo libre. La ejecución predeterminada estudia **atrapamiento con deformación**, no reproduce el diagrama completo de penetración/autorreparación.

El control sin carga permanece en la configuración inicial: se comprueba que la fuerza sobre cada nodo libre sea cero, dentro de precisión numérica. Las reacciones de los apoyos se distinguen de fuerzas internas del blanco.

## Funciones y estructura

El ejecutable `src/caso_06_plana.py` lee argumentos, crea `Parametros` y llama a `simular` de `src/penetracion_activa.py`.

| Función | Qué recibe y realiza | Qué entrega |
|---|---|---|
| `Parametros` | Configuración de fuerza, tamaño, preestrés y tolerancias | Datos reproducibles del ensayo |
| `construir` | Parámetros | Coordenadas, vecinos, longitudes de reposo, apoyos y posición de partícula |
| `wca` | Vectores de separación y sigma | Repulsión y energía desplazada al corte |
| `fuerzas` | Posiciones de membrana/partícula | Fuerzas del blanco y reacción del contacto sobre la partícula |
| `referencia_analitica` | Coordenadas, h y parámetros | Serie de Fourier de pequeña deformación; no mueve los nodos de la animación |
| `simular` y su función interna `rhs` | Estado inicial, parámetros y carpeta | Integra la movilidad de Stokes; guarda estados y observables |
| `dibujar` | Estados calculados | GIF, figura y perfil comparativo |

## Construir la solución analítica

En el límite lineal del artículo, ecuaciones 16–24, el desplazamiento normal w satisface una ecuación de Poisson. Para una carga puntual centrada:

```text
P0 = 2F0/(k*h)
Hp = (2p−1)*pi/L
w_hat(p,q) = h*P0/[6*(1−xi)*(Hp²+Hq²)]
w(x,y) = 4/L² sum_p sum_q w_hat(p,q)*cos(Hp*x)*cos(Hq*y)
```

El estado transitorio se obtiene multiplicando cada coeficiente por `1−exp(−3*A*(1−xi)*(Hp²+Hq²)*t)`, con `A=mu*k*h²`. La serie aproxima una fuerza puntual y una membrana continua. El contacto real del programa distribuye la carga sobre varios beads: no esperes igualdad exacta en el centro. Compara lejos de la carga, aumenta modos y verifica que la aproximación mejore al disminuir F0.

## Copilot, trabajo y defensa

Pide a Copilot que derive `F=−grad(U)` y el factor de decaimiento de cada modo de Fourier antes de cambiar el código. Después implementa una función pequeña que evalúe la serie y explica sus dimensiones. Preguntas de defensa: ¿dónde se aplica acción/reacción?, ¿qué aporta xi?, ¿por qué no hay conservación de energía mecánica en Stokes?, ¿qué diferencia una fuerza activa de un impacto balístico?, ¿qué parte del resultado cambia al reducir la membrana?

Entrega diagrama de fuerzas, ecuaciones, explicación de funciones, comparación de dos cargas, animación, CSV, verificador y derivación de Fourier. No atribuyas la deformación observada a células reales ni presentes este ejercicio como réplica de las figuras del artículo.
