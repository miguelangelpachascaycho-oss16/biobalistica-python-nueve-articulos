# Alumno 07 — contacto con una membrana dipolar mínima

**Categoría: penetración mecánica activa, no biobalística.** El blanco es una cadena artificial de partículas dipolares que modela propiedades mecánicas de membranas; no una bicapa lipídica explícita. El docente autorizó incluir esta clase de modelo.

Lectura: A. Daddi-Moussa-Ider et al. (2019), *Membrane penetration and trapping of an active particle*, Journal of Chemical Physics 150, 064906. [DOI 10.1063/1.5080807](https://doi.org/10.1063/1.5080807). [Texto completo público de autores](https://user.thphy.uni-duesseldorf.de/hlowen/doc/op/op0397.pdf). [Versión abierta arXiv 1901.07359](https://arxiv.org/abs/1901.07359). No se redistribuye el PDF editorial; se enlazan las copias públicas.

## Ejecutar en VS Code

Si ya creaste `.venv` e instalaste `requirements.txt`, usa las dos últimas órdenes:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe caso_07_dipolar.py --animar
.\.venv\Scripts\python.exe verificar_nuevos.py
```

Abre `resultados/caso_07/simulacion.gif`, `simulacion.png`, `metricas.csv` y `resumen.json`. La vista de contacto amplía la zona central de la cadena; el tercer panel muestra su perfil completo. El radio dibujado corresponde al radio modelado. Las flechas representan orientaciones dipolares.

## Fuerzas publicadas

Las ecuaciones 1–11 suman energía dipolar, repulsión WCA y resortes opcionales. En dos dimensiones, cada dipolo tiene orientación `m_i=(cos(phi_i),sin(phi_i))`. Si `c=mu0*m²/(4*pi)`, la contribución dipolar por par es:

```text
Uij = c/r³ [m_i·m_j − 3(m_i·n)(m_j·n)]
F_i = −dU/dr_i
T_i = −dU/dphi_i
dr_i/dt = mu*(F_i + F_contacto)
dphi_i/dt = gamma*T_i
gamma/mu = 3/(4*a²)
```

La partícula de radio R recibe la reacción del contacto y F0, y se mueve con movilidad de Stokes `mu*a/R`. Se usa el corte `ell=1.5h` para interacciones dipolares y elásticas. Las WCA tienen sus propios radios de corte. El programa no incluye inercia ni ruido térmico.

El caso predeterminado conserva N=20, `h/a=2^(7/6)`, `R/a=1`, fuerza dipolar reducida E1=1 y actividad E2=0.01. Selecciona kappa=0: se estudia el caso sin resortes, gobernado por dipolos y WCA. Si se añadieran resortes en el motor, la conversión publicada es `k=24*c*kappa/h^5`. Ambos extremos permanecen fijos y sus dipolos se orientan a torque cero.

## Comparación analítica

Las ecuaciones 43a–b del artículo predicen, en pequeña deformación y estado estacionario:

```text
P0 = h^4*F0/(12*c)
rho(x) = P0*(L/2 − abs(x))
phi(x) = −P0*sign(x)
```

Deriva el perfil triangular resolviendo `rho''+2*P0*delta(x)=0`, con desplazamiento cero en los extremos. La carga puntual produce un salto de pendiente de `−2P0`. Esta fórmula se dibuja como comparación independiente: **la cadena de la animación se integra con las fuerzas no lineales**, no se obliga a seguir el triángulo.

El programa toma L como la distancia entre los centros de los apoyos, `(N−1)h`, frente a la convención `Nh` del texto. Esta diferencia finita y el contacto con dos beads explican parte de la discrepancia con el continuo. El valor predeterminado de fuerza corresponde al régimen pequeño; no se afirma reproducir todo el diagrama de penetración.

## Estructura y funciones

`caso_07_dipolar.py` lee argumentos y llama al motor `penetracion_activa.py`. Comparte `Parametros`, `construir`, `wca`, `fuerzas`, `referencia_analitica`, `simular` y `dibujar` con el caso 06, pero activa **una energía dipolar y grados de libertad angulares distintos**. `orientar_extremos` impone torque cero alineando cada dipolo extremo con el campo de su vecino. `rhs` convierte fuerzas y torques en velocidades lineales y angulares; LSODA integra ambos campos. `fuerzas` entrega también la reacción sobre el intruso. Las pruebas independientes comprueban tanto fuerza como torque contra derivadas de energía.

El integrador tiene un paso máximo: en vuelo libre, una ecuación casi lineal puede permitir un paso tan grande que la partícula salte sobre toda la región de contacto. Explica por qué el mensaje «success» del integrador no detectaría por sí mismo ese error físico.

## Actividad con Copilot

Solicita: «Deriva el torque a partir de la energía de dos dipolos en 2D; explica qué cambia al rotar uno sin mover sus centros». Luego pide la deducción del perfil triangular y verifica cada signo. Repite el ensayo con una fuerza menor:

```powershell
.\.venv\Scripts\python.exe caso_07_dipolar.py --fuerza 0.005 --salida resultados/caso_07_menor --animar
```

Entrega comparación de perfiles normalizados y error respecto al continuo, CSV, animación y explicación oral de torque, movilidad y condiciones de borde. El control sin fuerza es inmóvil y se verifica en `VERIFICACION_NUEVOS.json`. No confundir el modelo dipolar artificial con una célula ni el movimiento activo sobreamortiguado con balística inercial.
