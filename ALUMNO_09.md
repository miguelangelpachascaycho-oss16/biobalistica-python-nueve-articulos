# Alumno 09 · Contacto elástico, indentación y rebote

Nombre: __________________________

## Artículo individual

**Saifoori, Nezamabadi y Ghadiri (2024). Analysis of impact deformation of elastic-perfectly plastic particles.** Computational Particle Mechanics 11, 2629-2640. DOI: [10.1007/s40571-024-00742-x](https://link.springer.com/article/10.1007/s40571-024-00742-x).

[Lectura y versión disponible](https://link.springer.com/article/10.1007/s40571-024-00742-x). Artículo completo de acceso abierto. Se usa el submodelo elástico de verificación, no los resultados de grandes deformaciones plásticas.

**Dónde está el modelo:** Sección 2.2, Verification, ecuaciones (5)-(9).

## Modelo y alcance

F=(4/3) sqrt(R) E* δ^(3/2); m δ''=-F durante el contacto.

**Qué hace este ejemplo:** Se reproduce únicamente la referencia elástica de Hertz de la sección 2.2. Con δ=Lq, t=Ts: q''=-K max(q,0)^(3/2), q(0)=0, q'(0)=1, K=(4/3)sqrt(R)E*T²sqrt(L)/m. Se calcula indentación global y fuerza; no se ejecuta el MPM ni plasticidad del artículo. El contorno dibujado es esquemático, no un campo de deformación.

Los tres escenarios modifican únicamente `K`: A=0.5, B=1.0, C=2.0. Son escenarios de práctica, no condiciones experimentales recomendadas.

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
8. Desarrolla este reto: **Verificar q_max=(5/(4K))^(2/5), energía constante y restitución próxima a 1. Explicar por qué no hay deformación residual en este submodelo.** Guarda tu modificación como `mi_simulacion_09.py` para conservar el ejemplo original.
9. Trabaja con Copilot por etapas usando el prompt siguiente; después explica el código con tus propias palabras.
10. Prepara tu informe, tabla de funciones y defensa. El programa de ejemplo es un punto de partida; debes aportar la modificación, la predicción y el análisis.

## Prompt inicial para Copilot

> Actúa como tutor de Python. Estoy trabajando en el alumno 09, Contacto elástico, indentación y rebote. Lee ALUMNO_09.md y simulacion_09.py. Primero explícame la ecuación y los supuestos; pídeme una predicción. Después revisemos una función por vez: sus argumentos, formas de los arreglos, retorno y quién la llama. Ayúdame a realizar el reto sin cambiar silenciosamente el modelo. Distingue ecuaciones publicadas, reducciones docentes y datos simulados. Hazme preguntas antes de avanzar y comprueba los cambios.

## Mapa del código

| Función | Ubicación |
|---|---|
| `integrar_rk4` | [Línea 17](simulacion_09.py#L17) |
| `calcular_modelo` | [Línea 40](simulacion_09.py#L40) |
| `verificar` | [Línea 56](simulacion_09.py#L56) |
| `comparar_escenarios` | [Línea 68](simulacion_09.py#L68) |
| `guardar_resultados` | [Línea 74](simulacion_09.py#L74) |
| `graficar_resultados` | [Línea 85](simulacion_09.py#L85) |
| `main` | [Línea 97](simulacion_09.py#L97) |

Para cada función prepara una fila con: propósito, entradas, unidades o escalas, forma del arreglo, salida, quién la llama y una prueba o comprobación. Explica la diferencia entre devolver un dato con `return`, imprimirlo y guardarlo en un archivo.

## Defensa individual

¿Qué representa la indentación y en qué se diferencia de la deformación unitaria? ¿Qué partes de MPM y plasticidad has omitido?

Además, el docente podrá elegir una función al azar y pedirte cambiar un parámetro antes de volver a ejecutar. Debes predecir el efecto y explicar cualquier diferencia con tu predicción.

## Entrega

- `mi_simulacion_09.py` y `requirements.txt`, junto con el módulo compartido `animaciones.py`.
- Los tres CSV, los parámetros y la figura comparativa.
- Informe de 2 páginas: referencia y ubicación de la ecuación; supuestos; predicción; resultados; comprobación; límites.
- Tabla de funciones y registro breve de tres ayudas de Copilot, con lo que aceptaste, corregiste o verificaste.

No entregues `.venv` ni conversaciones personales completas. Fecha y plataforma: las define el docente.

[Volver a la distribución](README.md#distribución-sin-artículos-repetidos).

## Ver el movimiento y analizarlo

Ejecuta `python simulacion_09.py --escenario todos --verificar --animar`. Abre `resultados/alumno_09/visor.html` en el navegador: puedes pausar, arrastrar el tiempo y cambiar A/B/C. También se generan `animacion.gif` (escenario B si existe) y `metricas.json` con resultados de los tres escenarios. El tiempo de reproducción está ralentizado; las unidades del modelo son relativas.

Explica `preparar_serie`, `resumir_metricas` y `exportar_movimiento` en [animaciones.py](animaciones.py): convierten los estados calculados en posiciones, métricas y cuadros. La ecuación permanece en tu archivo individual. El tamaño dibujado de la esfera se amplifica para verla.

Entrega también el visor, el GIF y una tabla de métricas A/B/C. No deduzcas deformación del tejido a partir de una trayectoria: en 02/03/05/07/08 se calcula penetración; en 09, indentación y fuerza del contacto elástico; en 01/04/06 se calcula movimiento en el fluido y el impacto no está resuelto. El dibujo del contorno es esquemático y no proporciona tensiones ni deformaciones locales.

Conserva `animaciones.py` en la misma carpeta que tu programa. El integrador y las ecuaciones están en el archivo individual; el módulo compartido transforma sus resultados en gráficos y animaciones.
