> El recorrido que sigue corresponde al motor auxiliar anterior. Para los modelos celulares/tisulares actuales consulta [DEM celular](CASOS_CELULARES.md), [bicapa 3D](PILOTO_MEMBRANA.md), [piel Ogden](PIEL_OGDEN.md) y [vesícula DPD](VESICULA_DPD.md), que explican las funciones de sus cinco implementaciones reducidas. Las nueve simulaciones auxiliares no son las nueve asignaciones biológicas solicitadas.

# Explicación de la estructura y las funciones

## Recorrido del programa

`main()` lee opciones → `verificar()` si se solicita → `comparar_escenarios()` → `calcular_modelo()` → guardar CSV y métricas → graficar → exportar visor y GIF opcional.

El archivo individual contiene la ley y los parámetros de su artículo. `motor_contacto.py` contiene métodos compartidos. `animaciones.py` convierte resultados en figuras, perfil y cuadros. Una modificación del dibujo no debe cambiar la ecuación.

## Entradas y salidas importantes

| Función individual | Recibe | Devuelve |
|---|---|---|
| parametros_escenario | Un valor de A/B/C | Diccionario k, n, beta, eta, d y zeta |
| fuerza_contacto | q escalar, v escalar y diccionario | Fuerza normal escalar relativa |
| solucion_analitica | Matriz de estados, parámetro y constantes | Matriz con referencia y diccionario de predicciones |
| calcular_modelo | Parámetro y paso temporal | Diccionario datos, parámetros, referencia y métricas |
| comparar_escenarios | A/B/C/todos y paso | Diccionario escenario → resultado |
| verificar | Sin argumentos | Métricas de error; lanza error si falla una comprobación |
| guardar_resultados | Resultados y carpeta | Guarda archivos; no devuelve una solución nueva |
| main | Argumentos de la terminal | Coordina efectos y salida por consola |

El arreglo integrado tiene tres variables: `[q, v, Wdis]`. El historial exportado tiene diez columnas: `s, q, v, fuerza, energia_elastica, energia_disipada, energia_total, q_referencia, v_referencia, delta_sobre_R`. Hay una fila por instante. Las columnas de referencia de tiempo corto quedan vacías fuera de su ventana; los estados físicos sí están calculados.

`lambda q,v: fuerza_contacto(q,v,p)` adapta la función del artículo a los dos argumentos que necesita el motor, conservando p como constantes. No introduce otra ley.

## Métodos compartidos

| Función | Entradas y salida | Qué debes entender |
|---|---|---|
| paso_rk4 | Derivadas, tiempo, vector y paso → nuevo vector | Los cuatro cálculos de pendiente y su combinación |
| integrar_contacto | Función fuerza, k, n, paso y criterio → historial | Integra q, v y energía; termina en separación |
| derivadas (interna) | Tiempo y estado → tres derivadas | q'=v, v'=-F y Wdis'=(F-Fel)*v |
| evento (interna) | Estado → escalar de contacto | Distingue carga de separación; evita parar en el contacto inicial |
| primitiva_velocidad | v, beta, eta → H(v) | Primera integral y series para evitar cancelación numérica |
| cuadratura_contacto | k, n, beta, eta y malla → curva y predicciones | Ruta semianalítica sin RK4; raíces y cuadratura por ramas |
| velocidad (interna) | q y rama → v | Resuelve H(v) con el intervalo de carga o descarga |
| acumular (interna) | dt/dángulo → tiempos | Regla trapezoidal tras regularizar el máximo de indentación |
| referencia_lineal | Tiempos y zeta → q, v y predicciones | Fórmulas cerradas del caso 09 |
| serie_inicial | Tiempos, disipación y límite → q y v aproximadas | Una serie no debe prolongarse fuera del intervalo declarado |
| completar_referencia | Datos y tipo → datos con referencia | Selecciona la referencia correcta sin alterar estados numéricos |
| metricas_contacto | Historial y predicciones → diccionario | Usa datos originales, no píxeles ni cuadros del GIF |
| perfil_blanco | Coordenadas radiales, δ y R → desplazamientos superficiales | Hipótesis espacial Hertz; su centro vale δ |
| graficar_comparacion | Número, resultados y carpeta → figura guardada | Gráficas separadas de la física |
| preparar_serie | Historial → 120 cuadros | Interpola el contacto e incluye vuelo previo uniforme |
| crear_paquete | Número y resultados → datos del visor | Agrupa curvas, cuadros y métricas |
| guardar_visor | Paquetes y ruta → HTML guardado | Serializa datos; el HTML no resuelve otra ODE |
| crear_gif | Paquete y ruta → GIF | Actualiza esfera, perfil y punto de la curva |
| cuadro (interna) | Índice → artistas actualizados | Toma un estado y modifica los objetos gráficos |
| exportar_movimiento | Número, resultados, carpeta y opción GIF | Escribe visor y GIF opcional |

