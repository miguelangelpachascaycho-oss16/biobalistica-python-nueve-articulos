# Alumno 09 — Yong y Du (2023)

**Artículo distinto:** *Effects of Shape on Interaction Dynamics of Tetrahedral Nanoplastics and the Cell Membrane*. [DOI 10.1021/acs.jpcb.2c07460](https://doi.org/10.1021/acs.jpcb.2c07460). [Lectura de texto completo](<https://par.nsf.gov/servlets/purl/10447218>). Acceso: Manuscrito público NSF PAR; versión abierta arXiv 2210.11555.

**Tipo:** Contacto y penetración de nanoplásticos; no pistola génica. **Blanco:** Bicapa DOPC H2E2(C5)2 y tetraedro rígido. Es una implementación docente reducida; las diferencias con el artículo se explican en [la guía del modelo](CASO_09.md).

## Paso a paso

1. Descarga **Code → Download ZIP** desde GitHub, extrae el archivo y abre la carpeta en Visual Studio Code.
2. Abre **Terminal → New Terminal** y ejecuta desde la raíz:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe ejecutar_caso.py 9 --animar
.\.venv\Scripts\python.exe verificar_nuevos.py
```

3. Selecciona `.venv` como intérprete en VS Code. Abre `caso_09_tetraedro.py` y el motor que indica la guía. Copilot ayuda a estudiar el código; no hace falta para ejecutarlo.
4. Consulta las salidas en `resultados/caso_09`. La [vista previa GIF](caso_09.gif) y [figura](caso_09.png) del repositorio son resultados pregenerados; el comando anterior genera tus propios archivos.
5. Abre el CSV de métricas y el JSON de parámetros de esa carpeta. Relaciona posiciones, contacto y deformación con un mismo instante. No concluyas daño celular solo por ver un cambio de forma.
6. Ejecuta el control y la comparación sugerida en [la guía](CASO_09.md). Distingue los valores publicados, las elecciones docentes y las variables que cambiaste.

## Trabajo analítico y explicación del código

Deduce la rotación libre del tetraedro y explica momento angular, tensor de inercia y deformación de la bicapa.

Para cada función explica entrada, unidades, retorno, forma de los arreglos y quién la llama. Señala dónde se calcula la fuerza sobre el blanco, dónde se aplica la reacción y dónde se actualizan las coordenadas. Explica cómo el dibujado utiliza esas coordenadas.

Pide a Copilot: «Lee mi guía y explícame una sola función cada vez. Pregúntame por signos, dimensiones y supuestos. Ayúdame a derivar el límite analítico antes de modificar el programa. No atribuyas al artículo un parámetro añadido por el ejercicio». Revisa el diff y registra una ayuda aceptada y una corrección razonada.

Entrega código comentado, derivación, parámetros, CSV, curvas, animación, control y una defensa oral. Las comprobaciones numéricas no validan el comportamiento de células reales ni convierten la reducción en una reproducción completa del artículo.
