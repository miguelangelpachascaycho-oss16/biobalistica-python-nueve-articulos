> Registro de candidatos de la búsqueda previa; Guha, Zhang 2018, Hardy y Shen 2024 no se asignan entre las nueve actividades actuales. Consulta [la selección vigente](REVISION_BIOBALISTICA.md).

# Acceso a las fuentes pendientes

Revisión del 14 de noviembre de 2026. Se comprobaron registros bibliográficos, repositorios institucionales y páginas editoriales. Un registro de acceso abierto no garantiza que el archivo sea accesible desde esta sesión ni que corresponda exactamente al artículo.

| Caso | Hallazgo | Estado real |
|---|---|---|
| Guha 2010 | [Tesis pública de Rachel Ann Guha, 2009, RShare/Toronto Metropolitan University](https://rshare.library.torontomu.ca/articles/thesis/Ballistic_impact_of_single_particles_into_gelatin_experiments_and_modeling_with_application_to_transdermal_pharmaceutical_delivery/14655951), [DOI de la tesis](https://doi.org/10.32920/ryerson.14655951.v1) | PDF completo de 81 páginas descargado y revisado. Es una tesis complementaria; aún falta cotejar el artículo de 2010. |
| Zhang 2018 | [Página editorial](https://doi.org/10.1039/C7NR08879E) | No se localizó una copia completa pública verificable; acceso editorial bloqueado en esta sesión. |
| Hardy 2005 | [PDF editorial indicado por el catálogo de acceso abierto](https://iopscience.iop.org/article/10.1088/0031-9155/50/19/010/pdf) | El servidor devuelve una verificación humana, no un PDF. No se obtuvo el texto completo. |
| Shen 2024 | [Manuscrito aceptado indicado por el catálogo](https://www.sciencedirect.com/science/article/am/pii/S0167577X23015537) | El enlace al manuscrito aceptado redirigió a una página de PDF no encontrada en la comprobación actual. El texto completo sigue pendiente. |

## Qué aporta la tesis de Guha

Fuente complementaria con título coincidente con el artículo de 2010. Sus secciones 3.1–3.1.3 y 4.1.3 describen elementos finitos axisimétricos, una ley de Ogden incompresible y erosión de elementos. En la tesis se representa una capa equivalente de estrato córneo y epidermis viable; la dermis se omite. Esto debe cotejarse con el artículo, cuyo resumen habla de dermis.

La página impresa 29 (página 40 del PDF) da las ecuaciones 3-2 y 3-3:

```text
W = (2 mu_infinito / alpha²) (lambda1^alpha + lambda2^alpha + lambda3^alpha - 3)
P_z = (2 mu_infinito / alpha) (lambda_z^(alpha-1) - lambda_z^(-1-alpha/2))
```

`P_z` es esfuerzo nominal. La tesis obtiene un módulo de corte a alta tasa de 15 MPa; el valor 2.25 MPa corresponde a un módulo de Young cuasiestático derivado, no al parámetro de corte del impacto. Usarlos indistintamente cambiaría el modelo.

Estos hallazgos no convierten todavía B08 en una réplica del artículo. El siguiente paso es cotejar ambos documentos y registrar parámetros, contacto, erosión, malla y condiciones de contorno antes de implementarlo.

El repositorio enlaza la tesis y no redistribuye su PDF. El registro institucional la identifica como «In Copyright». Los catálogos se usaron para localizar fuentes; la identidad del documento y las ecuaciones se comprobaron en el PDF, incluida revisión visual de la página de fórmulas.

## Fuentes revisadas en la continuación

Arai et al. (2013) ya tiene texto completo editorial abierto y un piloto DPD documentado en [VESICULA_DPD.md](VESICULA_DPD.md). Se obtuvo además el suplemento teórico de Ballistic Microscopy; no define todavía un caso de evolución espacial de membrana que pueda contarse como terminado. La revisión de estas y otras fuentes está en [BUSQUEDA_FALTANTES.md](BUSQUEDA_FALTANTES.md).
