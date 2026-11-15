# Aprender a generar una simulación desde un artículo

1. Delimita el blanco y el mecanismo: balística con inercia, contacto activo de Stokes o dinámica molecular con solvente. El modelo de una esfera rígida no implica que el blanco sea rígido.
2. Copia a tu cuaderno las ecuaciones necesarias, identifica parámetros y unidades y marca cualquier dato añadido por la reducción docente. No conviertas una elección de código en un dato del artículo.
3. Dibuja fuerzas y condiciones de borde. Decide qué recibe la reacción del contacto y qué fuerzas provienen del medio o de un apoyo externo.
4. Deriva un límite analítico que pueda resolverse antes de programar. Consulta [el mapa de referencias](SOLUCIONES_ANALITICAS.md).
5. Escribe una función pequeña para la ley de fuerza. Comprueba signo, dimensiones y, si existe potencial, `F=−grad(U)`. Para dipolos/rigidez comprueba también torque.
6. Construye la geometría por separado. Un arreglo de coordenadas no es todavía una simulación dinámica.
7. Programa la actualización del estado y un control de reposo o vuelo libre. Evita que un integrador adaptativo salte toda la zona de contacto durante un paso libre.
8. Calcula observables a partir de posiciones: desplazamiento normal, perfil, asfericidad o rugosidad, según el blanco. Identifica qué no mide cada observable.
9. Guarda CSV, parámetros y estados. Dibuja la partícula y el blanco desde el mismo instante de esos datos.
10. Refina paso/malla y contrasta con el límite analítico. En modelos con ruido, compara distribuciones de conjuntos de semillas, no coincidencias de una sola trayectoria.
11. Contrasta con el artículo sin olvidar diferencias de dimensión, escala, solvente, química o duración. La comparación de un límite no valida la célula completa.
12. Explica cada función y presenta una limitación concreta. Usa Copilot para revisar pasos, no para sustituir tu defensa de las ecuaciones.

Cada alumno sigue el README de su carpeta en `casos/` y la guía de su modelo. Las animaciones pregeneradas sirven para revisar el resultado esperado; la entrega incluye una ejecución propia y un cambio razonado.
