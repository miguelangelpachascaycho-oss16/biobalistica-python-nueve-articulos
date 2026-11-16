# Implementar la actividad en Visual Studio Code con GitHub Copilot

## 1. Encuentra tu nombre y descarga el proyecto

En el [inicio del repositorio](../README.md#actividades-asignadas), abre la ficha junto a tu nombre. Anota el **número del caso**. Las carpetas de `casos/` llevan número y nombre; el número identifica el modelo y puede no coincidir con tu posición en la lista.

Desde la página principal de GitHub, pulsa **Code → Download ZIP**. Extrae el ZIP. Abre VS Code y selecciona **File → Open Folder** sobre la carpeta que contiene `README.md`, `requirements.txt`, `ejecutar_caso.py`, `src/` y `casos/`. Trabaja en la carpeta extraída, no dentro del ZIP ni abriendo solo un `.py`.

## 2. Prepara Python y VS Code

Instala Python 3.11 o posterior desde [Python](https://www.python.org/downloads/) y [Visual Studio Code](https://code.visualstudio.com/). En **Extensions**, instala **Python**, de Microsoft; VS Code y su extensión no sustituyen al intérprete Python. [Configuración oficial de Python](https://code.visualstudio.com/docs/python/python-tutorial).

Abre **Terminal → New Terminal**. Los comandos siguientes son para PowerShell en Windows, ejecutados desde la raíz del proyecto:

```powershell
py --version
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -c "import numpy, scipy, matplotlib, PIL; print('Dependencias OK')"
```

Si `py` no existe y `python --version` funciona, reemplaza `py` por `python` en las dos primeras líneas. Luego pulsa **Ctrl+Shift+P**, busca **Python: Select Interpreter** y selecciona `.venv\Scripts\python.exe`. Usar directamente ese ejecutable evita tener que cambiar la política de PowerShell.

## 3. Configura Copilot como tutor

Abre el menú del icono de Copilot en VS Code y elige **Use AI Features** o **Sign in to use Copilot**, según la versión. Inicia sesión con tu propia cuenta de GitHub y sigue las indicaciones de acceso. Comprueba que puedes abrir su chat y obtener una explicación del archivo abierto. [Configuración oficial de Copilot](https://code.visualstudio.com/docs/setup/copilot).

El cálculo científico se ejecuta con Python. Copilot necesita acceso al servicio para la tutoría; su disponibilidad y límites dependen de la cuenta. Puedes ejecutar y comprobar el programa aunque el chat no esté disponible.

## 4. Ejecuta primero la referencia de tu caso

```powershell
.\.venv\Scripts\python.exe ejecutar_caso.py --listar
```

Busca tu nombre. Copia de tu ficha el comando correspondiente. Por ejemplo, el caso 01 se ejecuta con:

```powershell
.\.venv\Scripts\python.exe ejecutar_caso.py 1 --animar
```

Sustituye `1` por tu caso asignado. La ficha indica el directorio exacto de salida dentro de `resultados/`, el programa de `src/`, el motor y el verificador. Ejecuta un caso cada vez; algunas simulaciones DPD y la generación del GIF tardan varios minutos. Espera a que vuelva el indicador de la terminal y comprueba los archivos, no solo la última imagen.

## 5. Comprende la estructura antes de crear tu versión

Abre el programa señalado en tu ficha. Sigue sus imports hasta el motor compartido cuando corresponda. Dibuja el flujo y explica:

| Parte | Pregunta que debes contestar |
|---|---|
| Parámetros y geometría | ¿Qué representa cada dato, qué unidad tiene y cuál es el estado inicial? |
| Fuerzas y energía | ¿Qué ecuación del artículo se implementa y dónde aparece la reacción sobre el blanco? |
| Integración | ¿Qué estado se actualiza y cómo se usa el tiempo? |
| Observables | ¿Cómo se mide deformación y cómo se distingue del movimiento rígido? |
| Archivos y animación | ¿Qué datos se guardan y cómo llegan esos mismos estados al dibujo? |

En cada función identifica argumentos, retorno, forma de los arreglos y quién la llama. Usa [el mapa de funciones](EXPLICACION_FUNCIONES.md) y la guía de tu modelo.

## 6. Construye y comprueba tu implementación

Deduce primero el subproblema analítico de tu ficha. Escribe hipótesis, ecuaciones, unidades y condiciones iniciales o de borde. Después guarda una copia del programa principal **dentro de `src/`** con el nombre `mi_caso_NN.py`, sustituyendo `NN` por tu número con dos dígitos. Conserva los motores compartidos.

Pide ayuda por etapas, por ejemplo:

> «Explícame esta función y luego pregúntame por sus entradas, unidades y retorno. Espera mi explicación antes de avanzar».

> «Esta es mi deducción analítica. Comprueba signos e hipótesis y ayúdame a implementarla en una función pequeña; no generes todo el programa».

> «Propón un control capaz de revelar un error físico aunque la animación se vea bien. Indica qué cantidad debo comparar».

La ficha contiene el comando de tu copia, su carpeta de salida y el verificador. Revisa cada cambio antes de aceptarlo, ejecuta la comprobación y registra el resultado. Para depurar, coloca un punto de interrupción en una función, selecciona el intérprete `.venv` y usa **Run and Debug → Python Debugger → Python File**, o la opción equivalente de tu versión. Inspecciona una llamada y sus variables; si el programa necesita argumentos, usa los de tu ficha en la configuración de depuración. [Depuración de Python](https://code.visualstudio.com/docs/python/debugging).

No atribuyas al artículo un parámetro añadido por el ejercicio. Una referencia analítica de un límite no resuelve necesariamente toda la membrana ni valida biológicamente el modelo.

## 7. Revisa las salidas y entrega

Abre tu GIF, curvas, CSV y parámetros. Compara un mismo instante en datos y animación. Ejecuta el control y la comprobación analítica indicados en tu ficha. Explica si el cambio observado es deformación, desplazamiento rígido, fluctuación térmica o rotura de enlaces del modelo.

Entrega tu código, mapa de funciones, derivación, parámetros, CSV, curvas, animación y registro breve de ayudas de Copilot. Conserva la misma rúbrica del grupo. Debes explicar sin el chat qué realiza cada función y justificar el resultado.

## Si aparece un error

| Mensaje o situación | Qué revisar |
|---|---|
| No se encuentra `requirements.txt` o `ejecutar_caso.py` | La terminal debe estar en la raíz de la carpeta extraída. |
| `ModuleNotFoundError: numpy/scipy/matplotlib/PIL` | Instala las dependencias con `.\.venv\Scripts\python.exe -m pip install -r requirements.txt` y usa ese intérprete. |
| No se encuentra un motor del proyecto | Mantén la copia `mi_caso_NN.py` dentro de `src/` y conserva el resto de archivos. |
| Copilot no responde | Revisa la sesión y el acceso de tu cuenta; continúa ejecutando las verificaciones locales. |
| Solo ves el GIF descargado | La vista pregenerada no sustituye tu ejecución; comprueba los archivos nuevos de `resultados/`. |
