# Estructura y funciones de las nueve actividades

El lanzador `ejecutar_caso.py` no calcula fuerzas. Su `main()` lee `ACTIVIDADES.json`, selecciona un programa y lo ejecuta con el mismo intérprete Python. Los argumentos adicionales llegan al programa científico. Así, `ejecutar_caso.py 9 --animar` ejecuta `caso_09_tetraedro.py --animar`.

| Alumnos | Programa o motor | Explicación de funciones |
|---|---|---|
| 01–02 | `caso_celular_01.py`, `caso_celular_02.py`, `celula_dem.py` | [DEM celular](CASOS_CELULARES.md) |
| 03 | `piloto_membrana.py` | [Bicapa DEM 3D](PILOTO_MEMBRANA.md) |
| 04 | `piel_ogden.py` | [Energía, tensiones, contacto y FEM](PIEL_OGDEN.md) |
| 05 | `vesicula_dpd.py` | [DPD de vesícula y funciones](VESICULA_DPD.md) |
| 06 | `caso_06_plana.py`, `penetracion_activa.py` | [Hoja elástica, WCA y Fourier](CASO_06.md) |
| 07 | `caso_07_dipolar.py`, `penetracion_activa.py` | [Energía dipolar, torque y perfil triangular](CASO_07.md) |
| 08 | `caso_08_cooperativa.py`, `bicapa_dpd.py` | [DPD H2T5 y cuerpos guiados](CASO_08.md) |
| 09 | `caso_09_tetraedro.py`, `bicapa_dpd.py` | [DPD DOPC y rotación del tetraedro](CASO_09.md) |

En cada motor identifica configuración → geometría → fuerzas → integrador → observables → archivos y dibujo. La visualización consume las coordenadas resultantes; no añade una deformación predeterminada.

Al compartir un motor, dos casos siguen teniendo artículos distintos, pero deben explicarse sus diferencias físicas: en 06 predominan resortes de una hoja; 07 incorpora energía y torque dipolares de una cadena. En 08 los lípidos son H2T5 y las NP reciben resortes móviles; 09 usa DOPC de 14 beads y una NP tetraédrica con velocidad inicial, sin resorte móvil.

Para cada función presenta argumentos, unidades, retornos, forma de arreglos, dependencias y su responsabilidad física. Explica qué cambiaría si se quitara una fuerza o se modificara el paso temporal. Distingue una modificación de física de una modificación del dibujo.
