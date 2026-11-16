# Biobalística y penetración mecánica en Python

## Actividades asignadas

**Busca tu nombre y abre «Tu ficha».** Allí encontrarás el artículo, las ecuaciones, el paso a paso, el programa, sus funciones y el trabajo que debes implementar con ayuda de Copilot.

**[Empezar: instalar y trabajar en VS Code con Copilot](docs/INICIO_VSCODE_COPILOT.md)** · [Ver las animaciones](GALERIA.md)

| Estudiante | Caso | Simulación | Paso a paso |
|---|---|---|---|
| Flor Angelita Mendoza García | 09 | Bicapa DOPC H2E2(C5)2 y tetraedro rígido | [Tu ficha](casos/09_flor_angelita_mendoza_garcia/README.md) |
| Nayeli Mishel Albarrán Chávez | 08 | Bicapa H2T5, agua y dos NP rígidas | [Tu ficha](casos/08_nayeli_mishel_albarran_chavez/README.md) |
| Gerwins Branco Díaz Delgado | 05 | Vesícula HTTT y agua explícita DPD | [Tu ficha](casos/05_gerwins_branco_diaz_delgado/README.md) |
| Dafne Luana Vilcarromero Santillán | 04 | Piel hiperelástica, reducción FEM axisimétrica | [Tu ficha](casos/04_dafne_luana_vilcarromero_santillan/README.md) |
| Heily Amelith Huamán Rojas | 03 | Bicapa lipídica idealizada DEM 3D | [Tu ficha](casos/03_heily_amelith_huaman_rojas/README.md) |
| Daria Danae Flores Rodrigo | 02 | Célula idealizada DEM 2D | [Tu ficha](casos/02_daria_danae_flores_rodrigo/README.md) |
| Víctor Ronaldo Zuta Rodríguez | 06 | Membrana artificial mínima: hoja elástica | [Tu ficha](casos/06_victor_ronaldo_zuta_rodriguez/README.md) |
| Alisson Xiomara Torres Chappa | 01 | Célula idealizada DEM 2D | [Tu ficha](casos/01_alisson_xiomara_torres_chappa/README.md) |

El [caso 07 — membrana dipolar](casos/07_reserva_docente_membrana_dipolar/README.md) queda como reserva docente, sin estudiante asignado. Hay **ocho asignaciones individuales y nueve artículos distintos disponibles**. Cada carpeta de `casos/` lleva el nombre de su estudiante.

## Artículos y vistas previas

| Caso | Artículo | Blanco del modelo | Animación |
|---|---|---|---|
| [01](casos/01_alisson_xiomara_torres_chappa/README.md) | Campello y Zohdi (2014) | Célula idealizada DEM 2D | [GIF](casos/01_alisson_xiomara_torres_chappa/animacion.gif) |
| [02](casos/02_daria_danae_flores_rodrigo/README.md) | Campello y Zohdi (2014) | Célula idealizada DEM 2D | [GIF](casos/02_daria_danae_flores_rodrigo/animacion.gif) |
| [03](casos/03_heily_amelith_huaman_rojas/README.md) | Campello (2015) | Bicapa lipídica idealizada DEM 3D | [GIF](casos/03_heily_amelith_huaman_rojas/animacion.gif) |
| [04](casos/04_dafne_luana_vilcarromero_santillan/README.md) | Shen et al. (2025) | Piel hiperelástica, reducción FEM axisimétrica | [GIF](casos/04_dafne_luana_vilcarromero_santillan/animacion.gif) |
| [05](casos/05_gerwins_branco_diaz_delgado/README.md) | Arai, Yasuoka y Zeng (2013) | Vesícula HTTT y agua explícita DPD | [GIF](casos/05_gerwins_branco_diaz_delgado/animacion.gif) |
| [06](casos/06_victor_ronaldo_zuta_rodriguez/README.md) | Daddi-Moussa-Ider et al. (2019) | Membrana artificial mínima: hoja elástica | [GIF](casos/06_victor_ronaldo_zuta_rodriguez/animacion.gif) |
| [07](casos/07_reserva_docente_membrana_dipolar/README.md) | Daddi-Moussa-Ider et al. (2019) | Membrana artificial mínima: cadena dipolar | [GIF](casos/07_reserva_docente_membrana_dipolar/animacion.gif) |
| [08](casos/08_nayeli_mishel_albarran_chavez/README.md) | Zhang et al. (2015) | Bicapa H2T5, agua y dos NP rígidas | [GIF](casos/08_nayeli_mishel_albarran_chavez/animacion.gif) |
| [09](casos/09_flor_angelita_mendoza_garcia/README.md) | Yong y Du (2023) | Bicapa DOPC H2E2(C5)2 y tetraedro rígido | [GIF](casos/09_flor_angelita_mendoza_garcia/animacion.gif) |

## Ejecutar la referencia en Visual Studio Code

Descarga **Code → Download ZIP**, extrae el archivo y abre la carpeta completa en VS Code. Desde **Terminal → New Terminal**, ejecuta en la raíz:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe ejecutar_caso.py --listar
.\.venv\Scripts\python.exe ejecutar_caso.py 1 --animar
```

Cambia `1` por el número del caso que figura junto a tu nombre y selecciona `.venv` como intérprete. Si `py` no está disponible, utiliza `python -m venv .venv`. Ejecuta un caso cada vez. Tu ficha indica la salida en `resultados/`, el verificador, los controles y las tareas analíticas. La instalación de dependencias requiere Internet; el cálculo se ejecuta sin Copilot ni claves de IA.

## Cómo está organizado

```text
casos/       Carpetas con nombre: ficha, GIF, figura y ejemplo/
src/         Programas de simulación y motores físicos compartidos
docs/        Guías, funciones, referencias analíticas y fuentes
pruebas/     Verificadores matemáticos y evidencia de las ejecuciones
resultados/  Tus propias salidas al ejecutar; no se suben al repositorio
```

En [cada ficha](casos/) se explica qué programa de `src/` estudiar y qué realiza cada función. [Copilot como tutor](docs/GUIA_COPILOT.md) y [cómo construir el modelo](docs/APRENDE_A_CONSTRUIR.md) acompañan la práctica. Las pruebas se ejecutan con los comandos de [pruebas/README.md](pruebas/README.md).

## Alcance científico

01–04: biobalística en células, bicapa o tejido idealizados. 05: colisión con una vesícula. 06–07: penetración activa en membranas artificiales mínimas; no son células ni bicapas moleculares. 08–09: interacción mecánica de nanopartículas con bicapas; no son disparos de un cañón de genes.

**Son implementaciones docentes reducidas**, con supuestos y elecciones complementarias declarados en cada guía. No constituyen nueve reproducciones cuantitativas completas ni predicciones biológicas validadas. El caso 04 muestra únicamente el impacto temprano; en 06–07 hay empuje activo, y en 08 el movimiento es guiado. Los GIF conservan las coordenadas y escalas calculadas. Consulta [fuentes, acceso y límites](docs/FUENTES_Y_ALCANCE.md): hay artículos CC BY y copias públicas de autor; la licencia de reutilización de las tres copias de Campello no está confirmada.

Los anteriores ejercicios genéricos de contacto y los documentos de búsqueda históricos se retiraron de la versión para alumnos. El historial de Git conserva la versión previa. El PDF original del docente se mantiene intacto.
