# Guía docente: construir y explicar simulaciones de biobalística

La actividad de nueve alumnos sigue incompleta. Hay cinco implementaciones didácticas reducidas de cinco artículos distintos, incluida una exploración DPD provisional; no hay nueve réplicas completas. La [revisión vigente](REVISION_BIOBALISTICA.md) y [la búsqueda de fuentes](BUSQUEDA_FALTANTES.md) registran los pendientes. No asignar los ejemplos auxiliares de contacto como si fueran artículos de biobalística celular/tisular.

## Programas disponibles y lecturas

| Modelo | Programa | Guía con ecuaciones, instalación y funciones |
|---|---|---|
| Campello y Zohdi, cnm.2649 | `caso_celular_01.py --animar` | [Célula 01](CASOS_CELULARES.md) |
| Campello y Zohdi, CMES 98:221 | `caso_celular_02.py --muestras 3 --animar` | [Célula 02](CASOS_CELULARES.md) |
| Campello 2015, solo ejemplo 5.3 | `piloto_membrana.py --animar` | [Bicapa 3D](PILOTO_MEMBRANA.md) |
| Shen et al. 2025 | `piel_ogden.py --animar` | [Impacto temprano en piel](PIEL_OGDEN.md) |
| Arai et al. 2013, piloto provisional | `vesicula_dpd.py --animar` | [Colisión con vesícula](VESICULA_DPD.md) |

Ejecutar esos argumentos con `.\.venv\Scripts\python.exe` después de instalar `requirements.txt`, como indica cada guía. Las guías declaran qué procede del artículo, qué se reduce y qué datos se eligen para la actividad. No todas las fuentes tienen licencia abierta confirmada; consultar la tabla de revisión.

## Secuencia de aprendizaje

1. Leer el artículo y localizar sus ecuaciones, variables, unidades, condiciones iniciales y tipo de blanco. Dibujar el problema y anticipar el movimiento antes de ejecutar.
2. Identificar cambios entre artículo y programa. Explicar qué conclusión impide cada simplificación.
3. Derivar un subproblema analítico: vuelo libre, enlace armónico, una ley constitutiva homogénea o trayectoria Poncelet según el caso. No afirmar una solución cerrada para toda la membrana si solo existe para ese límite.
4. Explicar cada función: entrada, unidades, retorno, dimensión de los arreglos, función que la llama y papel en el cálculo. Separar fuerzas, integración, observables y dibujo.
5. Ejecutar el control sin impacto y la simulación con impacto. Leer los CSV y comprobar que la animación provenga de esos estados.
6. Ejecutar el verificador correspondiente. Refinar tiempo/malla cuando proceda y distinguir verificación matemática de validación con datos experimentales. En DPD se necesitan conjuntos de semillas para comparar distribuciones.
7. Usar Copilot para revisar derivaciones o funciones pequeñas; registrar una propuesta aceptada y una corrección justificada. Revisar el diff.
8. Presentar código, parámetros, curvas y animación, más una defensa oral sin leer la respuesta de Copilot.

## Evaluación sugerida

| Evidencia | Puntaje |
|---|---:|
| Ecuaciones, unidades y correspondencia con el artículo | 25 |
| Explicación de estructura y funciones del código | 25 |
| Referencia analítica y controles numéricos | 20 |
| Interpretación de impacto, deformación y control | 20 |
| Registro crítico del trabajo con Copilot y limitaciones | 10 |

El alumno debe poder señalar la línea donde se calcula la fuerza sobre el blanco, la reacción sobre el proyectil y la actualización de posición. Debe explicar por qué trayectoria, deformación, difusión, daño y penetración son magnitudes diferentes. No se exige ejecutar experimentos biológicos.
