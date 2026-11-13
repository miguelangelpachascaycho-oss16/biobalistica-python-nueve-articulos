# Alumno 02 · Trabajo del gas y velocidad normalizada

Nombre: __________________________

## Artículo individual

**Zhang, Rielly y Das (2015). Microneedle-assisted microparticle delivery by gene guns: experiments and modeling on the effects of particle characteristics.** Drug Delivery 22(3), 335-350; publicación en línea en 2014. DOI: [10.3109/10717544.2014.887158](https://doi.org/10.3109/10717544.2014.887158).

[Lectura y versión disponible](https://repository.lboro.ac.uk/articles/journal_contribution/9243026). Manuscrito aceptado de autores en Loughborough, CC BY-NC-ND 4.0. Enlace editorial separado.

**Dónde está el modelo:** Sección 2.4.1, Acceleration stage, ecuaciones (1)-(4) del manuscrito aceptado.

## Modelo y alcance

P1 V1^γ = P2(V1+V2)^γ; E=∫P2 dV2; E=M u²/2.

**Qué hace este ejemplo:** Cambio de variables: s=V2/V1, Π=P2/P1, J=E/(P1V1), U=u/sqrt(2P1V1/M). Entonces Π=(1+s)^(-γ), J=∫Π ds y U=sqrt(J). Los valores de práctica no son ajustes del equipo.

Los tres escenarios modifican únicamente `gamma`: A=1.2, B=1.4, C=1.6. Son escenarios de práctica, no condiciones experimentales recomendadas.

## Paso a paso

1. Completa la [preparación común](README.md#preparación-común-en-windows-y-visual-studio-code).
2. Abre [simulacion_02.py](simulacion_02.py) en VS Code. Identifica las constantes, la ecuación y `main()`.
3. Antes de ejecutar, escribe qué esperas que cambie entre A y C y por qué. Todavía no leas las gráficas de ejemplo.
4. Ejecuta solo A:

   ```powershell
   .\.venv\Scripts\python.exe simulacion_02.py --escenario A
   ```

5. Revisa `resultados/alumno_02/escenario_A.csv`, `parametros.json` y `comparacion.png`. Explica cada columna y cada eje.
6. Ejecuta los tres escenarios y sus comprobaciones:

   ```powershell
   .\.venv\Scripts\python.exe simulacion_02.py --escenario todos --verificar
   ```

7. Explica qué comprueba `verificar()` y por qué una comprobación numérica no demuestra validación biológica.
8. Desarrolla este reto: **Repetir el cálculo con una malla más gruesa y explicar el error de integración. Añadir una gráfica de Π(s) sin mezclar presión, trabajo y velocidad en un mismo eje.** Guarda tu modificación como `mi_simulacion_02.py` para conservar el ejemplo original.
9. Trabaja con Copilot por etapas usando el prompt siguiente; después explica el código con tus propias palabras.
10. Prepara tu informe, tabla de funciones y defensa. El programa de ejemplo es un punto de partida; debes aportar la modificación, la predicción y el análisis.

## Prompt inicial para Copilot

> Actúa como tutor de Python. Estoy trabajando en el alumno 02, Trabajo del gas y velocidad normalizada. Lee ALUMNO_02.md y simulacion_02.py. Primero explícame la ecuación y los supuestos; pídeme una predicción. Después revisemos una función por vez: sus argumentos, formas de los arreglos, retorno y quién la llama. Ayúdame a realizar el reto sin cambiar silenciosamente el modelo. Distingue ecuaciones publicadas, reducciones docentes y datos simulados. Hazme preguntas antes de avanzar y comprueba los cambios.

## Mapa del código

| Función | Ubicación |
|---|---|
| `calcular_modelo` | [Línea 25](simulacion_02.py#L25) |
| `verificar` | [Línea 36](simulacion_02.py#L36) |
| `comparar_escenarios` | [Línea 47](simulacion_02.py#L47) |
| `guardar_resultados` | [Línea 53](simulacion_02.py#L53) |
| `graficar_resultados` | [Línea 64](simulacion_02.py#L64) |
| `main` | [Línea 76](simulacion_02.py#L76) |

Para cada función prepara una fila con: propósito, entradas, unidades o escalas, forma del arreglo, salida, quién la llama y una prueba o comprobación. Explica la diferencia entre devolver un dato con `return`, imprimirlo y guardarlo en un archivo.

## Defensa individual

¿Qué integra la función? ¿Por qué la velocidad tiene una raíz cuadrada? ¿Qué cambia cuando γ se aproxima a 1?

Además, el docente podrá elegir una función al azar y pedirte cambiar un parámetro antes de volver a ejecutar. Debes predecir el efecto y explicar cualquier diferencia con tu predicción.

## Entrega

- `mi_simulacion_02.py` y `requirements.txt`.
- Los tres CSV, los parámetros y la figura comparativa.
- Informe de 2 páginas: referencia y ubicación de la ecuación; supuestos; predicción; resultados; comprobación; límites.
- Tabla de funciones y registro breve de tres ayudas de Copilot, con lo que aceptaste, corregiste o verificaste.

No entregues `.venv` ni conversaciones personales completas. Fecha y plataforma: las define el docente.

[Volver a la distribución](README.md#distribución-sin-artículos-repetidos).
