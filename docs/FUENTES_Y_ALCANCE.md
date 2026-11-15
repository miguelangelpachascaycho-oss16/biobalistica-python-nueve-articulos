# Selección vigente: nueve actividades en el alcance ampliado

Actualización: 14 de noviembre de 2026. Se completó la **selección docente y ejecución de nueve implementaciones reducidas**, con nueve DOI distintos. El docente autorizó incluir penetración mecánica de nanopartículas. Los casos 06–09 se incorporan bajo esa ampliación; no se atribuye a todos la categoría de biobalística estricta ni de tejido real.

| Alumno | Artículo distinto | Categoría | Acceso al texto | Modelo, parámetros y límites |
|---|---|---|---|---|
| 01 | [10.1002/cnm.2649](https://doi.org/10.1002/cnm.2649) | Biobalística celular | Copia pública de autor; licencia de reutilización no confirmada | [Guía](modelos/CASOS_CELULARES.md) |
| 02 | [10.3970/cmes.2014.098.221](https://doi.org/10.3970/cmes.2014.098.221) | Biobalística celular con variabilidad | Copia pública de autor; licencia de reutilización no confirmada | [Guía](modelos/CASOS_CELULARES.md) |
| 03 | [10.1007/s40430-014-0273-5](https://doi.org/10.1007/s40430-014-0273-5) | Biobalística de bicapa | Copia pública de autor; licencia de reutilización no confirmada | [Guía](modelos/PILOTO_MEMBRANA.md) |
| 04 | [10.1016/j.taml.2024.100567](https://doi.org/10.1016/j.taml.2024.100567) | Biobalística tisular; impacto temprano | CC BY 4.0 | [Guía](modelos/PIEL_OGDEN.md) |
| 05 | [10.1039/C3NR02024J](https://doi.org/10.1039/C3NR02024J) | Colisión nanométrica; modelo de vesícula | CC BY 3.0 | [Guía](modelos/VESICULA_DPD.md) |
| 06 | [10.1088/1367-2630/ab35d2](https://doi.org/10.1088/1367-2630/ab35d2) | Penetración mecánica activa; no balística | CC BY 3.0 | [Guía](modelos/CASO_06.md) |
| 07 | [10.1063/1.5080807](https://doi.org/10.1063/1.5080807) | Penetración mecánica activa; no balística | Versión abierta en arXiv y copia pública de autores | [Guía](modelos/CASO_07.md) |
| 08 | [10.1038/srep10525](https://doi.org/10.1038/srep10525) | Penetración mecánica guiada; no balística | CC BY 4.0 | [Guía](modelos/CASO_08.md) |
| 09 | [10.1021/acs.jpcb.2c07460](https://doi.org/10.1021/acs.jpcb.2c07460) | Contacto y penetración de nanoplásticos; no pistola génica | Manuscrito público NSF PAR; versión abierta arXiv 2210.11555 | [Guía](modelos/CASO_09.md) |

## Alcance físico y de las comprobaciones

Los casos 01–03 conservan modelos DEM de célula/bicapa con reducción de nodos, chorro y tiempo; no reproducen tablas o figuras completas. El 04 usa la ley de Ogden publicada para impacto temprano FEM axisimétrico, con la advertencia de unidades y compresión descrita en su guía; no reproduce SPH-FEM ni perforación. El 05 es DPD de vesícula con geometría reducida, convenciones corregidas y entradas complementarias explícitas.

Los casos 06 y 07 son modelos mínimos de membranas artificiales; incluyen referencias analíticas publicadas. El 08 conserva DPD H2T5 y el mecanismo de resortes móviles, con constantes complementarias declaradas. El 09 conserva DOPC de 14 beads, fuerzas y topología cotejadas con el código de autores, y un tetraedro rígido de 56 beads; reduce preparación y duración a contacto temprano. Ninguno se presenta como una réplica cuantitativa completa ni como validación biológica.

`pruebas/evidencia/VERIFICACION_NUEVOS.json` registra comprobaciones mecánicas de 06–09. `pruebas/evidencia/EJECUCIONES_NUEVAS.json` registra contacto efectivo y métricas observadas. `casos/06_membrana_plana/ejemplo/referencia.csv` y `casos/07_membrana_dipolar/ejemplo/referencia.csv` permiten comparar perfiles con sus límites analíticos. Los cinco anteriores conservan sus verificadores e informes específicos.

## Acceso y licencias

Todos tienen enlaces a textos completos públicamente consultables; acceso público y licencia de reutilización se registran por separado. Para los tres de Campello no se confirmó una licencia abierta de reutilización y no se redistribuyen PDFs. Los nuevos 06 y 08 indican CC BY; 07 y 09 tienen versiones abiertas en repositorios. El código Python docente se escribió para esta actividad; no se copiaron scripts GPLv3 del repositorio de Yong/Du. Sus leyes, parámetros y topologías se citan en la guía 09.


El antiguo material de contacto general se conserva como auxiliar separado. La asignación actual está en `casos/01_celula_individual/README.md`–`casos/09_bicapa_tetraedro/README.md` y `docs/ACTIVIDADES.json`.
