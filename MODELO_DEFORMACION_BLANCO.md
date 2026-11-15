> **ARCHIVO AUXILIAR DE MECÁNICA DE CONTACTO. Las nueve actividades actuales comienzan en [README.md](README.md#empieza-aquí-actividad-para-alumnos).**

> **MATERIAL AUXILIAR ANTERIOR. Esta ficha no constituye una asignación de biobalística en células o tejidos. Consulta [la revisión vigente](REVISION_BIOBALISTICA.md).**

# Auxiliar: deformación en el modelo escalar de contacto

Los nueve casos resuelven **impacto normal e indentación del blanco**. La esfera se supone rígida y el blanco está fijo globalmente, pero su superficie puede desplazarse. En los artículos que estudian dos cuerpos se adopta este límite del contacto equivalente. No se conserva una escena de esfera deformándose contra una pared rígida.

## Salida dinámica

q(s)=δ(t)/L es la indentación central del blanco. La ODE produce su evolución, velocidad y reacción. Se calculan máximo, tiempo de contacto, fuerza máxima, restitución y energías. El centro de la esfera está en z=q−R/L, con z positivo hacia abajo. Antes del contacto se incluye aproximación libre uniforme, sin reacción y con blanco plano.

R/L=30 y `delta_sobre_R=q/30`. No se asignan tamaños, velocidades, módulos ni viscosidades de un organismo real. La actividad trabaja en escalas relativas y debe justificar cualquier conversión posterior a unidades físicas.

## Reconstrucción espacial declarada

Una ley escalar de contacto no determina por sí sola el desplazamiento de todos los puntos del blanco. Para visualizar una superficie se adopta la **reconstrucción axisimétrica cuasiestática de Hertz** parametrizada por δ(t). Es exacta dentro de esa aproximación elástica idealizada; para los modelos disipativos es una hipótesis espacial adicional, común y explícita. No se presenta como un resultado completo del campo viscoelástico de cada artículo.

Con a=√(Rδ), el desplazamiento superficial positivo hacia abajo es:

$$w(r)=\delta-\frac{r^2}{2R},\qquad 0\le r\le a,$$

$$w(r)=\frac{(2a^2-r^2)\arcsin(a/r)+a\sqrt{r^2-a^2}}{\pi R},\qquad r>a.$$

Se cumple w(0)=δ, continuidad en r=a y w→0 al alejarse. `perfil_blanco` implementa esta reconstrucción y recibe la indentación calculada. No aplica una oscilación ni una abolladura arbitraria para decorar la escena. La aproximación dentro del contacto coincide con el perfil parabólico local de la esfera para pequeñas indentaciones.

El perfil cuasiestático está relacionado con el contacto elástico de la ficha 01 y la aproximación espacial discutida por Brilliantov et al. en la ficha 06. Las leyes de fuerza y las adaptaciones concretas conservan su trazabilidad en las nueve fichas. El alumno debe reconocer esta diferencia entre ODE escalar y campo espacial.

## Cómo leer las vistas

- **Vista general:** esfera rígida y superficie del blanco con escalas geométricas iguales.
- **Contacto ampliado:** hace visible la pequeña indentación; usa escalas horizontal y vertical diferentes. No se interpreta como una fotografía a escala.
- **Curva sincronizada:** q(s) numérica y la referencia válida del caso. Una serie corta deja de dibujarse fuera de su ventana.

El paso de integración y la velocidad de reproducción son controles distintos. El CSV almacena los estados calculados, mientras el visor interpola cuadros para mostrar el movimiento.

## Qué se puede concluir

Se comparan indentación, reacción, energía y recuperación durante el contacto de los modelos elegidos. δ/R expresa indentación normalizada, **no** deformación unitaria local ε. Tampoco es una profundidad de perforación. No se calculan tensiones, daño, rotura de membrana, transfección, ondas ni un campo 3D de deformaciones de células.

Si la separación ocurre con δ>0, el contacto terminó antes de la recuperación completa. El último cuadro conserva ese estado y la animación termina allí; no se añade una recuperación posterior arbitraria ni se interpreta como una huella plástica permanente. Esa distinción forma parte de las prácticas 08 y 09.
