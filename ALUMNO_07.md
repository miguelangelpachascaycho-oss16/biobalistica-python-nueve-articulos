# Alumno 07 · Modelo analítico de Poncelet y parada

Nombre: __________________________

## Artículo individual

**Shen et al. (2025). Investigation of dynamic behavior of human skin tissue under micro-particle impact in the context of transdermal drug delivery: numerical and analytical perspectives.** Theoretical and Applied Mechanics Letters 15, 100567; disponible en línea en 2024. DOI: [10.1016/j.taml.2024.100567](https://doi.org/10.1016/j.taml.2024.100567).

[Lectura y versión disponible](https://pubs-en.cstam.org.cn/data/article/taml/preview/pdf/20250202.pdf). Artículo completo abierto CC BY 4.0; PDF de la revista.

**Dónde está el modelo:** Sección 2.1, Analytical model, ecuaciones (1) y (4)-(6).

## Modelo y alcance

-M dV/dt=B V²+C; tf=M/sqrt(BC)*atan(v0 sqrt(B/C)).

**Qué hace este ejemplo:** Submodelo homogéneo con s=t sqrt(BC)/M, w=V sqrt(B/C), z=PB/M. Entonces w'=-(1+w²), z'=w; sf=atan(w0). No se reproduce el SPH-FEM ni las capas de piel del artículo.

Los tres escenarios modifican únicamente `w0`: A=0.5, B=1.0, C=2.0. Son escenarios de práctica, no condiciones experimentales recomendadas.

## Paso a paso

1. Completa la [preparación común](README.md#preparación-común-en-windows-y-visual-studio-code).
2. Abre [simulacion_07.py](simulacion_07.py) en VS Code. Identifica las constantes, la ecuación y `main()`.
3. Antes de ejecutar, escribe qué esperas que cambie entre A y C y por qué. Todavía no leas las gráficas de ejemplo.
4. Ejecuta solo A:

   ```powershell
   .\.venv\Scripts\python.exe simulacion_07.py --escenario A
   ```

5. Revisa `resultados/alumno_07/escenario_A.csv`, `parametros.json` y `comparacion.png`. Explica cada columna y cada eje.
6. Ejecuta los tres escenarios y sus comprobaciones:

   ```powershell
   .\.venv\Scripts\python.exe simulacion_07.py --escenario todos --verificar
   ```

7. Explica qué comprueba `verificar()` y por qué una comprobación numérica no demuestra validación biológica.
8. Desarrolla este reto: **Comprobar la trayectoria numérica con las expresiones cerradas y verificar z_final=0.5*ln(1+w0²). Diferenciar verificar un cálculo y validar un tejido.** Guarda tu modificación como `mi_simulacion_07.py` para conservar el ejemplo original.
9. Trabaja con Copilot por etapas usando el prompt siguiente; después explica el código con tus propias palabras.
10. Prepara tu informe, tabla de funciones y defensa. El programa de ejemplo es un punto de partida; debes aportar la modificación, la predicción y el análisis.

## Prompt inicial para Copilot

> Actúa como tutor de Python. Estoy trabajando en el alumno 07, Modelo analítico de Poncelet y parada. Lee ALUMNO_07.md y simulacion_07.py. Primero explícame la ecuación y los supuestos; pídeme una predicción. Después revisemos una función por vez: sus argumentos, formas de los arreglos, retorno y quién la llama. Ayúdame a realizar el reto sin cambiar silenciosamente el modelo. Distingue ecuaciones publicadas, reducciones docentes y datos simulados. Hazme preguntas antes de avanzar y comprueba los cambios.

## Mapa del código

| Función | Ubicación |
|---|---|
| `integrar_rk4` | [Línea 16](simulacion_07.py#L16) |
| `calcular_modelo` | [Línea 39](simulacion_07.py#L39) |
| `verificar` | [Línea 50](simulacion_07.py#L50) |
| `comparar_escenarios` | [Línea 62](simulacion_07.py#L62) |
| `guardar_resultados` | [Línea 68](simulacion_07.py#L68) |
| `graficar_resultados` | [Línea 79](simulacion_07.py#L79) |
| `main` | [Línea 91](simulacion_07.py#L91) |

Para cada función prepara una fila con: propósito, entradas, unidades o escalas, forma del arreglo, salida, quién la llama y una prueba o comprobación. Explica la diferencia entre devolver un dato con `return`, imprimirlo y guardarlo en un archivo.

## Defensa individual

¿Cómo obtienes el instante final? ¿Qué ocurre si continúas la tangente después de la parada? ¿Qué es verificación y qué es validación?

Además, el docente podrá elegir una función al azar y pedirte cambiar un parámetro antes de volver a ejecutar. Debes predecir el efecto y explicar cualquier diferencia con tu predicción.

## Entrega

- `mi_simulacion_07.py` y `requirements.txt`.
- Los tres CSV, los parámetros y la figura comparativa.
- Informe de 2 páginas: referencia y ubicación de la ecuación; supuestos; predicción; resultados; comprobación; límites.
- Tabla de funciones y registro breve de tres ayudas de Copilot, con lo que aceptaste, corregiste o verificaste.

No entregues `.venv` ni conversaciones personales completas. Fecha y plataforma: las define el docente.

[Volver a la distribución](README.md#distribución-sin-artículos-repetidos).
