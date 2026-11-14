# Alumno 02 — Campello y Zohdi (2014)

**Artículo distinto:** *Design Evaluation of a Particle Bombardment System Used to Deliver Substances into Cells*. [DOI 10.3970/cmes.2014.098.221](https://doi.org/10.3970/cmes.2014.098.221). [Lectura de texto completo](<https://cmmrl.berkeley.edu/zohdipaper/109.pdf>). Acceso: Copia pública de autor; licencia de reutilización no confirmada.

**Tipo:** Biobalística celular con variabilidad. **Blanco:** Célula idealizada DEM 2D. Es una implementación docente reducida; las diferencias con el artículo se explican en [la guía del modelo](CASOS_CELULARES.md).

## Paso a paso

1. Descarga **Code → Download ZIP** desde GitHub, extrae el archivo y abre la carpeta en Visual Studio Code.
2. Abre **Terminal → New Terminal** y ejecuta desde la raíz:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe ejecutar_caso.py 2 --animar
.\.venv\Scripts\python.exe verificar_celulas.py
```

3. Selecciona `.venv` como intérprete en VS Code. Abre `caso_celular_02.py` y el motor que indica la guía. Copilot ayuda a estudiar el código; no hace falta para ejecutarlo.
4. Consulta las salidas en `resultados/celular_02`. La [vista previa GIF](celula_02.gif) y [figura](celula_02.png) del repositorio son resultados pregenerados; el comando anterior genera tus propios archivos.
5. Abre el CSV de métricas y el JSON de parámetros de esa carpeta. Relaciona posiciones, contacto y deformación con un mismo instante. No concluyas daño celular solo por ver un cambio de forma.
6. Ejecuta el control y la comparación sugerida en [la guía](CASOS_CELULARES.md). Distingue los valores publicados, las elecciones docentes y las variables que cambiaste.

## Trabajo analítico y explicación del código

Explica cómo se generan tamaños y velocidades; compara muestras sin confundir tres ensayos con una inferencia estadística.

Para cada función explica entrada, unidades, retorno, forma de los arreglos y quién la llama. Señala dónde se calcula la fuerza sobre el blanco, dónde se aplica la reacción y dónde se actualizan las coordenadas. Explica cómo el dibujado utiliza esas coordenadas.

Pide a Copilot: «Lee mi guía y explícame una sola función cada vez. Pregúntame por signos, dimensiones y supuestos. Ayúdame a derivar el límite analítico antes de modificar el programa. No atribuyas al artículo un parámetro añadido por el ejercicio». Revisa el diff y registra una ayuda aceptada y una corrección razonada.

Entrega código comentado, derivación, parámetros, CSV, curvas, animación, control y una defensa oral. Las comprobaciones numéricas no validan el comportamiento de células reales ni convierten la reducción en una reproducción completa del artículo.
