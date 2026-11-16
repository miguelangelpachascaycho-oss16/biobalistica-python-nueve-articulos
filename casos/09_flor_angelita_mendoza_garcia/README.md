# Caso 09 — Flor Angelita Mendoza García

**Tu actividad asignada.** [Instalación y tutoría con Copilot](../../docs/INICIO_VSCODE_COPILOT.md) · [Volver a la lista del grupo](../../README.md#actividades-asignadas).


**Artículo distinto:** *Effects of Shape on Interaction Dynamics of Tetrahedral Nanoplastics and the Cell Membrane*. [DOI 10.1021/acs.jpcb.2c07460](https://doi.org/10.1021/acs.jpcb.2c07460). [Lectura de texto completo](<https://par.nsf.gov/servlets/purl/10447218>). Acceso: Manuscrito público NSF PAR; versión abierta arXiv 2210.11555.

**Tipo:** Contacto y penetración de nanoplásticos; no pistola génica. **Blanco:** Bicapa DOPC H2E2(C5)2 y tetraedro rígido. Es una implementación docente reducida; las diferencias con el artículo se explican en [la guía del modelo](../../docs/modelos/CASO_09.md).

## Paso a paso en Visual Studio Code

1. Descarga **Code → Download ZIP** desde GitHub, extrae el archivo y abre la carpeta en Visual Studio Code.
2. Abre **Terminal → New Terminal** y ejecuta desde la raíz:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe ejecutar_caso.py 9 --animar
.\.venv\Scripts\python.exe pruebas/verificar_nuevos.py
```

3. Selecciona `.venv` como intérprete en VS Code. Abre `src/caso_09_tetraedro.py` y el motor que indica la guía. Copilot ayuda a estudiar el código; no hace falta para ejecutarlo.
4. Consulta las salidas en `resultados/caso_09`. La [vista previa GIF](animacion.gif) y [figura](figura.png) del repositorio son resultados pregenerados; el comando anterior genera tus propios archivos.
5. Abre el CSV de métricas y el JSON de parámetros de esa carpeta. Relaciona posiciones, contacto y deformación con un mismo instante. No concluyas daño celular solo por ver un cambio de forma.
6. Ejecuta el control y la comparación sugerida en [la guía](../../docs/modelos/CASO_09.md). Distingue los valores publicados, las elecciones docentes y las variables que cambiaste.

## Trabajo analítico y explicación del código

Deduce la rotación libre del tetraedro y explica momento angular, tensor de inercia y deformación de la bicapa.

Para cada función explica entrada, unidades, retorno, forma de los arreglos y quién la llama. Señala dónde se calcula la fuerza sobre el blanco, dónde se aplica la reacción y dónde se actualizan las coordenadas. Explica cómo el dibujado utiliza esas coordenadas.

Pide a Copilot: «Lee mi guía y explícame una sola función cada vez. Pregúntame por signos, dimensiones y supuestos. Ayúdame a derivar el límite analítico antes de modificar el programa. No atribuyas al artículo un parámetro añadido por el ejercicio». Revisa el diff y registra una ayuda aceptada y una corrección razonada.

Entrega código comentado, derivación, parámetros, CSV, curvas, animación, control y una defensa oral. Las comprobaciones numéricas no validan el comportamiento de células reales ni convierten la reducción en una reproducción completa del artículo.

## Construir tu implementación con ayuda de Copilot

1. Abre `src/caso_09_tetraedro.py` desde la raíz del proyecto y sigue los imports hasta el motor indicado en [la guía del modelo](../../docs/modelos/CASO_09.md). Dibuja el recorrido configuración → geometría → fuerzas → integrador → medición → animación.
2. Antes de modificar código, deduce el límite analítico descrito en esta ficha. Comprueba un valor a mano y anota sus unidades.
3. Usa **File → Save As** para guardar una copia del programa principal como `src/mi_caso_09.py`, dentro de `src/`. Los motores compartidos deben conservarse. Este archivo será tu versión de trabajo.
4. En el chat de Copilot, añade como contexto el programa y su motor. Pide: «Estudio el caso 09. Explica una función por vez; hazme identificar entradas, unidades, retorno y quién la llama. Después ayúdame a escribir una función pequeña de comprobación analítica. No cambies las ecuaciones del artículo».
5. Implementa la comprobación, explica cada línea y ejecútala. Para generar resultados con tu copia:

```powershell
.\.venv\Scripts\python.exe src/mi_caso_09.py --salida resultados/mi_caso_09 --animar
```

6. Compara los CSV y las curvas con la referencia. Aplica la comparación o control de la guía, cambia una sola cosa por ensayo y guarda cada ejecución en otra carpeta. Distingue el paso temporal del número de cuadros del GIF.
7. Pon un punto de interrupción en una función de fuerza, inicia la depuración de tu copia en VS Code y observa una entrada y su retorno. No ejecutes todo el modelo paso a paso: inspecciona una llamada y explica lo que contiene.
8. Registra una ayuda aceptada y una corrección que hiciste a Copilot. La defensa incluye explicar sin asistencia una función de fuerzas, una de integración y una de medición o dibujo.

**Comprobación antes de entregar:** ejecución propia sin errores; parámetros y unidades; derivación analítica con hipótesis; control; CSV y curvas; GIF generado desde los mismos estados; mapa de funciones y explicación oral. Revisa también [la guía de construcción](../../docs/APRENDE_A_CONSTRUIR.md).

## Qué observar en la animación

Contacto temprano de un tetraedro con una bicapa DOPC, con traslación y rotación. La rugosidad se compara con el control; no es un cañón de genes.

![Animación calculada](animacion.gif)
