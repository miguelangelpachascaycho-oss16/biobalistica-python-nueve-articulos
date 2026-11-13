# Alumno 01 · Frenado viscoso de una nanopartícula

Nombre: __________________________

## Artículo individual

**Fraire et al. (2022). Light triggered nanoscale biolistics for efficient intracellular delivery of functional macromolecules in mammalian cells.** Nature Communications 13, 1996. DOI: [10.1038/s41467-022-29713-7](https://www.nature.com/articles/s41467-022-29713-7).

[Lectura y versión disponible](https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-022-29713-7/MediaObjects/41467_2022_29713_MOESM1_ESM.docx). Artículo abierto CC BY 4.0; el modelo está en su suplemento original.

**Dónde está el modelo:** Suplemento: Theory and simulations, ecuaciones (4)-(9) y (11).

## Modelo y alcance

m dv/dt = -6πηRv; τ = m/(6πηR); v = v0 exp(-t/τ); r = v0τ[1-exp(-t/τ)].

**Qué hace este ejemplo:** Se reproduce el submodelo analítico de movimiento en un medio uniforme. Se usan s=t/T, w=v/v0, z=r/(v0T), a=τ/T. No se calcula interacción con membrana.

Los tres escenarios modifican únicamente `a`: A=0.5, B=1.0, C=2.0. Son escenarios de práctica, no condiciones experimentales recomendadas.

## Paso a paso

1. Completa la [preparación común](README.md#preparación-común-en-windows-y-visual-studio-code).
2. Abre [simulacion_01.py](simulacion_01.py) en VS Code. Identifica las constantes, la ecuación y `main()`.
3. Antes de ejecutar, escribe qué esperas que cambie entre A y C y por qué. Todavía no leas las gráficas de ejemplo.
4. Ejecuta solo A:

   ```powershell
   .\.venv\Scripts\python.exe simulacion_01.py --escenario A
   ```

5. Revisa `resultados/alumno_01/escenario_A.csv`, `parametros.json` y `comparacion.png`. Explica cada columna y cada eje.
6. Ejecuta los tres escenarios y sus comprobaciones:

   ```powershell
   .\.venv\Scripts\python.exe simulacion_01.py --escenario todos --verificar
   ```

7. Explica qué comprueba `verificar()` y por qué una comprobación numérica no demuestra validación biológica.
8. Desarrolla este reto: **Cambiar a sin cambiar el resto del programa; comparar el error de Euler con pasos 0.04 y 0.02. Explicar por qué la distancia se aproxima a una asíntota.** Guarda tu modificación como `mi_simulacion_01.py` para conservar el ejemplo original.
9. Trabaja con Copilot por etapas usando el prompt siguiente; después explica el código con tus propias palabras.
10. Prepara tu informe, tabla de funciones y defensa. El programa de ejemplo es un punto de partida; debes aportar la modificación, la predicción y el análisis.

## Prompt inicial para Copilot

> Actúa como tutor de Python. Estoy trabajando en el alumno 01, Frenado viscoso de una nanopartícula. Lee ALUMNO_01.md y simulacion_01.py. Primero explícame la ecuación y los supuestos; pídeme una predicción. Después revisemos una función por vez: sus argumentos, formas de los arreglos, retorno y quién la llama. Ayúdame a realizar el reto sin cambiar silenciosamente el modelo. Distingue ecuaciones publicadas, reducciones docentes y datos simulados. Hazme preguntas antes de avanzar y comprueba los cambios.

## Mapa del código

| Función | Ubicación |
|---|---|
| `integrar_rk4` | [Línea 17](simulacion_01.py#L17) |
| `calcular_modelo` | [Línea 40](simulacion_01.py#L40) |
| `verificar` | [Línea 49](simulacion_01.py#L49) |
| `comparar_escenarios` | [Línea 60](simulacion_01.py#L60) |
| `guardar_resultados` | [Línea 66](simulacion_01.py#L66) |
| `graficar_resultados` | [Línea 77](simulacion_01.py#L77) |
| `main` | [Línea 89](simulacion_01.py#L89) |

Para cada función prepara una fila con: propósito, entradas, unidades o escalas, forma del arreglo, salida, quién la llama y una prueba o comprobación. Explica la diferencia entre devolver un dato con `return`, imprimirlo y guardarlo en un archivo.

## Defensa individual

¿Dónde está la ecuación? ¿Qué diferencia hay entre τ, T y a? ¿Por qué z no es una profundidad experimental de transfección?

Además, el docente podrá elegir una función al azar y pedirte cambiar un parámetro antes de volver a ejecutar. Debes predecir el efecto y explicar cualquier diferencia con tu predicción.

## Entrega

- `mi_simulacion_01.py` y `requirements.txt`, junto con el módulo compartido `animaciones.py`.
- Los tres CSV, los parámetros y la figura comparativa.
- Informe de 2 páginas: referencia y ubicación de la ecuación; supuestos; predicción; resultados; comprobación; límites.
- Tabla de funciones y registro breve de tres ayudas de Copilot, con lo que aceptaste, corregiste o verificaste.

No entregues `.venv` ni conversaciones personales completas. Fecha y plataforma: las define el docente.

[Volver a la distribución](README.md#distribución-sin-artículos-repetidos).

## Ver el movimiento y analizarlo

Ejecuta `python simulacion_01.py --escenario todos --verificar --animar`. Abre `resultados/alumno_01/visor.html` en el navegador: puedes pausar, arrastrar el tiempo y cambiar A/B/C. También se generan `animacion.gif` (escenario B si existe) y `metricas.json` con resultados de los tres escenarios. El tiempo de reproducción está ralentizado; las unidades del modelo son relativas.

Explica `preparar_serie`, `resumir_metricas` y `exportar_movimiento` en [animaciones.py](animaciones.py): convierten los estados calculados en posiciones, métricas y cuadros. La ecuación permanece en tu archivo individual. El tamaño dibujado de la esfera se amplifica para verla.

Entrega también el visor, el GIF y una tabla de métricas A/B/C. No deduzcas deformación del tejido a partir de una trayectoria: en 02/03/05/07/08 se calcula penetración; en 09, indentación y fuerza del contacto elástico; en 01/04/06 se calcula movimiento en el fluido y el impacto no está resuelto. El dibujo del contorno es esquemático y no proporciona tensiones ni deformaciones locales.

Conserva `animaciones.py` en la misma carpeta que tu programa. El integrador y las ecuaciones están en el archivo individual; el módulo compartido transforma sus resultados en gráficos y animaciones.
