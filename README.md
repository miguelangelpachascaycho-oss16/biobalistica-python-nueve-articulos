# Biobalística en células y tejidos: simulaciones en Python

> **Actividad en revisión. La selección anterior de nueve artículos de contacto general no cumple el requisito de biobalística celular o tisular. Sus animaciones no son réplicas de nueve modelos biológicos.**

La actividad prevista exige nueve artículos distintos, uno por alumno, y una simulación de cada modelo que calcule el impacto de micro/nanoesferas y la deformación del blanco. Incluye ecuaciones, funciones explicadas, comparación analítica cuando corresponda y defensa del código en Visual Studio Code con ayuda de GitHub Copilot.

**Estado actual: nueve candidatos bibliográficos, uno condicional; cero réplicas completas verificadas; un piloto reducido. La distribución definitiva para los nueve alumnos está pendiente.**

Consulta la [revisión de biobalística](REVISION_BIOBALISTICA.md) y el [registro de fuentes y pendientes](SELECCION_BIOBALISTICA.json). La tabla diferencia modelos confirmados, textos incompletos y el candidato que podría no satisfacer la deformación causada por impacto.


**Actualización de fuentes:** se obtuvo y revisó la tesis pública de Guha (2009), complementaria al artículo de 2010. Los otros textos siguen pendientes. Consulta [el informe de acceso](ACCESO_FUENTES.md).

## Primer piloto de deformación calculada

[Campello (2015), ejemplo 5.3](https://doi.org/10.1007/s40430-014-0273-5): bicapa lipídica representada por nodos con inercia, enlaces, contacto y arrastre. La animación proviene de las posiciones integradas de ambas capas. Es una **reducción didáctica 3D**, no una reproducción completa de los resultados publicados.

Lee [el paso a paso, ecuaciones, diferencias y explicación de funciones](PILOTO_MEMBRANA.md).

![Piloto reducido de bicapa lipídica](piloto_membrana.gif)

## Ejecutar el piloto en Visual Studio Code

Descarga **Code → Download ZIP**, extrae la carpeta y ábrela en VS Code. Instala Python y la extensión Python de Microsoft; elige el intérprete del entorno creado abajo. Copilot puede ayudar a estudiar el código y no es necesario para ejecutarlo.

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe piloto_membrana.py --animar
.\.venv\Scripts\python.exe verificar_piloto.py
```

Abre `resultados/piloto_membrana/piloto_membrana.gif`. El NPZ guarda estados; el CSV guarda desplazamiento máximo, altura de proyectiles y enlaces rotos; el JSON documenta parámetros. Las comprobaciones independientes están en `VERIFICACION_PILOTO.json`. Una comprobación numérica no valida el comportamiento de células reales.

## Material auxiliar anterior

Los archivos `simulacion_01.py`–`09.py`, sus fichas `ALUMNO_01.md`–`09.md`, los nueve GIF antiguos y `visor_simulaciones.html` corresponden a [fundamentos de contacto](FUNDAMENTOS_CONTACTO.md). Se conservan para estudiar mecánica y soluciones analíticas; **no son las nueve asignaciones biológicas solicitadas**. Su verificación es matemática y no demuestra correspondencia con modelos de tejidos o células.
