# Caso 09 — contacto de un nanotetraedro con una bicapa DOPC

**Categoría: interacción y penetración mecánica de nanoplásticos; no una pistola génica.** El blanco es una bicapa molecular idealizada de membrana celular. Su inclusión responde a la ampliación de tema autorizada por el docente.

Lectura: X. Yong y K. Du (2023), *Effects of Shape on Interaction Dynamics of Tetrahedral Nanoplastics and the Cell Membrane*, Journal of Physical Chemistry B 127, 1652–1663. [DOI 10.1021/acs.jpcb.2c07460](https://doi.org/10.1021/acs.jpcb.2c07460). [Texto completo público en NSF PAR](https://par.nsf.gov/servlets/purl/10447218). [Versión abierta arXiv 2210.11555](https://arxiv.org/abs/2210.11555). [Configuraciones y programas de autores, GPLv3](https://github.com/SaIL-Yong/nanotetrahedra). Se enlazan las fuentes; este repositorio no redistribuye sus scripts ni el PDF editorial.

## Ejecutar en VS Code

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe src/caso_09_tetraedro.py --animar
.\.venv\Scripts\python.exe pruebas/verificar_nuevos.py
```

Consulta `resultados/caso_09/simulacion.gif`, `simulacion.png`, `metricas.csv`, `parametros.json` y `resumen.json`. La rama de control conserva la NP fija. La curva mide variación de altura de cabezas de la hoja inicialmente superior, quitando altura media mediante desviación estándar. No equivale a deformación local de área ni a daño biológico.

## Modelo publicado que se conserva

La molécula DOPC tiene 14 beads con arquitectura **H2E2(C5)2**: cabezas, gliceroles y dos colas. Se incluyen fuerzas DPD, resortes y ángulos. El enlace usa `U=1/2*256*(r−0.5)^2`. La flexión usa `U=1/2*Ka*(theta−theta0)^2`, con Ka=20 en segmentos ordinarios y Ka=36, theta0=120° en ángulos cis; los ordinarios tienen theta0=180°. La topología H–E–E y su ángulo especial se cotejaron con las configuraciones de autores: se usa Ka=20, theta0=120° para ese triplete, como en su script LAMMPS.

Las repulsiones son 25 para tipos iguales, 100 entre H/W y C/P, y 35 entre E y C/P. Se excluyen DPD entre vecinos enlazados. No se excluyen segundos vecinos. Se usa gamma=4.5 y sigma=3, consistentes con el código de autores y la relación correcta `sigma²=2*gamma*kBT`; la relación escrita en el manuscrito presenta los símbolos intercambiados.

La NP es un tetraedro FCC de **56 beads**, con arista aproximada 3.08 rc y constante de red 0.87 rc, correspondiente al tamaño publicado 3.1 rc. Se integra como cuerpo rígido: posiciones internas constantes, traslación vertical y rotación libre, con fuerza y torque calculados por las interacciones. La velocidad inicial −5 rc/tau se cotejó en `short_time_dynamics.script` de autores. **Después del lanzamiento no hay fuerza activa ni ancla de velocidad constante en este caso.**

## Reducciones importantes

El artículo usa una membrana grande de 4608 lípidos, barostato de presión normal/tensión durante la preparación y millones de pasos. El ejercicio usa 128 lípidos en una caja pequeña, NVT y una preparación breve construida de nuevo; no importa la configuración equilibrada original. Utiliza kick-drift de primer orden en vez de velocity-Verlet. La preparación y el contacto observados son exploratorios: **no representan equilibrio termodinámico ni los estados finales de inserción/difusión descritos por el artículo**. No se copian a esta reducción sus conversiones calibradas de rc=0.689 nm y tau=154 ps.

Se estudia únicamente contacto temprano de un tetraedro pequeño. No se simulan los tamaños 5.6, 8.0 y 10.5 rc, arresto dinámico prolongado ni coeficientes de difusión. Los movimientos laterales del COM están restringidos, como en las simulaciones de tiempo corto del artículo; la rotación permanece libre.

## Funciones que debes explicar

`src/caso_09_tetraedro.py` lee argumentos y llama a `simular` en `src/bicapa_dpd.py`. Las funciones comunes están descritas en [el mapa del caso 08](CASO_08.md), pero aquí `plantilla` cambia a 14 beads, `interacciones` incorpora glicerol/hidrofobicidad, `geometria_np` construye el tetraedro FCC, y `paso_rigido` elimina el resorte de guía y aplica la restricción lateral.

En `paso_rigido`, explica estas operaciones:

```text
F = suma(F_bead)
torque = suma((r_bead−COM) × F_bead)
V_nueva = V + dt*F/M
L_nuevo = L + dt*torque
omega = Q * I_cuerpo^(-1) * Q^T * L
Q_nueva = exp(dt*[omega]_cruz) * Q
r_bead = COM + Q*b_bead
```

Q es una matriz de orientación; L es momento angular, distinto de omega. La exponencial de una matriz antisimétrica se evalúa mediante la rotación de Rodrigues de SciPy. Mantener las distancias internas evita que la NP se deforme al recibir fuerzas desiguales.

## Referencias analíticas y Copilot

Un tetraedro regular tiene tensor de inercia isotrópico respecto a su centro. Sin torque, su omega es constante y `Q(t)=exp(t*[omega]_cruz)*Q(0)`. El verificador comprueba esta rotación libre y la traslación sin fuerzas, además de `F=−grad(U)`, disipación y acción/reacción.

Para dos beads aislados unidos por un enlace, sin otros términos, deriva `omega_bond=sqrt(2*Kb/m)` y `r(t)=l0+(r0−l0)*cos(omega_bond*t)` para partida en reposo. Este límite no describe toda la membrana; sirve para comprobar la implementación de su ley de enlace.

Pide a Copilot una explicación de cada producto matricial y del torque, y compruébala con una fuerza aplicada por el COM y otra fuera del COM. Entrega derivaciones, parámetros, CSV, animación, control y explicación oral. Distingue desplazamiento del intruso, cambio de forma de la bicapa, rotación rígida, ruido y difusión. No interpretes el ensayo breve como evidencia de nanotoxicidad o reproducción de las conclusiones del artículo.

Para refinar el paso conservando tiempos de preparación y observación:

```powershell
.\.venv\Scripts\python.exe src/caso_09_tetraedro.py --dt 0.001 --preparar 3200 --pasos 5200 --semilla 2027 --salida resultados/caso_09_refinado
```

Es necesario repetir conjuntos de semillas para contrastar distribuciones. No atribuyas a dt una diferencia causada por reducir simultáneamente la duración del ensayo.
