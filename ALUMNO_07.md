# Alumno 07 — Daddi-Moussa-Ider et al. (2019)

**Artículo distinto:** *Membrane penetration and trapping of an active particle*. [DOI 10.1063/1.5080807](https://doi.org/10.1063/1.5080807). [Lectura de texto completo](<https://arxiv.org/abs/1901.07359>). Acceso: Versión abierta en arXiv y copia pública de autores.

**Tipo:** Penetración mecánica activa; no balística. **Blanco:** Membrana artificial mínima: cadena dipolar. Es una implementación docente reducida; las diferencias con el artículo se explican en [la guía del modelo](CASO_07.md).

## Paso a paso

1. Descarga **Code → Download ZIP** desde GitHub, extrae el archivo y abre la carpeta en Visual Studio Code.
2. Abre **Terminal → New Terminal** y ejecuta desde la raíz:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe ejecutar_caso.py 7 --animar
.\.venv\Scripts\python.exe verificar_nuevos.py
```

3. Selecciona `.venv` como intérprete en VS Code. Abre `caso_07_dipolar.py` y el motor que indica la guía. Copilot ayuda a estudiar el código; no hace falta para ejecutarlo.
4. Consulta las salidas en `resultados/caso_07`. La [vista previa GIF](caso_07.gif) y [figura](caso_07.png) del repositorio son resultados pregenerados; el comando anterior genera tus propios archivos.
5. Abre el CSV de métricas y el JSON de parámetros de esa carpeta. Relaciona posiciones, contacto y deformación con un mismo instante. No concluyas daño celular solo por ver un cambio de forma.
6. Ejecuta el control y la comparación sugerida en [la guía](CASO_07.md). Distingue los valores publicados, las elecciones docentes y las variables que cambiaste.

## Trabajo analítico y explicación del código

Deduce el perfil triangular y explica los torques, la movilidad de Stokes y el límite de carga puntual.

Para cada función explica entrada, unidades, retorno, forma de los arreglos y quién la llama. Señala dónde se calcula la fuerza sobre el blanco, dónde se aplica la reacción y dónde se actualizan las coordenadas. Explica cómo el dibujado utiliza esas coordenadas.

Pide a Copilot: «Lee mi guía y explícame una sola función cada vez. Pregúntame por signos, dimensiones y supuestos. Ayúdame a derivar el límite analítico antes de modificar el programa. No atribuyas al artículo un parámetro añadido por el ejercicio». Revisa el diff y registra una ayuda aceptada y una corrección razonada.

Entrega código comentado, derivación, parámetros, CSV, curvas, animación, control y una defensa oral. Las comprobaciones numéricas no validan el comportamiento de células reales ni convierten la reducción en una reproducción completa del artículo.
