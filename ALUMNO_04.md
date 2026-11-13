# Alumno 04 · Aceleración por arrastre a Reynolds intermedio

Nombre: __________________________

## Artículo individual

**Pirmoradi et al. (2015). A microarray MEMS device for biolistic delivery of vaccine and drug powders.** Human Vaccines & Immunotherapeutics 11(8), 1936-1944. DOI: [10.1080/21645515.2015.1029211](https://doi.org/10.1080/21645515.2015.1029211).

[Lectura y versión disponible](https://pmc.ncbi.nlm.nih.gov/articles/PMC4635881/). Texto completo abierto, CC BY-NC 3.0; texto XML oficial alternativo en Europe PMC.

**Dónde está el modelo:** Device Operating Principle and Design, ecuación (1).

## Modelo y alcance

m dv/dt=3πμd(u-v){1+[ρf d |u-v|/μ]^(2/3)/6}.

**Qué hace este ejemplo:** Flujo uniforme prescrito. s=t/τ, τ=m/(3πμd), w=v/u y Re0=ρfdu/μ: dw/ds=(1-w)[1+(Re0|1-w|)^(2/3)/6]. No se modelan los microcanales ni la presión del dispositivo.

Los tres escenarios modifican únicamente `Re0`: A=0.1, B=1.0, C=10.0. Son escenarios de práctica, no condiciones experimentales recomendadas.

## Paso a paso

1. Completa la [preparación común](README.md#preparación-común-en-windows-y-visual-studio-code).
2. Abre [simulacion_04.py](simulacion_04.py) en VS Code. Identifica las constantes, la ecuación y `main()`.
3. Antes de ejecutar, escribe qué esperas que cambie entre A y C y por qué. Todavía no leas las gráficas de ejemplo.
4. Ejecuta solo A:

   ```powershell
   .\.venv\Scripts\python.exe simulacion_04.py --escenario A
   ```

5. Revisa `resultados/alumno_04/escenario_A.csv`, `parametros.json` y `comparacion.png`. Explica cada columna y cada eje.
6. Ejecuta los tres escenarios y sus comprobaciones:

   ```powershell
   .\.venv\Scripts\python.exe simulacion_04.py --escenario todos --verificar
   ```

7. Explica qué comprueba `verificar()` y por qué una comprobación numérica no demuestra validación biológica.
8. Desarrolla este reto: **Añadir el caso Re0=0 y compararlo con w=1-exp(-s). Explicar por qué la velocidad se aproxima a la del fluido y no crece sin límite.** Guarda tu modificación como `mi_simulacion_04.py` para conservar el ejemplo original.
9. Trabaja con Copilot por etapas usando el prompt siguiente; después explica el código con tus propias palabras.
10. Prepara tu informe, tabla de funciones y defensa. El programa de ejemplo es un punto de partida; debes aportar la modificación, la predicción y el análisis.

## Prompt inicial para Copilot

> Actúa como tutor de Python. Estoy trabajando en el alumno 04, Aceleración por arrastre a Reynolds intermedio. Lee ALUMNO_04.md y simulacion_04.py. Primero explícame la ecuación y los supuestos; pídeme una predicción. Después revisemos una función por vez: sus argumentos, formas de los arreglos, retorno y quién la llama. Ayúdame a realizar el reto sin cambiar silenciosamente el modelo. Distingue ecuaciones publicadas, reducciones docentes y datos simulados. Hazme preguntas antes de avanzar y comprueba los cambios.

## Mapa del código

| Función | Ubicación |
|---|---|
| `integrar_rk4` | [Línea 16](simulacion_04.py#L16) |
| `calcular_modelo` | [Línea 39](simulacion_04.py#L39) |
| `verificar` | [Línea 52](simulacion_04.py#L52) |
| `comparar_escenarios` | [Línea 63](simulacion_04.py#L63) |
| `guardar_resultados` | [Línea 69](simulacion_04.py#L69) |
| `graficar_resultados` | [Línea 80](simulacion_04.py#L80) |
| `main` | [Línea 92](simulacion_04.py#L92) |

Para cada función prepara una fila con: propósito, entradas, unidades o escalas, forma del arreglo, salida, quién la llama y una prueba o comprobación. Explica la diferencia entre devolver un dato con `return`, imprimirlo y guardarlo en un archivo.

## Defensa individual

¿Qué representa la velocidad relativa u-v? ¿Cuál es la diferencia con el frenado del alumno 01?

Además, el docente podrá elegir una función al azar y pedirte cambiar un parámetro antes de volver a ejecutar. Debes predecir el efecto y explicar cualquier diferencia con tu predicción.

## Entrega

- `mi_simulacion_04.py` y `requirements.txt`.
- Los tres CSV, los parámetros y la figura comparativa.
- Informe de 2 páginas: referencia y ubicación de la ecuación; supuestos; predicción; resultados; comprobación; límites.
- Tabla de funciones y registro breve de tres ayudas de Copilot, con lo que aceptaste, corregiste o verificaste.

No entregues `.venv` ni conversaciones personales completas. Fecha y plataforma: las define el docente.

[Volver a la distribución](README.md#distribución-sin-artículos-repetidos).
