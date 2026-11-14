# Revisión de artículos de biobalística en células y tejidos

**Estado: selección en revisión. No son nueve asignaciones terminadas.**

Se localizaron nueve artículos distintos relacionados con biobalística celular o tisular. El noveno es condicional y puede requerir sustitución. Todavía no hay nueve réplicas completas verificadas en Python. Los identificadores B01–B09 son candidatos, no números definitivos de alumno.

## Criterio de aceptación

Cada asignación debe reunir: un artículo único; blanco celular o tisular (se admite una membrana celular idealizada); micro/nanoproyectil balístico; ley publicada que determine la deformación del blanco; ecuaciones, parámetros y condiciones identificables; implementación Python trazable; animación a partir de esos estados; comprobaciones numéricas; explicación de funciones y un límite analítico identificable. Un material sintético que imite tejido no basta para esta selección.

## Candidatos y pendientes

| ID | Artículo distinto | Blanco | Método del artículo | Estado |
|---|---|---|---|---|
| B01 | Campello y Zohdi (2014). [A computational framework for simulation of the delivery of substances into cells](https://doi.org/10.1002/cnm.2649) | Célula idealizada con bicapa lipídica | DEM: nodos, enlaces, presión y contactos | Modelo identificado; implementación y validación pendientes |
| B02 | Campello y Zohdi (2014). [Design Evaluation of a Particle Bombardment System Used to Deliver Substances into Cells](https://doi.org/10.3970/cmes.2014.098.221) | Célula idealizada con bicapa lipídica | DEM celular con variabilidad de los proyectiles | Modelo identificado; implementación y validación pendientes |
| B03 | Campello (2015). [Computational modeling and simulation of rupture of membranes and thin films](https://doi.org/10.1007/s40430-014-0273-5) | Bicapa lipídica; exclusivamente ejemplo 5.3 | DEM de dos capas en tres dimensiones | Piloto reducido implementado; reproducción completa pendiente |
| B04 | Zhang, Meng, Qin y Keten (2018). [Ballistic impact response of lipid membranes](https://doi.org/10.1039/C7NR08879E) | Membrana lipídica | Dinámica molecular de grano grueso | Pendiente de texto completo y suplemento |
| B05 | Fraire et al. (2022). [Light triggered nanoscale biolistics for efficient intracellular delivery of functional macromolecules in mammalian cells](https://doi.org/10.1038/s41467-022-29713-7) | Membrana celular en medio acuoso | Fluido bifásico, malla dinámica y movimiento de esfera | Faltan detalles para una réplica Python completa y verificada |
| B06 | Shen, Meng, Hirschler y Roth (2024). [Dynamic behavior of multilayered skin structure: A preliminary numerical and analytical microscopic analysis](https://doi.org/10.1016/j.matlet.2023.135368) | Piel multicapa | SPH-FEM y análisis de penetración | Pendiente de texto completo |
| B07 | Shen et al. (2025). [Investigation of dynamic behavior of human skin tissue under micro-particle impact in the context of transdermal drug delivery: numerical and analytical perspectives](https://doi.org/10.1016/j.taml.2024.100567) | Tejido cutáneo humano | SPH-FEM con ley hiperelástica de Ogden | Modelo identificado; implementación y validación pendientes |
| B08 | Guha, Shear y Papini (2010). [Ballistic Impact of Single Particles Into Gelatin: Experiments and Modeling With Application to Transdermal Pharmaceutical Delivery](https://doi.org/10.1115/1.4002428) | Dermis humana en modelo FEM; gelatina en experimentos | Elementos finitos de impacto y penetración | Tesis pública de 2009 revisada; pendiente cotejar el artículo de 2010 |
| B09 | Hardy y Kendall (2005). [Mucosal deformation from an impinging transonic gas jet and the ballistic impact of microparticles](https://doi.org/10.1088/0031-9155/50/19/010) | Mucosa | CFD con superficie deformable y micropartículas | CONDICIONAL: no asignar; comprobar si cumple deformación calculada por impacto |

## Decisiones que evitan una falsa reproducción

- B01 y B02 son publicaciones distintas, pero comparten una familia DEM. No se presentarán como teorías independientes. B02 debe conservar dinámica celular y trazabilidad de la variabilidad, no limitarse a una regresión.
- B03 cuenta por su ejemplo biológico 5.3; sus ejemplos de tela y cizallamiento no son la práctica asignable. Hay un [piloto reducido](PILOTO_MEMBRANA.md), identificado como tal.
- B04 requiere revisar potenciales e integración molecular antes de escribir una réplica. No se reemplaza por resortes genéricos.
- B05 requiere resolver la interfaz y el fluido para mostrar su deformación. Su solución de Stokes es una referencia de movimiento libre, no un modelo de deformación celular.
- B06 y B07 necesitan deformación espacial del tejido. La profundidad de Poncelet no define por sí sola la forma de la piel.
- B08 solo puede entrar por su submodelo de dermis humana, una vez revisado el texto completo. La gelatina experimental no se renombra como piel.
- B09 permanece fuera de la asignación: debe aclararse si la forma del tejido es dato impuesto y si satisface el impacto de esfera solicitado. Su título no demuestra que lo cumpla.

Fuentes: cada título enlaza al DOI. Las páginas/textos efectivamente consultados y la evidencia disponible están en [SELECCION_BIOBALISTICA.json](SELECCION_BIOBALISTICA.json). No se redistribuyen PDF editoriales en el repositorio.

## Qué impide cerrar los nueve casos

Faltan los textos completos y/o suplementos de los artículos B04, B06, B08 y B09 para comprobar las ecuaciones; en B08 ya se obtuvo y revisó la tesis complementaria de 2009, que debe cotejarse con el artículo; en B05 faltan detalles de configuración para una réplica verificable. B01, B02 y B07 tienen modelo identificado pero aún requieren implementación y comprobación. Es necesario confirmar o sustituir B09. Tener un DOI diferente no equivale a tener una simulación reproducida.

Las prácticas antiguas de contacto permanecen como fundamentos auxiliares. No cumplen por sí solas esta actividad y no deben entregarse como nueve artículos de biobalística celular.

Actualización de acceso: se encontró la tesis pública de Guha (2009). Consulta [el informe de fuentes](ACCESO_FUENTES.md) para distinguir tesis, artículo y enlaces todavía inaccesibles.
