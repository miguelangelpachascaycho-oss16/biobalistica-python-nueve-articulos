# Caso 08 — penetración cooperativa de dos nanopartículas

**Categoría: penetración mecánica guiada; no biobalística libre.** El modelo molecular representa una bicapa lipídica y partículas movidas mediante resortes. Se incluye con la ampliación de tema autorizada por el docente.

Lectura: H. Zhang et al. (2015), *Cooperative Transmembrane Penetration of Nanoparticles*, Scientific Reports 5, 10525. [Artículo abierto y licencia CC BY 4.0](https://www.nature.com/articles/srep10525). [DOI 10.1038/srep10525](https://doi.org/10.1038/srep10525). [PDF institucional alternativo](https://sites.esm.psu.edu/wiki/_media/research%3Asuz10%3A2015_scientific-reports.pdf).

## Ejecutar y analizar

En la terminal de VS Code, desde la carpeta del repositorio:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe src/caso_08_cooperativa.py --animar
.\.venv\Scripts\python.exe pruebas/verificar_nuevos.py
```

Abre `resultados/caso_08/simulacion.gif`, `simulacion.png`, `metricas.csv` y `resumen.json`. Se muestran contacto, control con las dos NP fijas y rugosidad de la hoja superior. El agua participa en el cálculo y se omite del dibujo. El NPZ guarda estados de lípidos y cuerpos, sin copiar todas las posiciones del solvente.

Ejecuta el caso con una sola NP para comparar, conservando el primer resultado:

```powershell
.\.venv\Scripts\python.exe src/caso_08_cooperativa.py --numero-np 1 --salida resultados/caso_08_una_np --animar
```

## Correspondencia con el artículo

Se conserva el modelo de lípido **H2T5**, con dos beads de cabeza hidrofílica y cinco de cola hidrofóbica, agua explícita, DPD y resortes/ángulos. Las interacciones blandas tienen amplitud 25 entre caracteres iguales y 95 entre hidrofílicos/hidrofóbicos. Se elige estudiar las partículas hidrofílicas WNP del artículo. Se representan como cuerpos rígidos y se integra su traslación y rotación.

Los componentes DPD son repulsión `a_ij*(1−r/rc)`, fricción radial y ruido térmico por pares. El código usa `gamma=4.5`, `sigma=3`, con `sigma²=2*gamma*kBT` en unidades `rc=m=kBT=1`. La fuerza del resorte móvil sobre cada COM es `Fz=−ks*(zCOM−zancla)`, con `zancla=z0−Vs*t`. La reacción de cada contacto modifica las posiciones de la bicapa y de la NP.

**Decisiones docentes y límites:** el texto principal da constantes de enlace 128 y de flexión 15, pero no fija inequívocamente sus unidades, longitudes/ángulos de reposo ni la rigidez del resorte de guía. El ejercicio interpreta energías armónicas con factores 1/2, adopta `l0=0.5`, `theta0=pi`, `ks=40`, gamma y sigma indicados arriba; son decisiones complementarias, no valores verificados del artículo. El caso contiene 128 lípidos y dos esferas de 66 beads y radio aproximado 1.15 rc, frente a las esferas de diámetro 6 rc y caja 72×72×60 rc³ del artículo. La caja y duración están reducidas. No se calibra tensión cero ni se simulan todas las químicas WNP/ONP/JNP/RNP.

La preparación se realiza sin NP; después se insertan y se quita solamente agua superpuesta. Las ramas de contacto y control parten del mismo estado. La rama control también capta la relajación inducida por la inserción. El integrador es kick-drift de primer orden, distinto al utilizado en la publicación. **Se muestra contacto temprano y deformación; no se reproducen los 45 microsegundos ni las fases estadísticas de penetración del artículo.**

## Estructura del programa y funciones

El ejecutable llama a `simular` de `src/bicapa_dpd.py`.

| Función | Responsabilidad |
|---|---|
| `Parametros` | Registra artículo, caja, paso, velocidad de ancla y cantidad de NP |
| `plantilla` | Define tipos, enlaces, ángulos y constantes de un lípido H2T5 |
| `construir` | Construye las dos hojas, el agua, velocidades iniciales y topología |
| `interacciones` | Construye la matriz de repulsiones según química de beads |
| `angulos_fuerzas` | Deriva fuerzas de la energía angular y conserva fuerza/torque totales |
| `fuerzas` | Busca vecinos periódicos; suma DPD, enlaces y ángulos |
| `geometria_np` | Genera los beads de la esfera rígida |
| `insertar_np` | Añade NP y devuelve grupos, geometría e inercia de cada cuerpo |
| `paso_rigido` | Suma fuerza/torque, aplica el resorte móvil e integra COM y orientación |
| `altura_membrana` | Promedia alturas de cabezas por celda para medir heterogeneidad de forma |
| `simular` | Ejecuta preparación, contacto y control; guarda CSV, NPZ y parámetros |
| `dibujar` | Muestra el corte de las coordenadas calculadas y la curva de rugosidad |

## Límite analítico para aprender a programar

Suprime mentalmente solvente y membrana y conserva solo una NP de masa M y el resorte que se desplaza a velocidad Vs. Con `z(0)=z0` y `v(0)=0`:

```text
M*z'' + ks*(z−z0+Vs*t) = 0
omega = sqrt(ks/M)
z(t) = z0−Vs*t + Vs/omega*sin(omega*t)
```

Deriva la solución y explica por qué la partícula inicialmente no sigue instantáneamente al ancla. `pruebas/verificar_nuevos.py` contrasta este límite con el paso rígido y reduce dt. Es una solución deducida del resorte del modelo, no una solución cerrada de toda la bicapa.

## Copilot y defensa

Pide a Copilot que explique la diferencia entre velocidad del ancla y velocidad de NP, y que localice el torque producido por fuerzas que no pasan por el COM. Después analiza distancia entre NP y rugosidad para uno/dos cuerpos. Una diferencia entre dos trayectorias no demuestra por sí sola cooperación estadística: intervienen ruido térmico, hidrodinámica y tamaño de caja. Harían falta varios conjuntos de semillas y preparación convergente para contrastar el resultado publicado.

Entrega diagrama, derivación del resorte móvil, comparación una/dos NP, CSV, animación, control y mapa de funciones. Explica por qué la rugosidad no equivale a área de poro, deformación unitaria ni viabilidad celular, y señala todas las decisiones añadidas al artículo.

Para refinar dt sin cambiar la duración, duplica los pasos de ambas etapas:

```powershell
.\.venv\Scripts\python.exe src/caso_08_cooperativa.py --dt 0.0015 --preparar 3200 --pasos 5200 --semilla 2027 --salida resultados/caso_08_refinado
```

Repite con varias semillas y compara distribuciones: dos trayectorias con distinto ruido no tienen que superponerse punto por punto.
