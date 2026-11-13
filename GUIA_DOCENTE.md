> **MATERIAL AUXILIAR ANTERIOR. Esta ficha no constituye una asignación de biobalística en células o tejidos. Consulta [la revisión vigente](REVISION_BIOBALISTICA.md).**

# Guía docente: aprender a generar simulaciones

Asigna una ficha a cada alumno. Hay nueve artículos y nueve DOI únicos, aunque algunos autores y familias de modelos se repiten. Todos calculan indentación del blanco, con esfera rígida; se sustituyeron los casos antiguos de vuelo, penetración sin deformación y pared rígida.

La selección es de fundamentos de mecánica de impacto relacionados con la biobalística. No se afirma que los nueve artículos estudien células. Antes de fijar la entrega, revisa el acceso a las lecturas de suscripción (02–05); se indican enlaces y versiones. No es necesario comprar PDFs para ejecutar los ejemplos. Si la biblioteca no proporciona una lectura, la ficha identifica el alcance disponible y el complemento de autores cuando existe.

## Secuencia sugerida

1. Diagrama, unidades y ley extraída del artículo; predicción sin ejecutar.
2. Derivación de una referencia analítica con sus supuestos y límites.
3. Código propio por funciones; contraste con la referencia resuelta.
4. Verificación, tres escenarios y refinamiento del paso.
5. Animación de esfera y blanco, métricas y defensa en vivo.

Para una demostración común empieza por 09 (solución cerrada), sigue con 01 (energía y cuadratura) y muestra luego un modelo disipativo. Los casos 06–08 requieren distinguir serie, referencia límite y contacto sin atracción. Sus referencias no son soluciones temporales completas.

## Rúbrica: 20 puntos

| Criterio | Puntos |
|---|---:|
| Artículo, diagrama, variables y supuestos | 3 |
| Derivación analítica y dominio de validez | 5 |
| Estructura, entradas, retornos y explicación de funciones | 5 |
| Verificación, energía y comparación de escenarios | 4 |
| Animación coherente y modificación propia revisada | 3 |

## Defensa de 6–8 minutos

Pide localizar la ley, desarrollar un paso de la deducción, recorrer main() y explicar dos funciones elegidas por ti. Elige una función del modelo y otra del integrador o de la animación. Solicita un cambio de parámetro, predicción previa y ejecución. Pregunta por la forma del arreglo de estado y por qué aumentar cuadros no reduce el error de RK4.

En 03/04, pregunta por qué e_obj no coincide necesariamente con e_calculado. En 07, distingue truncamiento y criterio de separación. En 08/09, pregunta por qué una indentación positiva al separarse no demuestra una huella permanente. En todos, diferencia indentación, deformación unitaria y perforación.

## Evidencias mínimas

Derivación individual, implementación propia con modificación justificada, 27 escenarios repartidos entre los nueve alumnos, tabla de métricas, comparación con referencia, CSV, visor, GIF y tabla de funciones. No evalúes como aprendizaje suficiente la mera reproducción del archivo proporcionado. Pide tres ejemplos de ayuda de Copilot que el alumno haya verificado, sin exigir conversaciones personales completas.

El perfil del blanco es una reconstrucción cuasiestática común. Solo la indentación se resuelve dinámicamente en todos los casos; no exijas interpretar el dibujo como un campo 3D de tensiones. Los parámetros relativos no son propiedades medidas de organismos. Fecha y plataforma de entrega: las define el docente.
