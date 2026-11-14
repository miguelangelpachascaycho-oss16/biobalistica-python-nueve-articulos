# Selección de artículos y estado real de la actividad

Actualización: 14 de noviembre de 2026. **La solicitud de nueve artículos distintos abiertos con impacto y deformación del blanco no está completada.** No distribuir las nueve fichas auxiliares antiguas como si cumplieran este requisito.

## Implementaciones disponibles

| Artículo distinto | Implementación | Deformación calculada | Acceso y límites |
|---|---|---|---|
| Campello y Zohdi (2014), [10.1002/cnm.2649](https://doi.org/10.1002/cnm.2649) | [Célula 01](CASOS_CELULARES.md) | Dos capas de nodos y enlaces en célula circular | Copia pública de autor; licencia abierta no confirmada. Reducción de malla, chorro y tiempo |
| Campello y Zohdi (2014), [10.3970/cmes.2014.098.221](https://doi.org/10.3970/cmes.2014.098.221) | [Célula 02](CASOS_CELULARES.md) | Dinámica celular y variabilidad de proyectiles | Copia pública de autor; licencia abierta no confirmada. Tres muestras docentes, no los 400 cálculos publicados |
| Campello (2015), [10.1007/s40430-014-0273-5](https://doi.org/10.1007/s40430-014-0273-5), ejemplo 5.3 | [Bicapa plana](PILOTO_MEMBRANA.md) | DEM 3D de ambas capas | Copia pública de autor; licencia abierta no confirmada. Piloto reducido |
| Shen et al. (2025), [10.1016/j.taml.2024.100567](https://doi.org/10.1016/j.taml.2024.100567) | [Piel Ogden](PIEL_OGDEN.md) | Nodos FEM axisimétricos con energía de Ogden | CC BY 4.0. Solo fase temprana; no replica el SPH-FEM, perforación ni curvas publicadas. Compresión volumétrica local elevada declarada |
| Arai et al. (2013), [10.1039/C3NR02024J](https://doi.org/10.1039/C3NR02024J) | [Piloto DPD](VESICULA_DPD.md) | Beads de vesícula HTTT, solvente explícito e impacto con control | CC BY 3.0. Geometría y escala reducidas; integrador distinto; dos entradas de interacción complementadas y convenciones corregidas. No reproduce umbrales ni área de poro |

Las comprobaciones matemáticas están en `VERIFICACION_CELULAS.json`, `VERIFICACION_PILOTO.json`, `VERIFICACION_PIEL.json` y `VERIFICACION_VESICULA.json`. No equivalen a validación biológica.

## Candidatos abiertos aún sin una implementación aceptable

- Fraire et al. (2022), [10.1038/s41467-022-29713-7](https://www.nature.com/articles/s41467-022-29713-7): nanoscale biolistics en células de mamífero, CC BY 4.0. Su suplemento describe una interfaz bifásica y movimiento de esfera en Fluent, pero no aporta todos los detalles para reproducir su deformación en Python. Stokes solo no cumple.


## Candidatos retirados de la asignación

Zhang et al. (2018), Shen et al. (2024), Guha et al. (2010) y Hardy y Kendall (2005) dejan de contarse como asignaciones: no se ha verificado su texto/modelo abierto adecuado. Los datos bibliográficos se conservan en `descartados_de_asignacion` de [SELECCION_BIOBALISTICA.json](SELECCION_BIOBALISTICA.json). La tesis pública de Guha sigue siendo material complementario; no reemplaza a un artículo distinto.

Se revisaron también estudios de penetración activa de partículas, indentación de membranas, impacto en gelatina/hidrogeles y deformación por chorro gaseoso. No se contabilizan como nuevos casos de biobalística celular/tisular. Un DOI distinto, una trayectoria o una animación plausible no bastan: hacen falta una ley de deformación publicada y acceso al detalle necesario para implementarla.

No se afirma que no existan otros artículos; la búsqueda realizada no ha identificado nueve que permitan cerrar esta tarea sin cambiar los requisitos o inventar una correspondencia de modelos. Hay cinco implementaciones reducidas, incluida la exploración DPD provisional. Faltan cuatro implementaciones y una selección completa de fuentes que cumpla el acceso solicitado; tres de las cinco implementaciones disponibles conservan además la salvedad de licencia indicada arriba.

Detalle de las nuevas fuentes revisadas: [BUSQUEDA_FALTANTES.md](BUSQUEDA_FALTANTES.md).
