# Alumno 03 · Desaceleración y evento de parada

Nombre: __________________________

## Artículo individual

**Zhang et al. (2015). Microneedle assisted micro-particle delivery by gene guns: Mathematical model formulation and experimental verification.** Chemical Engineering Science 125, 176-190. DOI: [10.1016/j.ces.2014.06.031](https://doi.org/10.1016/j.ces.2014.06.031).

[Lectura y versión disponible](https://repository.lboro.ac.uk/articles/journal_contribution/9243128). Manuscrito aceptado de autores en Loughborough, CC BY-NC-ND 4.0.

**Dónde está el modelo:** Sección 2.1.3.2: ecuaciones (15)-(18); sección 2.2 sobre programación y eventos.

## Modelo y alcance

m dv/dt = -(a v + b v² + c), dx/dt=v, mientras v>0. Los coeficientes agrupan las tres fuerzas de las ecuaciones publicadas.

**Qué hace este ejemplo:** Una región 1D homogénea. Con s=t/T, w=v/Vref y z=x/(Vref T): dw/ds=-(A w+B w²+C), dz/ds=w; A=aT/m, B=bVrefT/m, C=cT/(mVref). B=0.2 y C=0.1 son docentes; se omiten las capas y huecos del modelo completo.

Los tres escenarios modifican únicamente `A`: A=0.5, B=1.0, C=2.0. Son escenarios de práctica, no condiciones experimentales recomendadas.

## Paso a paso

1. Completa la [preparación común](README.md#preparación-común-en-windows-y-visual-studio-code).
2. Abre [simulacion_03.py](simulacion_03.py) en VS Code. Identifica las constantes, la ecuación y `main()`.
3. Antes de ejecutar, escribe qué esperas que cambie entre A y C y por qué. Todavía no leas las gráficas de ejemplo.
4. Ejecuta solo A:

   ```powershell
   .\.venv\Scripts\python.exe simulacion_03.py --escenario A
   ```

5. Revisa `resultados/alumno_03/escenario_A.csv`, `parametros.json` y `comparacion.png`. Explica cada columna y cada eje.
6. Ejecuta los tres escenarios y sus comprobaciones:

   ```powershell
   .\.venv\Scripts\python.exe simulacion_03.py --escenario todos --verificar
   ```

7. Explica qué comprueba `verificar()` y por qué una comprobación numérica no demuestra validación biológica.
8. Desarrolla este reto: **Explicar el evento que termina la integración y refinar el paso. Comparar el tiempo y la distancia de parada con una cuadratura independiente en el dominio de la velocidad.** Guarda tu modificación como `mi_simulacion_03.py` para conservar el ejemplo original.
9. Trabaja con Copilot por etapas usando el prompt siguiente; después explica el código con tus propias palabras.
10. Prepara tu informe, tabla de funciones y defensa. El programa de ejemplo es un punto de partida; debes aportar la modificación, la predicción y el análisis.

## Prompt inicial para Copilot

> Actúa como tutor de Python. Estoy trabajando en el alumno 03, Desaceleración y evento de parada. Lee ALUMNO_03.md y simulacion_03.py. Primero explícame la ecuación y los supuestos; pídeme una predicción. Después revisemos una función por vez: sus argumentos, formas de los arreglos, retorno y quién la llama. Ayúdame a realizar el reto sin cambiar silenciosamente el modelo. Distingue ecuaciones publicadas, reducciones docentes y datos simulados. Hazme preguntas antes de avanzar y comprueba los cambios.

## Mapa del código

| Función | Ubicación |
|---|---|
| `integrar_rk4` | [Línea 16](simulacion_03.py#L16) |
| `integrar_hasta_parada` | [Línea 30](simulacion_03.py#L30) |
| `calcular_modelo` | [Línea 61](simulacion_03.py#L61) |
| `verificar` | [Línea 69](simulacion_03.py#L69) |
| `comparar_escenarios` | [Línea 84](simulacion_03.py#L84) |
| `guardar_resultados` | [Línea 90](simulacion_03.py#L90) |
| `graficar_resultados` | [Línea 101](simulacion_03.py#L101) |
| `main` | [Línea 113](simulacion_03.py#L113) |

Para cada función prepara una fila con: propósito, entradas, unidades o escalas, forma del arreglo, salida, quién la llama y una prueba o comprobación. Explica la diferencia entre devolver un dato con `return`, imprimirlo y guardarlo en un archivo.

## Defensa individual

¿Por qué no basta integrar hasta un tiempo fijo? ¿Qué error cometerías si permitieras velocidades negativas después de la parada?

Además, el docente podrá elegir una función al azar y pedirte cambiar un parámetro antes de volver a ejecutar. Debes predecir el efecto y explicar cualquier diferencia con tu predicción.

## Entrega

- `mi_simulacion_03.py` y `requirements.txt`.
- Los tres CSV, los parámetros y la figura comparativa.
- Informe de 2 páginas: referencia y ubicación de la ecuación; supuestos; predicción; resultados; comprobación; límites.
- Tabla de funciones y registro breve de tres ayudas de Copilot, con lo que aceptaste, corregiste o verificaste.

No entregues `.venv` ni conversaciones personales completas. Fecha y plataforma: las define el docente.

[Volver a la distribución](README.md#distribución-sin-artículos-repetidos).
