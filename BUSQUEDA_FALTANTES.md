# Búsqueda y resolución de los casos restantes

**Estado actual:** nueve actividades reducidas asignadas y ejecutadas en el alcance ampliado a penetración mecánica aprobado por el docente. Los cuatro añadidos son Daddi-Moussa-Ider et al. (NJP 2019), Daddi-Moussa-Ider et al. (JCP 2019), Zhang et al. (2015) y Yong/Du (2023). [Selección vigente](REVISION_BIOBALISTICA.md). La revisión que sigue describe la búsqueda previa bajo el criterio de biobalística estricta; no es el estado actual de entrega.

Revisión histórica: 14 de noviembre de 2026. Se mantienen tres condiciones simultáneas: artículo distinto, texto/modelo públicamente accesible y colisión biobalística con deformación del blanco calculada. No se cambian estos requisitos por un número suficiente de DOI.

## Nuevo piloto implementado

**Arai, Yasuoka y Zeng (2013), [10.1039/C3NR02024J](https://doi.org/10.1039/C3NR02024J).** El texto completo editorial fue obtenido y sus ecuaciones 1–7 se cotejaron visualmente en el PDF. La página editorial indica CC BY 3.0. Describe colisión de NP con vesícula y evolución de su membrana. Se añadieron `vesicula_dpd.py`, `verificar_vesicula.py` y [guía de ejecución y funciones](VESICULA_DPD.md). Es una implementación reducida con parámetros complementarios, no una réplica cuantitativa ni una asignación definitiva. No representa una pistola génica.

## Otras fuentes examinadas

| Fuente distinta | Evidencia accesible | Decisión para la actividad solicitada |
|---|---|---|
| Fraire et al. (2022), [10.1038/s41467-022-29713-7](https://www.nature.com/articles/s41467-022-29713-7) | Texto y suplemento abiertos, CC BY 4.0; biobalística nanométrica en células de mamífero | Sigue pendiente: el suplemento describe interfaz bifásica en Fluent, pero no toda la configuración para reproducirla. La solución analítica de Stokes solo no calcula deformación de membrana |
| Jijumon et al. (2025), [Ballistic Microscopy, 10.1101/2025.10.07.681030](https://www.biorxiv.org/content/10.1101/2025.10.07.681030v1) | Preprint abierto; se obtuvo suplemento de 55 páginas, incluyendo teoría S17–S21 | No se asigna como caso terminado: trayectoria y escalas de cavitación/estiramiento no definen una evolución espacial completa de la membrana. La energía de expansión S4 requiere además aclaración dimensional. Se declara que es preprint |
| Berkey et al. (2022), [10.1038/s44172-022-00031-6](https://www.nature.com/articles/s44172-022-00031-6) | Abierto CC BY 4.0; FEM multicapa de piel humana con Ogden, GOH y Prony | Esferas de 4.4–5 mm y lesión por fragmentos. No se introduce como sustituto silencioso de biobalística micro/nanométrica para entrega celular |
| Shen et al. (2024), [10.1016/j.matlet.2023.135368](https://doi.org/10.1016/j.matlet.2023.135368) | Registro de manuscrito aceptado; el enlace al PDF devolvió página no encontrada en la comprobación actual | No se cuenta como texto abierto verificado. El modelo del artículo de 2025 no sustituye el acceso a este artículo distinto |
| Elsafty, Berkey y Dauskardt (2024), [10.1016/j.jmbbm.2024.106456](https://doi.org/10.1016/j.jmbbm.2024.106456) | Resumen y registro editorial; no se obtuvo texto completo abierto | No asignado |
| Rostami y Ahmadian (2024), [10.1088/2057-1976/ad5019](https://pubmed.ncbi.nlm.nih.gov/38788696/) | Resumen primario: colisión de nanoaguja, membrana/córtex FEM y citoplasma Euleriano; no se obtuvo texto abierto | No asignado, aunque el caso con velocidad inicial sería un candidato pertinente |
| Zhang et al. (2018), [10.1039/C7NR08879E](https://doi.org/10.1039/C7NR08879E) | Resumen primario de impacto balístico en membrana | Falta texto completo abierto verificado; no se reconstruye el modelo desde el resumen |
| Yong y Du (2023), [manuscrito público NSF](https://par.nsf.gov/servlets/purl/10447218) | DPD de nanotetraedros y membrana; entrada con momento inicial | Estudia nanoplásticos y su difusión/inserción. No se cuenta como otro artículo de biobalística celular sin ampliar el tema solicitado |

También se revisaron estudios abiertos de penetración activa, endocitosis, gelatina/hidrogeles y dinámica de vesículas en flujo. No equivalen por sí mismos a los casos pedidos. Una tesis pública puede servir para estudiar ecuaciones, pero no se cuenta como un artículo distinto de acceso abierto.

## Estado previo a la ampliación de alcance

Antes de la ampliación había **cinco implementaciones didácticas reducidas de cinco artículos distintos, incluida la nueva exploración DPD**, y no nueve casos cerrados. El quinto piloto conserva pendientes de fidelidad y calibración descritos en su guía. Las tres copias públicas de autor de Campello mantienen su salvedad de licencia. El acceso y la fidelidad de cada fuente se registran por separado en [la revisión](REVISION_BIOBALISTICA.md).

Bajo aquel criterio faltaban cuatro implementaciones y una selección definitiva. El alcance ampliado permitió completar las nueve actividades docentes, con las limitaciones de fidelidad señaladas en cada guía. Esta búsqueda no demuestra que no existan otras fuentes; indica cuáles se comprobaron y por qué no permiten declarar la tarea completa. Los archivos auxiliares antiguos tampoco completan ese número.
