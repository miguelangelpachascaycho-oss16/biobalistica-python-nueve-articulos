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
| `integrar_rk4` | [Línea 17](simulacion_08.py#L17) |
| `integrar_hasta_parada` | [Línea 31](simulacion_08.py#L31) |
| `arrastre_por_velocidad_cuadrada` | [Línea 62](simulacion_08.py#L62) |
| `calcular_modelo` | [Línea 72](simulacion_08.py#L72) |
| `verificar` | [Línea 80](simulacion_08.py#L80) |
| `comparar_escenarios` | [Línea 94](simulacion_08.py#L94) |
| `guardar_resultados` | [Línea 100](simulacion_08.py#L100) |
| `graficar_resultados` | [Línea 111](simulacion_08.py#L111) |
| `main` | [Línea 123](simulacion_08.py#L123) |

Para cada función prepara una fila con: propósito, entradas, unidades o escalas, forma del arreglo, salida, quién la llama y una prueba o comprobación. Explica la diferencia entre devolver un dato con `return`, imprimirlo y guardarlo en un archivo.

## Defensa individual

¿Por qué Cd no es constante? ¿Cómo evitas dividir por cero? ¿Qué evidencia faltaría para afirmar que tus parámetros representan un gel?

Además, el docente podrá elegir una función al azar y pedirte cambiar un parámetro antes de volver a ejecutar. Debes predecir el efecto y explicar cualquier diferencia con tu predicción.

## Entrega

- `mi_simulacion_08.py` y `requirements.txt`, junto con el módulo compartido `animaciones.py`.
- Los tres CSV, los parámetros y la figura comparativa.
- Informe de 2 páginas: referencia y ubicación de la ecuación; supuestos; predicción; resultados; comprobación; límites.
- Tabla de funciones y registro breve de tres ayudas de Copilot, con lo que aceptaste, corregiste o verificaste.

No entregues `.venv` ni conversaciones personales completas. Fecha y plataforma: las define el docente.

[Volver a la distribución](README.md#distribución-sin-artículos-repetidos).

## Ver el movimiento y analizarlo

Ejecuta `python simulacion_08.py --escenario todos --verificar --animar`. Abre `resultados/alumno_08/visor.html` en el navegador: puedes pausar, arrastrar el tiempo y cambiar A/B/C. También se generan `animacion.gif` (escenario B si existe) y `metricas.json` con resultados de los tres escenarios. El tiempo de reproducción está ralentizado; las unidades del modelo son relativas.

Explica `preparar_serie`, `resumir_metricas` y `exportar_movimiento` en [animaciones.py](animaciones.py): convierten los estados calculados en posiciones, métricas y cuadros. La ecuación permanece en tu archivo individual. El tamaño dibujado de la esfera se amplifica para verla.

Entrega también el visor, el GIF y una tabla de métricas A/B/C. No deduzcas deformación del tejido a partir de una trayectoria: en 02/03/05/07/08 se calcula penetración; en 09, indentación y fuerza del contacto elástico; en 01/04/06 se calcula movimiento en el fluido y el impacto no está resuelto. El dibujo del contorno es esquemático y no proporciona tensiones ni deformaciones locales.

Conserva `animaciones.py` en la misma carpeta que tu programa. El integrador y las ecuaciones están en el archivo individual; el módulo compartido transforma sus resultados en gráficos y animaciones.
