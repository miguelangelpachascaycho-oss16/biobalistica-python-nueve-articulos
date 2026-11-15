# Biobalística y penetración mecánica: nueve simulaciones en Python

**Nueve actividades docentes, con nueve artículos distintos y una ficha por alumno.** Cada programa calcula el movimiento de partículas y la deformación del blanco. Los casos 06–09 corresponden a la ampliación autorizada a penetración mecánica: no se presentan como biobalística estricta; 06 y 07 usan membranas artificiales mínimas.

Son implementaciones reducidas para aprender a construir y explicar simulaciones, con supuestos y parámetros complementarios declarados. No son nueve reproducciones cuantitativas completas ni predicciones validadas de células reales. Las lecturas se enlazan en cada ficha: hay artículos CC BY y copias públicas de autor; las tres de Campello conservan una salvedad de licencia en [la revisión de fuentes](REVISION_BIOBALISTICA.md).

## Empieza aquí: actividad para alumnos

1. Abre **tu ficha [ALUMNO_01](ALUMNO_01.md), [02](ALUMNO_02.md), [03](ALUMNO_03.md), [04](ALUMNO_04.md), [05](ALUMNO_05.md), [06](ALUMNO_06.md), [07](ALUMNO_07.md), [08](ALUMNO_08.md) o [09](ALUMNO_09.md)**. Cada una contiene un artículo diferente, el paso a paso, el modelo, las funciones y lo que debes entregar.
2. Sigue la [instalación en VS Code](#abrir-y-ejecutar-en-visual-studio-code) y ejecuta `ejecutar_caso.py` con tu número. Por ejemplo, para el alumno 06: `python ejecutar_caso.py 6 --animar`, usando el intérprete del entorno instalado.
3. Explica las ecuaciones y cada función; compara un límite con su referencia analítica y analiza las curvas y la deformación calculada.

> **Ruta de la actividad actual: `ALUMNO_NN.md` → `ejecutar_caso.py N --animar`.** Los archivos `simulacion_NN.py`, `CONTACTO_AUX_NN.md`, `animacion_NN.gif` y `visor_simulaciones.html` son un archivo auxiliar de mecánica de contacto. Sus números no corresponden a las asignaciones actuales. Consulta ese material solo como apoyo adicional.

## Qué representa cada grupo

| Alumnos | Tema | Alcance del blanco |
|---|---|---|
| 01–04 | Biobalística | Célula idealizada, bicapa y tejido cutáneo; modelos reducidos |
| 05 | Colisión de nanopartícula con vesícula | Vesícula idealizada, ampliación a interacción de nanopartículas |
| 06–07 | Penetración mecánica | Membranas artificiales mínimas: hoja elástica y cadena dipolar; no son células ni bicapas moleculares |
| 08–09 | Penetración/interacción mecánica con bicapa | Modelos de lípidos y nanopartículas; no son disparos de un cañón de genes |

**Las nueve implementaciones son reducciones docentes de modelos publicados.** Cada guía declara qué ecuaciones usa, qué simplifica y qué parámetros añade. Una comparación analítica verifica un límite del modelo; no demuestra por sí sola que se hayan reproducido los experimentos o todas las figuras del artículo.

## Asignación y vistas previas

| Alumno | Artículo distinto | Blanco calculado | Guía y movimiento |
|---|---|---|---|
| [01](ALUMNO_01.md) | Campello y Zohdi (2014), [10.1002/cnm.2649](https://doi.org/10.1002/cnm.2649) | Célula idealizada DEM 2D | [Modelo y funciones](CASOS_CELULARES.md) · [GIF](celula_01.gif) |
| [02](ALUMNO_02.md) | Campello y Zohdi (2014), [10.3970/cmes.2014.098.221](https://doi.org/10.3970/cmes.2014.098.221) | Célula idealizada DEM 2D | [Modelo y funciones](CASOS_CELULARES.md) · [GIF](celula_02.gif) |
| [03](ALUMNO_03.md) | Campello (2015), [10.1007/s40430-014-0273-5](https://doi.org/10.1007/s40430-014-0273-5) | Bicapa lipídica idealizada DEM 3D | [Modelo y funciones](PILOTO_MEMBRANA.md) · [GIF](piloto_membrana.gif) |
| [04](ALUMNO_04.md) | Shen et al. (2025), [10.1016/j.taml.2024.100567](https://doi.org/10.1016/j.taml.2024.100567) | Piel hiperelástica, reducción FEM axisimétrica | [Modelo y funciones](PIEL_OGDEN.md) · [GIF](piel_ogden.gif) |
| [05](ALUMNO_05.md) | Arai, Yasuoka y Zeng (2013), [10.1039/C3NR02024J](https://doi.org/10.1039/C3NR02024J) | Vesícula HTTT y agua explícita DPD | [Modelo y funciones](VESICULA_DPD.md) · [GIF](vesicula_dpd.gif) |
| [06](ALUMNO_06.md) | Daddi-Moussa-Ider et al. (2019), [10.1088/1367-2630/ab35d2](https://doi.org/10.1088/1367-2630/ab35d2) | Membrana artificial mínima: hoja elástica | [Modelo y funciones](CASO_06.md) · [GIF](caso_06.gif) |
| [07](ALUMNO_07.md) | Daddi-Moussa-Ider et al. (2019), [10.1063/1.5080807](https://doi.org/10.1063/1.5080807) | Membrana artificial mínima: cadena dipolar | [Modelo y funciones](CASO_07.md) · [GIF](caso_07.gif) |
| [08](ALUMNO_08.md) | Zhang et al. (2015), [10.1038/srep10525](https://doi.org/10.1038/srep10525) | Bicapa H2T5, agua y dos NP rígidas | [Modelo y funciones](CASO_08.md) · [GIF](caso_08.gif) |
| [09](ALUMNO_09.md) | Yong y Du (2023), [10.1021/acs.jpcb.2c07460](https://doi.org/10.1021/acs.jpcb.2c07460) | Bicapa DOPC H2E2(C5)2 y tetraedro rígido | [Modelo y funciones](CASO_09.md) · [GIF](caso_09.gif) |

## Abrir y ejecutar en Visual Studio Code

Descarga **Code → Download ZIP**, extrae la carpeta y ábrela en VS Code. Desde **Terminal → New Terminal**, crea un entorno e instala las dependencias:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe ejecutar_caso.py --listar
.\.venv\Scripts\python.exe ejecutar_caso.py 6 --animar
```

Cambia `6` por tu número del 1 al 9. Selecciona `.venv` como intérprete de VS Code. La ficha `ALUMNO_NN.md` indica la carpeta de resultados, controles y verificador de cada caso. Copilot puede ayudar a estudiar el programa y no es necesario para ejecutarlo. Ejecuta un caso cada vez; los DPD y algunas animaciones pueden tardar varios minutos en una laptop.

Los CSV y JSON guardan métricas y parámetros; los NPZ conservan estados. El GIF representa las coordenadas calculadas. Las vistas de esta página están pregeneradas; al ejecutar se crean tus propios resultados en `resultados/`.

## Qué debe explicar el alumno

[Guía docente](GUIA_DOCENTE.md) · [Aprender a construir](APRENDE_A_CONSTRUIR.md) · [Funciones](EXPLICACION_FUNCIONES.md) · [Referencias analíticas](SOLUCIONES_ANALITICAS.md) · [Copilot](GUIA_COPILOT.md).

Cada entrega debe incluir diagrama de fuerzas, ecuaciones y unidades, código comentado, comparación analítica de un límite válido, control sin contacto o sin excitación, CSV, curvas, animación y defensa de las funciones. Debe distinguir deformación, desplazamiento rígido, ruido térmico, difusión y daño.

Las comprobaciones de los casos 06–09 se ejecutan con:

```powershell
.\.venv\Scripts\python.exe verificar_nuevos.py
```

Comprueban gradientes de energía, torque, acción/reacción, disipación, control en reposo, rotación libre y resorte móvil analítico. Los casos anteriores tienen verificadores específicos indicados en sus fichas. Estas pruebas son verificación matemática, no validación biológica ni reproducción de todas las figuras de los artículos.

## Material auxiliar preservado

`simulacion_01.py`–`simulacion_09.py`, `CONTACTO_AUX_NN.md`, `animacion_NN.gif` y `visor_simulaciones.html` pertenecen al anterior material de [fundamentos de contacto](FUNDAMENTOS_CONTACTO.md), junto con `motor_contacto.py`, `animaciones.py` y `verificar_todos.py`. **Las asignaciones actuales son las fichas ALUMNO y el lanzador `ejecutar_caso.py`.** El auxiliar no se cuenta como otros nueve artículos celulares. El PDF original del docente no se ha modificado.
