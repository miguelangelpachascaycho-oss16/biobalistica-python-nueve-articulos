# Alumno 06 · Seguimiento lagrangiano de una partícula

Nombre: __________________________

## Artículo individual

**Thorpe et al. (2025). Enhancing biolistic plant transformation and genome editing with a flow guiding barrel.** Nature Communications 16, 5624. DOI: [10.1038/s41467-025-60761-x](https://www.nature.com/articles/s41467-025-60761-x).

[Lectura y versión disponible](https://pmc.ncbi.nlm.nih.gov/articles/PMC12216195/). Texto completo abierto CC BY-NC-ND 4.0. Reproducción parcial de un submodelo físico.

**Dónde está el modelo:** Methods: COMSOL simulations; COMSOL simulation and particle tracking. Se identifica el seguimiento lagrangiano con arrastre de Stokes.

## Modelo y alcance

m dv/dt=6πηR(uf-v); dx/dt=v, en forma vectorial.

**Qué hace este ejemplo:** Reducción 2D de la parte de seguimiento. Tiempo s=t/τ, uf=(1,α sin s), posiciones relativas a Urefτ. El campo de flujo es prescrito y docente. No se calcula el CFD compresible, la geometría ni los resultados biológicos del artículo.

Los tres escenarios modifican únicamente `alpha`: A=0.1, B=0.2, C=0.3. Son escenarios de práctica, no condiciones experimentales recomendadas.

## Paso a paso

1. Completa la [preparación común](README.md#preparación-común-en-windows-y-visual-studio-code).
2. Abre [simulacion_06.py](simulacion_06.py) en VS Code. Identifica las constantes, la ecuación y `main()`.
3. Antes de ejecutar, escribe qué esperas que cambie entre A y C y por qué. Todavía no leas las gráficas de ejemplo.
4. Ejecuta solo A:

   ```powershell
   .\.venv\Scripts\python.exe simulacion_06.py --escenario A
   ```

5. Revisa `resultados/alumno_06/escenario_A.csv`, `parametros.json` y `comparacion.png`. Explica cada columna y cada eje.
6. Ejecuta los tres escenarios y sus comprobaciones:

   ```powershell
   .\.venv\Scripts\python.exe simulacion_06.py --escenario todos --verificar
   ```

7. Explica qué comprueba `verificar()` y por qué una comprobación numérica no demuestra validación biológica.
8. Desarrolla este reto: **Añadir flechas de velocidad a la trayectoria y distinguir el campo de flujo del movimiento de la partícula. Explicar por qué prescribir un flujo no equivale a resolverlo.** Guarda tu modificación como `mi_simulacion_06.py` para conservar el ejemplo original.
9. Trabaja con Copilot por etapas usando el prompt siguiente; después explica el código con tus propias palabras.
10. Prepara tu informe, tabla de funciones y defensa. El programa de ejemplo es un punto de partida; debes aportar la modificación, la predicción y el análisis.

## Prompt inicial para Copilot

> Actúa como tutor de Python. Estoy trabajando en el alumno 06, Seguimiento lagrangiano de una partícula. Lee ALUMNO_06.md y simulacion_06.py. Primero explícame la ecuación y los supuestos; pídeme una predicción. Después revisemos una función por vez: sus argumentos, formas de los arreglos, retorno y quién la llama. Ayúdame a realizar el reto sin cambiar silenciosamente el modelo. Distingue ecuaciones publicadas, reducciones docentes y datos simulados. Hazme preguntas antes de avanzar y comprueba los cambios.

## Mapa del código

| Función | Ubicación |
|---|---|
| `integrar_rk4` | [Línea 16](simulacion_06.py#L16) |
| `calcular_modelo` | [Línea 39](simulacion_06.py#L39) |
| `verificar` | [Línea 52](simulacion_06.py#L52) |
| `comparar_escenarios` | [Línea 65](simulacion_06.py#L65) |
| `guardar_resultados` | [Línea 71](simulacion_06.py#L71) |
| `graficar_resultados` | [Línea 82](simulacion_06.py#L82) |
| `main` | [Línea 94](simulacion_06.py#L94) |

Para cada función prepara una fila con: propósito, entradas, unidades o escalas, forma del arreglo, salida, quién la llama y una prueba o comprobación. Explica la diferencia entre devolver un dato con `return`, imprimirlo y guardarlo en un archivo.

## Defensa individual

¿Qué contiene el vector estado? ¿Qué devuelve derivadas? ¿Qué parte de COMSOL reemplaza tu programa y cuál queda fuera?

Además, el docente podrá elegir una función al azar y pedirte cambiar un parámetro antes de volver a ejecutar. Debes predecir el efecto y explicar cualquier diferencia con tu predicción.

## Entrega

- `mi_simulacion_06.py` y `requirements.txt`.
- Los tres CSV, los parámetros y la figura comparativa.
- Informe de 2 páginas: referencia y ubicación de la ecuación; supuestos; predicción; resultados; comprobación; límites.
- Tabla de funciones y registro breve de tres ayudas de Copilot, con lo que aceptaste, corregiste o verificaste.

No entregues `.venv` ni conversaciones personales completas. Fecha y plataforma: las define el docente.

[Volver a la distribución](README.md#distribución-sin-artículos-repetidos).
