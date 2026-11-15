# Alumno 08 — Zhang et al. (2015)

**Artículo distinto:** *Cooperative Transmembrane Penetration of Nanoparticles*. [DOI 10.1038/srep10525](https://doi.org/10.1038/srep10525). [Lectura de texto completo](<https://www.nature.com/articles/srep10525>). Acceso: CC BY 4.0.

**Tipo:** Penetración mecánica guiada; no balística. **Blanco:** Bicapa H2T5, agua y dos NP rígidas. Es una implementación docente reducida; las diferencias con el artículo se explican en [la guía del modelo](../../docs/modelos/CASO_08.md).

## Paso a paso

1. Descarga **Code → Download ZIP** desde GitHub, extrae el archivo y abre la carpeta en Visual Studio Code.
2. Abre **Terminal → New Terminal** y ejecuta desde la raíz:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe ejecutar_caso.py 8 --animar
.\.venv\Scripts\python.exe pruebas/verificar_nuevos.py
```

3. Selecciona `.venv` como intérprete en VS Code. Abre `src/caso_08_cooperativa.py` y el motor que indica la guía. Copilot ayuda a estudiar el código; no hace falta para ejecutarlo.
4. Consulta las salidas en `resultados/caso_08`. La [vista previa GIF](animacion.gif) y [figura](figura.png) del repositorio son resultados pregenerados; el comando anterior genera tus propios archivos.
5. Abre el CSV de métricas y el JSON de parámetros de esa carpeta. Relaciona posiciones, contacto y deformación con un mismo instante. No concluyas daño celular solo por ver un cambio de forma.
6. Ejecuta el control y la comparación sugerida en [la guía](../../docs/modelos/CASO_08.md). Distingue los valores publicados, las elecciones docentes y las variables que cambiaste.

## Trabajo analítico y explicación del código

Deduce la respuesta de la NP al resorte móvil y compara una/dos partículas con sus controles.

Para cada función explica entrada, unidades, retorno, forma de los arreglos y quién la llama. Señala dónde se calcula la fuerza sobre el blanco, dónde se aplica la reacción y dónde se actualizan las coordenadas. Explica cómo el dibujado utiliza esas coordenadas.

Pide a Copilot: «Lee mi guía y explícame una sola función cada vez. Pregúntame por signos, dimensiones y supuestos. Ayúdame a derivar el límite analítico antes de modificar el programa. No atribuyas al artículo un parámetro añadido por el ejercicio». Revisa el diff y registra una ayuda aceptada y una corrección razonada.

Entrega código comentado, derivación, parámetros, CSV, curvas, animación, control y una defensa oral. Las comprobaciones numéricas no validan el comportamiento de células reales ni convierten la reducción en una reproducción completa del artículo.

## Qué observar en la animación

Dos nanopartículas guiadas por resortes móviles contactan la bicapa. La curva incluye fluctuación térmica y se compara con el control.

![Animación calculada](animacion.gif)
