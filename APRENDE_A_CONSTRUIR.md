# Aprende a construir tu simulación

El objetivo es que puedas crear y defender una simulación desde una ecuación. Los archivos resueltos son referencias para contrastar tu trabajo; tu entrega debe incluir una derivación, una implementación propia y una modificación razonada.

## 1. Convertir la lectura en un problema

Dibuja esfera rígida y blanco deformable. Localiza en tu artículo la fuerza normal y escribe sus variables, unidades, supuestos y condición de separación. Declara el límite esfera–blanco que usamos: blanco fijo, toda la compliancia en el blanco y sin fricción. Distingue esa adaptación de los experimentos originales.

Entrega antes de programar: una hoja con el diagrama, `m*delta_ddot=-F(delta,delta_dot)` y las condiciones iniciales. Define qué esperas que cambie entre A y C.

## 2. Resolver primero una relación analítica

Si necesitas una introducción, estudia el caso 09 y deduce la solución del oscilador amortiguado. Después trabaja tu caso individual con [SOLUCIONES_ANALITICAS.md](SOLUCIONES_ANALITICAS.md).

Tu resultado puede ser una fórmula temporal cerrada, una primera integral implícita o una serie truncada. Escribe qué sabes calcular directamente, qué exige una raíz o cuadratura y dónde vale la aproximación. Comprueba una derivada a mano. No llames «analítica» a una curva obtenida únicamente integrando una ODE.

## 3. Escribir funciones pequeñas

Empieza con estas responsabilidades, sin copiar el programa completo:

```python
def fuerza_contacto(q, v, parametros):
    # Implementa aquí tu ley; define qué significa cada entrada y la salida.
    raise NotImplementedError

def derivadas(t, estado):
    q, v = estado
    return [v, -fuerza_contacto(q, v, parametros)]
```

Calcula a mano dos valores de fuerza y compruébalos en Python. Indica por qué la primera derivada devuelve velocidad y la segunda aceleración. Explica que el estado guarda dos variables, mientras un historial guarda muchas filas temporales. El ejemplo añade una tercera variable integrada: energía disipada.

## 4. Programar y comparar dos rutas

Construye primero la referencia analítica que corresponda. Después implementa una integración numérica. Puedes comenzar con Euler para observar su error y pasar a RK4. La referencia preparada usa RK4 con paso fijo y una localización más precisa del último instante.

Guarda q y v en un arreglo de forma `(numero_de_instantes, numero_de_variables)`. Usa una función para calcular y otra para dibujar. Compara tu ruta numérica con la referencia por una diferencia cuantitativa, no solo porque las líneas parezcan coincidir.

En 02–05 se usa la primera integral para construir q(s) mediante raíces y cuadratura: esa ruta es semianalítica y no reutiliza RK4. En 06–08 la serie temporal solo vale al inicio; las predicciones de restitución y separación se estudian por separado.

## 5. Detectar el final físico del contacto

No elijas un tiempo arbitrario para continuar la reacción. Al descargar, detecta el primer cero de la fuerza repulsiva. En los modelos elásticos puede coincidir con q=0; en los modelos viscosos puede suceder antes. Compara expresamente ambos criterios cuando tu ficha lo pida.

Prueba qué error aparece si continúas una fuerza atractiva en un modelo sin adhesión. No muestres ese tramo como si fuera el resultado físico de tu animación.

## 6. Comprobar antes de animar

- Revisa condiciones iniciales y signos.
- Compara con tu solución o relación analítica y declara el dominio válido.
- Comprueba energía cinética + elástica + disipada durante el contacto.
- Reduce el paso a la mitad y compara indentación máxima y restitución.
- Distingue una discrepancia del modelo, una serie truncada y un error numérico.

Una curva suave no demuestra que el cálculo sea correcto. Para la defensa, muestra al docente una comprobación que detectaría una ecuación con signo equivocado.

## 7. Convertir resultados en movimiento

Cada cuadro toma q, v y F del mismo historial numérico. La esfera permanece rígida y su centro está en `z=q-R`. El blanco se deforma con profundidad central q, utilizando el perfil cuasiestático declarado en [MODELO_DEFORMACION_BLANCO.md](MODELO_DEFORMACION_BLANCO.md). El punto de la gráfica corresponde al mismo instante.

Explica cómo `np.interp` remuestrea para reproducir cuadros y por qué el número de cuadros no cambia la precisión de la ODE. Nunca midas una profundidad contando píxeles: usa el CSV y sus escalas.

## 8. Usar Copilot para aprender

Pide una pregunta o un cambio por vez. Por ejemplo: «Muéstrame la forma del arreglo que recibe esta función y pídeme explicar su retorno», o «Revisa mi derivación y señala el primer paso que no se deduce del anterior». Revisa las propuestas y ejecuta las comprobaciones antes de aceptarlas.

Tu trabajo está listo cuando puedes cambiar un parámetro, anticipar el efecto, ejecutar, explicar una diferencia y recorrer cualquier función sin depender de la respuesta de la IA.

## Producto final

Entrega código propio ejecutable, derivación analítica, comparación de los tres escenarios, métricas, animación, tabla de funciones y una modificación personal. Sugiere una condición en la que tu modelo dejaría de ser adecuado para una situación biobalística real.
