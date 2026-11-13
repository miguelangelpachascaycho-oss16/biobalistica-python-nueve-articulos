# Alumno 05 · Penetración de una microesfera en gel

Nombre: __________________________

## Artículo individual

**Veysset et al. (2018). High-velocity micro-particle impact on gelatin and synthetic hydrogel.** Journal of the Mechanical Behavior of Biomedical Materials 86, 71-76. DOI: [10.1016/j.jmbbm.2018.06.016](https://doi.org/10.1016/j.jmbbm.2018.06.016).

[Lectura y versión disponible](https://specialised-imaging.com/wp-content/uploads/2025/02/SI_RA__Veysset_et_al._-_2018_-_High-velocity_micro-particle_impact_on_gelatin_and_synthetic_hydrogel-1.pdf). PDF completo enlazado desde el fabricante de la cámara utilizada en el estudio; conserva derechos editoriales. No se redistribuye el PDF.

**Dónde está el modelo:** Sección 2.3, Poncelet model for particle penetration, ecuación (1).

## Modelo y alcance

F=B2 v²+B0; m dv/dt=-F; dx/dt=v.

**Qué hace este ejemplo:** Forma adimensional w'=-(w²+Y), z'=w, hasta w=0, con w(0)=1. Se varía la resistencia constante Y. No se reproduce la retracción tardía ni la cavidad observada en los experimentos.

Los tres escenarios modifican únicamente `Y`: A=0.2, B=0.5, C=1.0. Son escenarios de práctica, no condiciones experimentales recomendadas.

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
8. Desarrolla este reto: **Comprobar z_final=0.5 ln(1+1/Y) y s_final=atan(1/sqrt(Y))/sqrt(Y). Explicar por qué el modelo termina en la máxima penetración.** Guarda tu modificación como `mi_simulacion_05.py` para conservar el ejemplo original.
9. Trabaja con Copilot por etapas usando el prompt siguiente; después explica el código con tus propias palabras.
10. Prepara tu informe, tabla de funciones y defensa. El programa de ejemplo es un punto de partida; debes aportar la modificación, la predicción y el análisis.

## Prompt inicial para Copilot

> Actúa como tutor de Python. Estoy trabajando en el alumno 05, Penetración de una microesfera en gel. Lee ALUMNO_05.md y simulacion_05.py. Primero explícame la ecuación y los supuestos; pídeme una predicción. Después revisemos una función por vez: sus argumentos, formas de los arreglos, retorno y quién la llama. Ayúdame a realizar el reto sin cambiar silenciosamente el modelo. Distingue ecuaciones publicadas, reducciones docentes y datos simulados. Hazme preguntas antes de avanzar y comprueba los cambios.

## Mapa del código

| Función | Ubicación |
|---|---|
| `integrar_rk4` | [Línea 17](simulacion_05.py#L17) |
| `integrar_hasta_parada` | [Línea 31](simulacion_05.py#L31) |
| `calcular_modelo` | [Línea 62](simulacion_05.py#L62) |
| `verificar` | [Línea 67](simulacion_05.py#L67) |
| `comparar_escenarios` | [Línea 78](simulacion_05.py#L78) |
| `guardar_resultados` | [Línea 84](simulacion_05.py#L84) |
| `graficar_resultados` | [Línea 95](simulacion_05.py#L95) |
| `main` | [Línea 107](simulacion_05.py#L107) |

Para cada función prepara una fila con: propósito, entradas, unidades o escalas, forma del arreglo, salida, quién la llama y una prueba o comprobación. Explica la diferencia entre devolver un dato con `return`, imprimirlo y guardarlo en un archivo.

## Defensa individual

¿Qué fuerzas resume Poncelet? ¿Qué puedes medir en la animación y qué requeriría un modelo continuo del gel?

Además, el docente podrá elegir una función al azar y pedirte cambiar un parámetro antes de volver a ejecutar. Debes predecir el efecto y explicar cualquier diferencia con tu predicción.

## Entrega

- `mi_simulacion_05.py` y `requirements.txt`, junto con el módulo compartido `animaciones.py`.
- Los tres CSV, los parámetros y la figura comparativa.
- Informe de 2 páginas: referencia y ubicación de la ecuación; supuestos; predicción; resultados; comprobación; límites.
- Tabla de funciones y registro breve de tres ayudas de Copilot, con lo que aceptaste, corregiste o verificaste.

No entregues `.venv` ni conversaciones personales completas. Fecha y plataforma: las define el docente.

[Volver a la distribución](README.md#distribución-sin-artículos-repetidos).

## Ver el movimiento y analizarlo

Ejecuta `python simulacion_05.py --escenario todos --verificar --animar`. Abre `resultados/alumno_05/visor.html` en el navegador: puedes pausar, arrastrar el tiempo y cambiar A/B/C. También se generan `animacion.gif` (escenario B si existe) y `metricas.json` con resultados de los tres escenarios. El tiempo de reproducción está ralentizado; las unidades del modelo son relativas.

Explica `preparar_serie`, `resumir_metricas` y `exportar_movimiento` en [animaciones.py](animaciones.py): convierten los estados calculados en posiciones, métricas y cuadros. La ecuación permanece en tu archivo individual. El tamaño dibujado de la esfera se amplifica para verla.

Entrega también el visor, el GIF y una tabla de métricas A/B/C. No deduzcas deformación del tejido a partir de una trayectoria: en 02/03/05/07/08 se calcula penetración; en 09, indentación y fuerza del contacto elástico; en 01/04/06 se calcula movimiento en el fluido y el impacto no está resuelto. El dibujo del contorno es esquemático y no proporciona tensiones ni deformaciones locales.

Conserva `animaciones.py` en la misma carpeta que tu programa. El integrador y las ecuaciones están en el archivo individual; el módulo compartido transforma sus resultados en gráficos y animaciones.
