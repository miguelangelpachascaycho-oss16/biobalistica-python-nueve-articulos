# Alumno 05 · Simulación estadística de una razón y su incertidumbre

Nombre: __________________________

## Artículo individual

**Miller et al. (2021). An improved biolistic delivery and analysis method for evaluation of DNA and CRISPR-Cas delivery efficacy in plant tissue.** Scientific Reports 11, 7695. DOI: [10.1038/s41598-021-86549-9](https://www.nature.com/articles/s41598-021-86549-9).

[Lectura y versión disponible](https://pmc.ncbi.nlm.nih.gov/articles/PMC8032657/). Texto completo abierto, CC BY 4.0. Es una simulación estadística de análisis, no de penetración.

**Dónde está el modelo:** Methods: Statistical analysis; fórmula Q=a/b y propagación de incertidumbre. Contexto de normalización: figura 2.

## Modelo y alcance

Q=a/b; δQ/|Q|=sqrt[(δa/a)²+(δb/b)²], suponiendo incertidumbres independientes.

**Qué hace este ejemplo:** Se reproduce la propagación de incertidumbre. Para contrastarla por Monte Carlo se eligen variables lognormales positivas e independientes con medias 100 y coeficiente de variación CV. Esa distribución y los datos son docentes, no mediciones ni un supuesto atribuido a los autores.

Los tres escenarios modifican únicamente `CV`: A=0.02, B=0.05, C=0.1. Son escenarios de práctica, no condiciones experimentales recomendadas.

## Paso a paso

1. Completa la [preparación común](README.md#preparación-común-en-windows-y-visual-studio-code).
2. Abre [simulacion_05.py](simulacion_05.py) en VS Code. Identifica las constantes, la ecuación y `main()`.
3. Antes de ejecutar, escribe qué esperas que cambie entre A y C y por qué. Todavía no leas las gráficas de ejemplo.
4. Ejecuta solo A:

   ```powershell
   .\.venv\Scripts\python.exe simulacion_05.py --escenario A
   ```

5. Revisa `resultados/alumno_05/escenario_A.csv`, `parametros.json` y `comparacion.png`. Explica cada columna y cada eje.
6. Ejecuta los tres escenarios y sus comprobaciones:

   ```powershell
   .\.venv\Scripts\python.exe simulacion_05.py --escenario todos --verificar
   ```

7. Explica qué comprueba `verificar()` y por qué una comprobación numérica no demuestra validación biológica.
8. Desarrolla este reto: **Comparar la desviación estándar simulada con sqrt(2)*CV. Cambiar la semilla y luego el número de repeticiones; explicar qué cambia. Identificar la independencia requerida por la fórmula.** Guarda tu modificación como `mi_simulacion_05.py` para conservar el ejemplo original.
9. Trabaja con Copilot por etapas usando el prompt siguiente; después explica el código con tus propias palabras.
10. Prepara tu informe, tabla de funciones y defensa. El programa de ejemplo es un punto de partida; debes aportar la modificación, la predicción y el análisis.

## Prompt inicial para Copilot

> Actúa como tutor de Python. Estoy trabajando en el alumno 05, Simulación estadística de una razón y su incertidumbre. Lee ALUMNO_05.md y simulacion_05.py. Primero explícame la ecuación y los supuestos; pídeme una predicción. Después revisemos una función por vez: sus argumentos, formas de los arreglos, retorno y quién la llama. Ayúdame a realizar el reto sin cambiar silenciosamente el modelo. Distingue ecuaciones publicadas, reducciones docentes y datos simulados. Hazme preguntas antes de avanzar y comprueba los cambios.

## Mapa del código

| Función | Ubicación |
|---|---|
| `muestrear_positivo` | [Línea 25](simulacion_05.py#L25) |
| `calcular_modelo` | [Línea 32](simulacion_05.py#L32) |
| `verificar` | [Línea 42](simulacion_05.py#L42) |
| `comparar_escenarios` | [Línea 52](simulacion_05.py#L52) |
| `guardar_resultados` | [Línea 58](simulacion_05.py#L58) |
| `graficar_resultados` | [Línea 69](simulacion_05.py#L69) |
| `main` | [Línea 81](simulacion_05.py#L81) |

Para cada función prepara una fila con: propósito, entradas, unidades o escalas, forma del arreglo, salida, quién la llama y una prueba o comprobación. Explica la diferencia entre devolver un dato con `return`, imprimirlo y guardarlo en un archivo.

## Defensa individual

¿Qué simulas y qué ecuación procede del artículo? ¿Por qué un intervalo del 95 % no demuestra eficacia de transferencia?

Además, el docente podrá elegir una función al azar y pedirte cambiar un parámetro antes de volver a ejecutar. Debes predecir el efecto y explicar cualquier diferencia con tu predicción.

## Entrega

- `mi_simulacion_05.py` y `requirements.txt`.
- Los tres CSV, los parámetros y la figura comparativa.
- Informe de 2 páginas: referencia y ubicación de la ecuación; supuestos; predicción; resultados; comprobación; límites.
- Tabla de funciones y registro breve de tres ayudas de Copilot, con lo que aceptaste, corregiste o verificaste.

No entregues `.venv` ni conversaciones personales completas. Fecha y plataforma: las define el docente.

[Volver a la distribución](README.md#distribución-sin-artículos-repetidos).
