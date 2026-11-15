# Referencias analíticas de las nueve actividades

Una solución analítica de un subproblema comprueba una parte del programa. No sustituye la simulación de todo el blanco.

| Alumno | Límite o solución para estudiar | Ubicación |
|---|---|---|
| 01 | Vuelo libre y enlace lineal; acción/reacción del contacto | [Guía DEM](modelos/CASOS_CELULARES.md) |
| 02 | Los mismos límites mecánicos, separando variabilidad de parámetros | [Guía DEM](modelos/CASOS_CELULARES.md) |
| 03 | Oscilación de un enlace y control sin proyectiles | [Bicapa](modelos/PILOTO_MEMBRANA.md) |
| 04 | Trayectoria Poncelet y derivada de energía Ogden para el campo FEM | [Piel](modelos/PIEL_OGDEN.md) |
| 05 | Dos beads unidos por resorte: omega=sqrt(2C/(m*rs)) | [Vesícula](modelos/VESICULA_DPD.md) |
| 06 | Serie de Fourier espacial y relajación exponencial por modo, ecuaciones 20 y 24 del artículo | [Hoja elástica](modelos/CASO_06.md) |
| 07 | Perfil triangular de pequeña deformación y orientación dipolar, ecuación 43 del artículo | [Cadena dipolar](modelos/CASO_07.md) |
| 08 | NP unida a ancla móvil sin medio: z=z0−Vt+(V/omega)sin(omega*t) | [Dos NP](modelos/CASO_08.md) |
| 09 | Rotación libre de tetraedro con inercia isotrópica y oscilador de enlace aislado | [Tetraedro](modelos/CASO_09.md) |

Los casos 06 y 07 incluyen una comparación de perfil con la solución publicada; no se usa esa curva para mover los nodos. En 08 y 09 se deducen límites a partir de sus leyes de fuerza para aprender verificación: no se atribuye a los autores una solución cerrada para toda la bicapa.

Antes de pedir código a Copilot, explica hipótesis, condiciones iniciales/de borde, ecuación y unidades. Después compara error al refinar el paso. La fuerza conservativa debe seguir el gradiente de su energía y la fuerza disipativa debe tener potencia no positiva en el par aislado.
