> **ARCHIVO AUXILIAR DE MECÁNICA DE CONTACTO. Las nueve actividades actuales comienzan en [README.md](README.md#empieza-aquí-actividad-para-alumnos).**

# Auxiliar: soluciones analíticas de contacto

Una animación muestra resultados; la solución comienza al escribir y analizar las ecuaciones. Esta guía desarrolla las relaciones usadas por las nueve prácticas. Las deducciones intermedias son desarrollo docente, identificado como tal, a partir de las leyes enlazadas en cada ficha.

## Variables, signos y escalas

La esfera se considera rígida y el blanco fijo pero deformable. La indentación del blanco es δ≥0, positiva hacia su interior. Durante el contacto v=δ̇: v>0 comprime y v<0 descarga. La reacción F es positiva al comprimir y actúa contra el movimiento de aproximación:

$$m\ddot\delta=-F(\delta,\dot\delta),\qquad \delta(0)=0,\quad\dot\delta(0)=v_0.$$

Con longitud docente L, define q=δ/L, s=tv₀/L y velocidad relativa u=δ̇/v₀. La fuerza de referencia es mv₀²/L y la energía de referencia mv₀². En el código la columna `v` contiene u y las constantes están normalizadas: m=v₀=1. El radio satisface R/L=30. Por tanto `delta_sobre_R=q/30`; no es una deformación unitaria local.

## 01 · Hertz: energía y tiempo por cuadratura

La referencia elástica de [Argatov (2024), ecuaciones (1)-(6)](https://www.mdpi.com/2075-4442/12/6/193) usa una fuerza de potencia, F=kqⁿ, con n=3/2. Multiplica q″=−kqⁿ por q′ e integra:

$$\frac{u^2}{2}+\frac{kq^{n+1}}{n+1}=\frac12.$$

En la máxima indentación u=0:

$$q_m=\left(\frac{n+1}{2k}\right)^{1/(n+1)}=\left(\frac{5}{4k}\right)^{2/5}.$$

La rama de compresión tiene u(q)=+√[1−(q/qₘ)ⁿ⁺¹]; la descarga lleva signo negativo. El tiempo total es

$$s_c=2q_m\int_0^1\frac{dx}{\sqrt{1-x^{n+1}}}.$$

La relación es analítica exacta; evaluar la integral y reconstruir q(s) por cuadratura es un procedimiento **semianalítico**, independiente de RK4. No hay una fórmula elemental general de q(s). La restitución ideal es 1.

Para regularizar la cuadratura cerca de la máxima indentación, el código usa q=qₘ sin θ en carga y q=qₘ cos θ en descarga. Allí tanto dq/dθ como u tienden a cero, pero su cociente tiene el límite finito √[qₘ/F(qₘ)]. Esa es la razón de calcular el último valor de la integranda por un límite, en vez de dividir 0/0.

## 02–04 · Ley tipo Hunt–Crossley: primera integral

Las fichas 02, 03 y 04 asignan **artículos diferentes** y elecciones diferentes del amortiguamiento. Comparten la estructura F=kqⁿ(1+βu). Se compara la ley original de [Hunt y Crossley](https://doi.org/10.1115/1.3423596), la aproximación de [Lankarani y Nikravesh, ecuación (27)](https://www.researchgate.net/publication/230554857_A_Contact_Force_Model_With_Hysteresis_Damping_for_Impact_Analysis_of_Multibody_Systems) y la propuesta para materiales blandos de [Flores et al., ecuación (44)](https://www.researchgate.net/publication/225871744_On_the_continuous_contact_force_models_for_soft_materials_in_multibody_dynamics).

Usa u′=u du/dq y separa:

$$\frac{u}{1+\beta u}\,du=-kq^n\,dq.$$

Una primitiva que se anula en u=0 es

$$H(u)=\frac{\beta u-\ln(1+\beta u)}{\beta^2},\qquad H'(u)=\frac{u}{1+\beta u}.$$

Luego:

$$H(u)+\frac{kq^{n+1}}{n+1}=H(1).$$

De aquí se obtienen qₘ=[(n+1)H(1)/k]¹⁄⁽ⁿ⁺¹⁾ y la restitución e resolviendo **H(−e)=H(1)** en la rama de descarga, con 1−βe>0. La curva completa se reconstruye resolviendo u(q) e integrando ds=dq/u, sin integrar nuevamente la ODE.

- Alumno 02: β es el parámetro de práctica.
- Alumno 03: β=3(1−e_obj²)/4.
- Alumno 04: β=8(1−e_obj)/(5e_obj).

En 03 y 04 `e_obj` entra en una aproximación del amortiguamiento. **No se impone la velocidad final**: la integración produce `e_calculado`, que puede diferir. Esa diferencia no es automáticamente error numérico. Deriva esta primera integral con tus palabras y comprueba la derivada de H antes de programarla.

Cuando β→0, H(u)→u²/2 y se recupera Hertz. `primitiva_velocidad` usa una serie corta para evitar restar números casi iguales cerca de cero.

## 05 · Ley exponencial: otra primitiva exacta

La [sección 4 de Carvalho y Martins (2019)](https://www.sciencedirect.com/science/article/pii/S0094114X19302332) introduce F=k exp(ηu)qⁿ. Al separar variables aparece u exp(−ηu) du. La deducción docente da:

$$H(u)=\frac{1-(1+\eta u)e^{-\eta u}}{\eta^2},\qquad H'(u)=u e^{-\eta u}.$$

La primera integral conserva la forma H(u)+kqⁿ⁺¹/(n+1)=H(1). Se calculan qₘ y e como en el bloque anterior, usando esta otra H. El código evalúa raíces y cuadraturas: es una referencia semianalítica, no una segunda ejecución de RK4. La fuerza permanece positiva para q>0. Comprueba además el límite η→0.

## 06 · Serie de tiempo corto y su error

La ley normal de [Brilliantov et al. (1996), ecuación (24)](https://arxiv.org/html/cond-mat/0203598) conduce, en las escalas elegidas, a:

$$q''=-q^{3/2}-d\sqrt q\,q',\qquad q(0)=0,\quad q'(0)=1.$$

Para tiempos pequeños, parte de q≈s y q′≈1. Sustituye en el segundo miembro e integra dos veces:

$$q(s)\approx s-\frac{4d}{15}s^{5/2}-\frac4{35}s^{7/2}.$$

Esta es una **aproximación docente**, no la solución temporal completa. Se omiten términos superiores, incluidos términos con d². Solo se dibuja hasta s=0.12. Acorta esa ventana y compara el error. Fuera de ella las columnas de referencia quedan vacías: no se prolonga la curva como si fuera válida.

## 07 · Una predicción analítica de restitución

[Ramírez et al. (1999), ecuación (6)](https://arxiv.org/html/cond-mat/9905382), obtienen una expansión para disipación pequeña. Con k=m=v₀=1 y χ como coeficiente de √q q′:

$$e_1=1-1.15344\chi,\qquad e_2=1-1.15344\chi+0.79826\chi^2.$$

Compara órdenes 1 y 2 con la integración. La expansión original usa retorno a q=0; la animación usa separación sin atracción. Se guardan ambas restituciones numéricas y se genera `restitucion_analitica.png`. Así puedes separar error de truncamiento, cambio de criterio de separación y error del integrador. Una expansión de e no es una solución temporal cerrada de q(s).

## 08 · Separación antes de recuperar la forma

[Schwager y Pöschel (2008), ecuaciones (7)-(8)](https://arxiv.org/html/0708.1434) distinguen el final del contacto de la recuperación completa. Para la fuerza F=√q(q+d u), durante la descarga se pierde el contacto cuando

$$q_c+d u_c=0,\qquad u_c<0.$$

La indentación puede ser positiva en ese momento. Continuar hasta q=0 con la fuerza firmada puede introducir atracción artificial. Compara ambos criterios, comprueba la relación algebraica y el balance de energía. También se incluye la serie inicial y el límite elástico. **No se afirma una solución temporal elemental general ni se inventa la recuperación posterior del blanco.**

## 09 · Solución temporal cerrada

El modelo lineal analizado por [Schwager y Pöschel (2007), sección 3](https://arxiv.org/html/cond-mat/0701278) permite aprender primero el caso completo más sencillo:

$$q''+2\zeta q'+q=0,\qquad 0<\zeta<1.$$

Con ω=√(1−ζ²):

$$q(s)=e^{-\zeta s}\frac{\sin(\omega s)}\omega,$$

$$u(s)=e^{-\zeta s}\left[\cos(\omega s)-\frac\zeta\omega\sin(\omega s)\right].$$

El final correcto satisface q+2ζu=0 al descargar. Para los valores subcríticos de esta práctica:

$$s_c=\frac{\operatorname{atan2}(2\zeta\omega,2\zeta^2-1)}\omega,\qquad e=-u(s_c).$$

Usar atan sin seleccionar la rama puede devolver un tiempo incorrecto. Compara con el medio período π/ω, que permitiría atracción al final. Aquí sí se dispone de q(s), u(s) y s_c cerrados.

## Comprobaciones compartidas

El integrador incorpora la energía disipada mediante W′=(F−F_el)u, donde U=kqⁿ⁺¹/(n+1). Durante el contacto debe cumplirse:

$$\tfrac12u^2+U+W=\tfrac12.$$

Reducir el paso comprueba resolución numérica; variar el orden o la ventana de una serie comprueba aproximación analítica. Ninguna de estas comprobaciones valida propiedades de un tejido. Debes conocer qué ley elegiste y qué comportamiento deja fuera.
