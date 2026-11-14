# Guía docente: nueve actividades de modelado y explicación del código

La selección docente contiene nueve artículos distintos, con implementaciones reducidas. Los casos 06–09 se incluyen tras autorizar la ampliación a penetración mecánica de nanopartículas; no se renombran como biobalística. Los modelos 06 y 07 son membranas artificiales mínimas; 08 y 09 usan bicapas moleculares idealizadas. Ningún ejercicio constituye validación de células reales ni una reproducción completa del artículo.

La asignación está en [README](README.md), [ACTIVIDADES.json](ACTIVIDADES.json) y `ALUMNO_01.md`–`ALUMNO_09.md`. Cada ficha incluye lectura, comandos, salidas, funciones, derivación y defensa. Las diferencias entre modelos, acceso y licencias están en [REVISION_BIOBALISTICA.md](REVISION_BIOBALISTICA.md).

## Ejecutar un caso

```powershell
.\.venv\Scripts\python.exe ejecutar_caso.py 8 --animar
```

Sustituye 8 por el número del alumno; no se ejecutan nueve simulaciones en paralelo. Sigue la instalación de cada ficha. Los motores separan fuerzas, integración, observables y dibujo. Los cuatro programas nuevos usan `penetracion_activa.py` y `bicapa_dpd.py`, con leyes y topologías específicas según artículo.

## Secuencia de aprendizaje

1. Leer el artículo y localizar sus ecuaciones, variables, unidades, condiciones iniciales y tipo de blanco. Dibujar el problema y anticipar el movimiento antes de ejecutar.
2. Identificar cambios entre artículo y programa. Explicar qué conclusión impide cada simplificación.
3. Derivar un subproblema analítico: vuelo libre, enlace armónico, una ley constitutiva homogénea o trayectoria Poncelet según el caso. No afirmar una solución cerrada para toda la membrana si solo existe para ese límite.
4. Explicar cada función: entrada, unidades, retorno, dimensión de los arreglos, función que la llama y papel en el cálculo. Separar fuerzas, integración, observables y dibujo.
5. Ejecutar el control sin impacto y la simulación con impacto. Leer los CSV y comprobar que la animación provenga de esos estados.
6. Ejecutar el verificador correspondiente. Refinar tiempo/malla cuando proceda y distinguir verificación matemática de validación con datos experimentales. En DPD se necesitan conjuntos de semillas para comparar distribuciones; los casos 08–09 permiten `--semilla` y `--dt`.
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
