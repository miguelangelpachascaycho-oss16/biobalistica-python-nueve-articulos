# Dos artículos distintos: impacto sobre una célula completa

Estas implementaciones amplían el piloto de bicapa plana con una célula cerrada en 2D. Son **reducciones didácticas de los modelos físicos**, con deformación nodal calculada. No reproducen las figuras, porcentajes de entrega ni tablas completas de los artículos.

## Artículo C01

Campello y Zohdi (2014), *A computational framework for simulation of the delivery of substances into cells*, [DOI 10.1002/cnm.2649](https://doi.org/10.1002/cnm.2649). [Texto del autor alojado por Berkeley](https://msol.berkeley.edu/wp-content/uploads/2025/11/108.pdf).

Se implementan la bicapa circular y sus enlaces circunferenciales, radiales y cruzados; contacto, presión seguidora, arrastre y ruptura. Se utiliza la célula pequeña de diámetro externo 100 nm, espesor 10 nm y las propiedades de su sección 5. Las velocidades de estudio son 50, 100 y 150 nm/ns.

La malla de 90 nodos por capa y el chorro de 12 partículas son elecciones docentes. El artículo utiliza chorros mucho más numerosos. El tiempo por defecto se limita a 2 ns; el estudio publicado llega a 15 ns. La integración RK2 y el recorte unilateral del contacto son diferencias declaradas. Un resultado de entrega de esta reducción no se compara directamente con los porcentajes publicados.

```powershell
.\.venv\Scripts\python.exe src/caso_celular_01.py --velocidad 100 --animar
.\.venv\Scripts\python.exe src/caso_celular_01.py --control --salida resultados/control_01 --animar
```

## Artículo C02

Campello y Zohdi (2014), *Design Evaluation of a Particle Bombardment System Used to Deliver Substances into Cells*, [DOI 10.3970/cmes.2014.098.221](https://doi.org/10.3970/cmes.2014.098.221). [Texto del autor alojado por Berkeley](https://msol.berkeley.edu/wp-content/uploads/2025/11/109.pdf).

Se conserva dinámica celular en cada muestra. Cambian radio externo (60 nm), presión interna y umbrales de ruptura según el artículo. Los diámetros dentro del chorro siguen una distribución normal con desviación estándar igual al 10 % de su media. El muestreo docente cambia diámetro medio, velocidad y ancho del chorro con semilla reproducible.

Los rangos de entrada de este ejemplo, las 3 muestras y el chorro reducido son elecciones docentes. El programa no reproduce los 400 problemas ni las correlaciones publicadas. El indicador `DAM` suma la deformación actual de los enlaces rotos, siguiendo la ecuación 35; no tiene que ser monótono ni equivale a una variable de daño calibrada. Si el contorno circunferencial está roto, la fracción interior se registra como `NaN`: no se trata una membrana abierta como célula sellada.

```powershell
.\.venv\Scripts\python.exe src/caso_celular_02.py --muestras 3 --semilla 42 --animar
```

Las copias de los autores permiten consultar los textos; no se declara que esos artículos tengan licencia Creative Commons ni se redistribuyen sus PDF.

## Instalación y archivos

Desde la carpeta del repositorio:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

En VS Code selecciona ese entorno con **Python: Select Interpreter**. Cada caso necesita `src/celula_dem.py` y `src/piloto_membrana.py` en la misma carpeta; de este último solo reutiliza las funciones de fuerzas, sin ejecutar su programa principal.

Cada ejecución produce `estados.npz`, `parametros.json`, `metricas.csv` y, con `--animar`, `impacto.gif` y `impacto.png`. En C02 se crea una carpeta por muestra, más `muestras.csv` y `resumen.json`. Las muestras se ejecutan en secuencia. Los parámetros `--tiempo` y `--dt` permiten estudiar duración y convergencia.

## Ecuaciones y estructura del código

Las dos prácticas comparten un marco físico; sus artículos son distintos. Cada nodo se mueve por `m dv/dt = F_enlaces + F_contacto + F_pared + F_presion - c_env v` y `dx/dt=v`. La fuerza de enlace es axial, con resorte y amortiguador. Los contactos entre partículas y con la pared son repulsivos y amortiguados.

| Función | Qué realiza |
|---|---|
| `crear_celula` | Construye dos anillos, cinco conexiones por nodo, masas y chorro |
| `normales_internas` | Calcula la dirección actual de la presión a partir de vecinos |
| `fuerza_pared` | Calcula la reacción y la fricción de la pared rígida |
| `interior_poligono` | Evalúa geométricamente qué centros están dentro de un contorno cerrado |
| `simular_celula` | Integra posiciones y velocidades, rompe enlaces y calcula indicadores |
| `guardar_celula` | Exporta estados, parámetros y métricas |
| `animar_celula` | Dibuja esferas y enlaces a partir de los estados calculados |
| `main` de C01 | Conecta opciones, configuración de un impacto y exportación |
| `main` de C02 | Genera parámetros, ejecuta muestras y resume los resultados |

Los radios de las esferas están en unidades geométricas del dibujo. La curva muestra desplazamiento máximo respecto de la configuración inicial; no equivale a deformación unitaria ni elimina el efecto de la presión. La deformación de cada enlace se calcula como `L/L0-1`. Las partículas no giran; las limitaciones de esa hipótesis y de la fricción deben discutirse.

## Aprendizaje analítico y verificación

Antes del contacto, cada proyectil solo experimenta arrastre lineal. Con `tau=m/c_env`:

```text
v(t) = v0 exp(-t/tau)
x(t) = x0 + v0 tau [1-exp(-t/tau)]
```

Deriva ambas relaciones y compáralas con el tramo inicial de la solución. Para un enlace aislado usa la solución amortiguada explicada en [PILOTO_MEMBRANA.md](PILOTO_MEMBRANA.md). Ninguna de estas fórmulas representa la solución cerrada de la célula completa.

```powershell
.\.venv\Scripts\python.exe pruebas/verificar_celulas.py
```

La comprobación incluye cinco enlaces por nodo, sentido de las normales, balance de fuerzas internas, invariancia ante traslación, vuelo libre analítico, comparación al reducir `dt` a la mitad y control sin proyectiles. Los errores se registran en `pruebas/evidencia/VERIFICACION_CELULAS.json`. El refinamiento se comprueba hasta 0.3 ns; no constituye validación de los resultados a tiempos mayores, de la ruptura, de la malla espacial ni de células reales.

## Trabajo y defensa con Copilot

1. Dibuja el grafo de dependencias entre el programa principal y las funciones. Explica cada array y sus unidades.
2. Pide a Copilot que derive el vuelo libre y comprueba signos y condiciones iniciales.
3. Ejecuta impacto y control; identifica cuánto cambia el blanco por la presión antes de la llegada de los proyectiles.
4. Explica por qué los enlaces cruzados acoplan la flexión de las dos capas y cómo difieren los umbrales de ambos artículos.
5. En C01 compara las tres velocidades. En C02 repite una semilla y después cámbiala; conserva parámetros y resultados.
6. Explica por qué unas pocas muestras no bastan para inferir correlaciones y por qué un contorno roto impide interpretar el indicador interior como entrega celular validada.

La defensa debe incluir una modificación razonada, la comparación analítica y una limitación del modelo. Copilot es apoyo para comprender y revisar; las afirmaciones sobre el artículo se cotejan con sus ecuaciones.
