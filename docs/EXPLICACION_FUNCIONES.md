# Estructura y funciones de las nueve actividades

El lanzador `ejecutar_caso.py` no calcula fuerzas. Su `main()` lee `docs/ACTIVIDADES.json`, selecciona un programa y lo ejecuta con el mismo intérprete Python. Los argumentos adicionales llegan al programa científico. Así, `ejecutar_caso.py 9 --animar` ejecuta `src/caso_09_tetraedro.py --animar`.

| Alumnos | Programa o motor | Explicación de funciones |
|---|---|---|
| 01–02 | `src/caso_celular_01.py`, `src/caso_celular_02.py`, `src/celula_dem.py` | [DEM celular](modelos/CASOS_CELULARES.md) |
| 03 | `src/piloto_membrana.py` | [Bicapa DEM 3D](modelos/PILOTO_MEMBRANA.md) |
| 04 | `src/piel_ogden.py` | [Energía, tensiones, contacto y FEM](modelos/PIEL_OGDEN.md) |
| 05 | `src/vesicula_dpd.py` | [DPD de vesícula y funciones](modelos/VESICULA_DPD.md) |
| 06 | `src/caso_06_plana.py`, `src/penetracion_activa.py` | [Hoja elástica, WCA y Fourier](modelos/CASO_06.md) |
| 07 | `src/caso_07_dipolar.py`, `src/penetracion_activa.py` | [Energía dipolar, torque y perfil triangular](modelos/CASO_07.md) |
| 08 | `src/caso_08_cooperativa.py`, `src/bicapa_dpd.py` | [DPD H2T5 y cuerpos guiados](modelos/CASO_08.md) |
| 09 | `src/caso_09_tetraedro.py`, `src/bicapa_dpd.py` | [DPD DOPC y rotación del tetraedro](modelos/CASO_09.md) |

En cada motor identifica configuración → geometría → fuerzas → integrador → observables → archivos y dibujo. La visualización consume las coordenadas resultantes; no añade una deformación predeterminada.

Al compartir un motor, dos casos siguen teniendo artículos distintos, pero deben explicarse sus diferencias físicas: en 06 predominan resortes de una hoja; 07 incorpora energía y torque dipolares de una cadena. En 08 los lípidos son H2T5 y las NP reciben resortes móviles; 09 usa DOPC de 14 beads y una NP tetraédrica con velocidad inicial, sin resorte móvil.

Para cada función presenta argumentos, unidades, retornos, forma de arreglos, dependencias y su responsabilidad física. Explica qué cambiaría si se quitara una fuerza o se modificara el paso temporal. Distingue una modificación de física de una modificación del dibujo.
