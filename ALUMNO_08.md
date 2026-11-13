# Alumno 08 · Arrastre de Clift-Gauvin en un gel

Nombre: __________________________

## Artículo individual

**Veysset et al. (2020). High-Strain-Rate Behavior of a Viscoelastic Gel Under High-Velocity Microparticle Impact.** Experimental Mechanics 60, 1179-1186. DOI: [10.1007/s11340-020-00639-9](https://link.springer.com/article/10.1007/s11340-020-00639-9).

[Lectura y versión disponible](https://www.researchgate.net/publication/343621209_High-Strain-Rate_Behavior_of_a_Viscoelastic_Gel_Under_High-Velocity_Microparticle_Impact). La versión editorial requiere suscripción. Se localizó texto completo del manuscrito aceptado depositado por autores en ResearchGate; podría requerir cuenta. No se redistribuye ese PDF.

**Dónde está el modelo:** Manuscrito aceptado de los autores, ecuaciones (1)-(2): modified Clift-Gauvin model.

## Modelo y alcance

Cd=24/Re*(1+0.15 Re^0.687)+0.42/[1+42500 Re^(-1.16)]; F=0.5 Cd ρ A v²+A R.

**Qué hace este ejemplo:** Con Re=Re0*w, se resuelve w'=-[K Cd(Re0*w) w²+Y], z'=w, hasta w=0. K=0.02 e Y=0.1 son parámetros docentes adimensionales; no se ajusta viscosidad ni resistencia de un gel real.

Los tres escenarios modifican únicamente `Re0`: A=5.0, B=50.0, C=500.0. Son escenarios de práctica, no condiciones experimentales recomendadas.

## Paso a paso

1. Completa la [preparación común](README.md#preparación-común-en-windows-y-visual-studio-code).
2. Abre [simulacion_08.py](simulacion_08.py) en VS Code. Identifica las constantes, la ecuación y `main()`.
3. Antes de ejecutar, escribe qué esperas que cambie entre A y C y por qué. Todavía no leas las gráficas de ejemplo.
4. Ejecuta solo A:

   ```powershell
   .\.venv\Scripts\python.exe simulacion_08.py --escenario A
   ```

5. Revisa `resultados/alumno_08/escenario_A.csv`, `parametros.json` y `comparacion.png`. Explica cada columna y cada eje.
6. Ejecuta los tres escenarios y sus comprobaciones:

   ```powershell
   .\.venv\Scripts\python.exe simulacion_08.py --escenario todos --verificar
   ```

7. Explica qué comprueba `verificar()` y por qué una comprobación numérica no demuestra validación biológica.
8. Desarrolla este reto: **Implementar la evaluación estable de Cd*w² cuando w tiende a cero. Añadir una comparación de Cd(Re) con Stokes a Reynolds pequeño y explicar qué término cambia con la velocidad.** Guarda tu modificación como `mi_simulacion_08.py` para conservar el ejemplo original.
9. Trabaja con Copilot por etapas usando el prompt siguiente; después explica el código con tus propias palabras.
10. Prepara tu informe, tabla de funciones y defensa. El programa de ejemplo es un punto de partida; debes aportar la modificación, la predicción y el análisis.

## Prompt inicial para Copilot

> Actúa como tutor de Python. Estoy trabajando en el alumno 08, Arrastre de Clift-Gauvin en un gel. Lee ALUMNO_08.md y simulacion_08.py. Primero explícame la ecuación y los supuestos; pídeme una predicción. Después revisemos una función por vez: sus argumentos, formas de los arreglos, retorno y quién la llama. Ayúdame a realizar el reto sin cambiar silenciosamente el modelo. Distingue ecuaciones publicadas, reducciones docentes y datos simulados. Hazme preguntas antes de avanzar y comprueba los cambios.

## Mapa del código

| Función | Ubicación |
|---|---|
| `integrar_rk4` | [Línea 16](simulacion_08.py#L16) |
| `integrar_hasta_parada` | [Línea 30](simulacion_08.py#L30) |
| `arrastre_por_velocidad_cuadrada` | [Línea 61](simulacion_08.py#L61) |
| `calcular_modelo` | [Línea 71](simulacion_08.py#L71) |
| `verificar` | [Línea 79](simulacion_08.py#L79) |
| `comparar_escenarios` | [Línea 93](simulacion_08.py#L93) |
| `guardar_resultados` | [Línea 99](simulacion_08.py#L99) |
| `graficar_resultados` | [Línea 110](simulacion_08.py#L110) |
| `main` | [Línea 122](simulacion_08.py#L122) |

Para cada función prepara una fila con: propósito, entradas, unidades o escalas, forma del arreglo, salida, quién la llama y una prueba o comprobación. Explica la diferencia entre devolver un dato con `return`, imprimirlo y guardarlo en un archivo.

## Defensa individual

¿Por qué Cd no es constante? ¿Cómo evitas dividir por cero? ¿Qué evidencia faltaría para afirmar que tus parámetros representan un gel?

Además, el docente podrá elegir una función al azar y pedirte cambiar un parámetro antes de volver a ejecutar. Debes predecir el efecto y explicar cualquier diferencia con tu predicción.

## Entrega

- `mi_simulacion_08.py` y `requirements.txt`.
- Los tres CSV, los parámetros y la figura comparativa.
- Informe de 2 páginas: referencia y ubicación de la ecuación; supuestos; predicción; resultados; comprobación; límites.
- Tabla de funciones y registro breve de tres ayudas de Copilot, con lo que aceptaste, corregiste o verificaste.

No entregues `.venv` ni conversaciones personales completas. Fecha y plataforma: las define el docente.

[Volver a la distribución](README.md#distribución-sin-artículos-repetidos).