## Cómo responder en la defensa

Para cada función escribe: propósito; argumentos y tipos; unidades o normalización; forma de arreglos; retorno; quién la llama; una comprobación. Diferencia `return`, `print` y guardar en disco. Explica una función interna y una lambda. Indica qué funciones calculan física y cuáles solo representan resultados.

La cadena `HTML` contiene JavaScript para selector, pausa, tiempo y dibujo. `opciones` llena escenarios; `cargar` muestra métricas; `dibujar` representa un cuadro; `ciclo` actualiza la reproducción; `texto` escribe etiquetas; `w` reconstruye el perfil; `perfil` dibuja la superficie y `linea` traza las curvas. Los manejadores de los controles cambian escenario, tiempo o pausa. No integran el movimiento. El objetivo obligatorio es explicar el modelo y las funciones Python; editar el visor JavaScript puede reservarse como ampliación.

`verificar_todos.py` tiene dos funciones de revisión docente: `verificar_perfil` comprueba centro, continuidad y decaimiento de la superficie; `main` ejecuta las nueve prácticas secuencialmente y registra el informe.

## Enlaces a las funciones compartidas


### motor_contacto.py

| Función | Ubicación |
|---|---|
| `paso_rk4` | [Línea 16](motor_contacto.py#L16) |
| `integrar_contacto` | [Línea 25](motor_contacto.py#L25) |
| `primitiva_velocidad` | [Línea 69](motor_contacto.py#L69) |
| `cuadratura_contacto` | [Línea 87](motor_contacto.py#L87) |
| `referencia_lineal` | [Línea 123](motor_contacto.py#L123) |
| `serie_inicial` | [Línea 135](motor_contacto.py#L135) |
| `completar_referencia` | [Línea 144](motor_contacto.py#L144) |
| `metricas_contacto` | [Línea 167](motor_contacto.py#L167) |
| `perfil_blanco` | [Línea 183](motor_contacto.py#L183) |
| `derivadas` | [Línea 35](motor_contacto.py#L35) |
| `evento` | [Línea 40](motor_contacto.py#L40) |
| `velocidad` | [Línea 102](motor_contacto.py#L102) |
| `acumular` | [Línea 116](motor_contacto.py#L116) |

### animaciones.py

| Función | Ubicación |
|---|---|
| `graficar_comparacion` | [Línea 17](animaciones.py#L17) |
| `preparar_serie` | [Línea 48](animaciones.py#L48) |
| `crear_paquete` | [Línea 61](animaciones.py#L61) |
| `guardar_visor` | [Línea 94](animaciones.py#L94) |
| `crear_gif` | [Línea 99](animaciones.py#L99) |
| `exportar_movimiento` | [Línea 137](animaciones.py#L137) |
| `cuadro` | [Línea 123](animaciones.py#L123) |

### verificar_todos.py

| Función | Ubicación |
|---|---|
| `verificar_perfil` | [Línea 8](verificar_todos.py#L8) |
| `main` | [Línea 21](verificar_todos.py#L21) |
