# Alumno 09 · Transferencia térmica transitoria en dos capas

Nombre: __________________________

## Artículo individual

**Liu (2006). Quantitative Evaluation of the Skin Heat Transfer Characteristics Subjected to a Transient High-speed Helium Gas Impingement.** Journal of Biological Sciences 6(2), 231-237. DOI: [10.3923/jbs.2006.231.237](https://scialert.net/fulltext/index.php?doi=jbs.2006.231.237).

[Lectura y versión disponible](https://scialert.net/fulltext/index.php?doi=jbs.2006.231.237). Texto completo accesible en la revista. No se copia ni se redistribuye el artículo.

**Dónde está el modelo:** Results and Discussion: Skin heat transfer; modelo unidimensional de dos capas y figura 8.

## Modelo y alcance

ρ c ∂T/∂t=∂(k ∂T/∂x)/∂x, con intercambio convectivo en la superficie.

**Qué hace este ejemplo:** Se explicita la ecuación de conducción estándar correspondiente al modelo 1D descrito en el texto; no tiene número de ecuación allí. Se usan coordenadas relativas, conductividad uniforme, capacidades relativas 1.3 y 1 en dos capas docentes y un pulso térmico de práctica. No se reproduce el flujo de gas calculado por los autores.

Los tres escenarios modifican únicamente `Bi`: A=0.2, B=0.5, C=1.0. Son escenarios de práctica, no condiciones experimentales recomendadas.

## Paso a paso

1. Completa la [preparación común](README.md#preparación-común-en-windows-y-visual-studio-code).
2. Abre [simulacion_09.py](simulacion_09.py) en VS Code. Identifica las constantes, la ecuación y `main()`.
3. Antes de ejecutar, escribe qué esperas que cambie entre A y C y por qué. Todavía no leas las gráficas de ejemplo.
4. Ejecuta solo A:

   ```powershell
   .\.venv\Scripts\python.exe simulacion_09.py --escenario A
   ```

5. Revisa `resultados/alumno_09/escenario_A.csv`, `parametros.json` y `comparacion.png`. Explica cada columna y cada eje.
6. Ejecuta los tres escenarios y sus comprobaciones:

   ```powershell
   .\.venv\Scripts\python.exe simulacion_09.py --escenario todos --verificar
   ```

7. Explica qué comprueba `verificar()` y por qué una comprobación numérica no demuestra validación biológica.
8. Desarrolla este reto: **Duplicar el número de nodos y comparar el máximo superficial. Explicar el paso de estabilidad y la condición convectiva. Probar una entrada térmica nula.** Guarda tu modificación como `mi_simulacion_09.py` para conservar el ejemplo original.
9. Trabaja con Copilot por etapas usando el prompt siguiente; después explica el código con tus propias palabras.
10. Prepara tu informe, tabla de funciones y defensa. El programa de ejemplo es un punto de partida; debes aportar la modificación, la predicción y el análisis.

## Prompt inicial para Copilot

> Actúa como tutor de Python. Estoy trabajando en el alumno 09, Transferencia térmica transitoria en dos capas. Lee ALUMNO_09.md y simulacion_09.py. Primero explícame la ecuación y los supuestos; pídeme una predicción. Después revisemos una función por vez: sus argumentos, formas de los arreglos, retorno y quién la llama. Ayúdame a realizar el reto sin cambiar silenciosamente el modelo. Distingue ecuaciones publicadas, reducciones docentes y datos simulados. Hazme preguntas antes de avanzar y comprueba los cambios.

## Mapa del código

| Función | Ubicación |
|---|---|
| `calcular_modelo` | [Línea 25](simulacion_09.py#L25) |
| `verificar` | [Línea 46](simulacion_09.py#L46) |
| `comparar_escenarios` | [Línea 55](simulacion_09.py#L55) |
| `guardar_resultados` | [Línea 61](simulacion_09.py#L61) |
| `graficar_resultados` | [Línea 72](simulacion_09.py#L72) |
| `main` | [Línea 84](simulacion_09.py#L84) |

Para cada función prepara una fila con: propósito, entradas, unidades o escalas, forma del arreglo, salida, quién la llama y una prueba o comprobación. Explica la diferencia entre devolver un dato con `return`, imprimirlo y guardarlo en un archivo.

## Defensa individual

¿Qué guarda el arreglo de temperaturas? ¿Por qué no puedes elegir cualquier paso temporal? ¿Qué datos has supuesto en la frontera?

Además, el docente podrá elegir una función al azar y pedirte cambiar un parámetro antes de volver a ejecutar. Debes predecir el efecto y explicar cualquier diferencia con tu predicción.

## Entrega

- `mi_simulacion_09.py` y `requirements.txt`.
- Los tres CSV, los parámetros y la figura comparativa.
- Informe de 2 páginas: referencia y ubicación de la ecuación; supuestos; predicción; resultados; comprobación; límites.
- Tabla de funciones y registro breve de tres ayudas de Copilot, con lo que aceptaste, corregiste o verificaste.

No entregues `.venv` ni conversaciones personales completas. Fecha y plataforma: las define el docente.

[Volver a la distribución](README.md#distribución-sin-artículos-repetidos).
