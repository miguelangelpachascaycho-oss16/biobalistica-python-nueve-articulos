# Alumno 03 — Campello (2015)

**Artículo distinto:** *Computational modeling and simulation of rupture of membranes and thin films — solo ejemplo 5.3*. [DOI 10.1007/s40430-014-0273-5](https://doi.org/10.1007/s40430-014-0273-5). [Lectura de texto completo](<https://www.researchgate.net/publication/269096734_Computational_modeling_and_simulation_of_rupture_of_membranes_and_thin_films>). Acceso: Copia pública de autor; licencia de reutilización no confirmada.

**Tipo:** Biobalística de bicapa. **Blanco:** Bicapa lipídica idealizada DEM 3D. Es una implementación docente reducida; las diferencias con el artículo se explican en [la guía del modelo](PILOTO_MEMBRANA.md).

## Paso a paso

1. Descarga **Code → Download ZIP** desde GitHub, extrae el archivo y abre la carpeta en Visual Studio Code.
2. Abre **Terminal → New Terminal** y ejecuta desde la raíz:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe ejecutar_caso.py 3 --animar
.\.venv\Scripts\python.exe verificar_piloto.py
```

3. Selecciona `.venv` como intérprete en VS Code. Abre `piloto_membrana.py` y el motor que indica la guía. Copilot ayuda a estudiar el código; no hace falta para ejecutarlo.
4. Consulta las salidas en `resultados/piloto_membrana`. La [vista previa GIF](piloto_membrana.gif) y [figura](piloto_membrana.png) del repositorio son resultados pregenerados; el comando anterior genera tus propios archivos.
5. Abre el CSV de métricas y el JSON de parámetros de esa carpeta. Relaciona posiciones, contacto y deformación con un mismo instante. No concluyas daño celular solo por ver un cambio de forma.
6. Ejecuta el control y la comparación sugerida en [la guía](PILOTO_MEMBRANA.md). Distingue los valores publicados, las elecciones docentes y las variables que cambiaste.

## Trabajo analítico y explicación del código

Deriva el oscilador de un enlace y explica qué cambia cuando se desactiva una interacción por ruptura.

Para cada función explica entrada, unidades, retorno, forma de los arreglos y quién la llama. Señala dónde se calcula la fuerza sobre el blanco, dónde se aplica la reacción y dónde se actualizan las coordenadas. Explica cómo el dibujado utiliza esas coordenadas.

Pide a Copilot: «Lee mi guía y explícame una sola función cada vez. Pregúntame por signos, dimensiones y supuestos. Ayúdame a derivar el límite analítico antes de modificar el programa. No atribuyas al artículo un parámetro añadido por el ejercicio». Revisa el diff y registra una ayuda aceptada y una corrección razonada.

Entrega código comentado, derivación, parámetros, CSV, curvas, animación, control y una defensa oral. Las comprobaciones numéricas no validan el comportamiento de células reales ni convierten la reducción en una reproducción completa del artículo.
