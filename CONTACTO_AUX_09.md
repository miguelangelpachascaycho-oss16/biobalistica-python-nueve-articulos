> **MATERIAL AUXILIAR ANTERIOR. Esta ficha no constituye una asignación de biobalística en células o tejidos. Consulta [la revisión vigente](REVISION_BIOBALISTICA.md).**

# Alumno 09 · Impacto y deformación del blanco

## Artículo distinto asignado

**Schwager y Pöschel (2007). Coefficient of restitution and linear–dashpot model revisited.** Granular Matter 9, 465-469. [DOI 10.1007/s10035-007-0065-z](https://doi.org/10.1007/s10035-007-0065-z).

[Lectura](https://arxiv.org/html/cond-mat/0701278). Texto completo de autores en arXiv.

**Localización:** Sección 3, solución del oscilador y ecuaciones (17)-(21), condición de separación y restitución.

**Ley que vas a representar:** `δ''+2ζδ'+δ=0, δ(0)=0, δ'(0)=1; separación cuando δ+2ζδ'=0`.

**Adaptación declarada:** Modelo escalar fenomenológico de contacto, aplicado a esfera rígida y blanco deformable fijo. No se presenta como ley constitutiva de una célula.

Todos los casos de esta edición calculan la indentación del **blanco deformable**, con esfera rígida. Se trabaja en coordenadas relativas y con propiedades docentes. No son calibraciones de células ni reproducciones completas de los experimentos del artículo. Consulta [cómo se dibuja y qué se mide](MODELO_DEFORMACION_BLANCO.md).

## Construir la simulación analítica

Solución temporal cerrada δ=e^(-ζt)sin(ωt)/ω, ω=sqrt(1-ζ²), y tiempo de separación mediante atan2.

**Tu derivación individual:** Deducir la solución del oscilador y seleccionar la rama correcta del tiempo de separación. Comparar con el criterio erróneo de medio período.

Consulta [las deducciones y límites](SOLUCIONES_ANALITICAS.md). Identifica si tu resultado es cerrado, implícito, semianalítico o una aproximación. No presentes una integración numérica como solución analítica.

## Paso a paso en VS Code

1. Sigue la [instalación común](README.md#instalación-y-ejecución). Conserva `motor_contacto.py` y `animaciones.py` junto al programa.
2. Antes de ver el ejemplo, dibuja la esfera, el blanco y las fuerzas. Define δ, v, m, la reacción y la convención de signos.
3. Escribe `m δ''=-F(δ,δ')`, las condiciones iniciales y la condición de separación. Desarrolla a mano tu relación analítica.
4. Crea tu propio `mi_simulacion_09.py` siguiendo [Aprende a construir](APRENDE_A_CONSTRUIR.md). Primero implementa el cálculo de F; comprueba un valor a mano. Luego construye la referencia analítica de tu caso.
5. Ejecuta la referencia preparada para contrastar tu implementación:

   ```powershell
   .\.venv\Scripts\python.exe simulacion_09.py --escenario A --verificar --animar
   ```

6. Abre `resultados/alumno_09/visor.html`: reproduce, pausa y cambia el tiempo. Observa cómo la esfera desplaza la superficie del blanco. La curva de δ(t) usa exactamente el mismo estado que la escena.
7. Ejecuta los tres escenarios:

   ```powershell
   .\.venv\Scripts\python.exe simulacion_09.py --escenario todos --verificar --animar
   ```

8. El parámetro `zeta` toma A=0.05, B=0.15, C=0.3. Predice qué pasará con la indentación máxima, la fuerza, la restitución y la energía antes de compararlos.
9. Abre `comparacion.png`, `metricas.json` y los CSV. Explica el error numérico frente a la referencia y el error de aproximación cuando corresponda. Un vacío en las columnas de referencia significa que la serie ya está fuera de su ventana de validez.
10. Reduce el paso a la mitad con `--paso 0.001`, cambia `--salida resultados/mi_refinamiento_09` y compara. Distingue resolución del integrador y número de cuadros del GIF.
11. Implementa tu reto personal y ejecuta tu archivo desde una terminal nueva. Explica cada función sin leer respuestas de Copilot.

## Funciones que debes explicar

| Función | Propósito |
|---|---|
| [`parametros_escenario`](simulacion_09.py#L20) | Transforma el parámetro del escenario en constantes de la ley. |
| [`fuerza_contacto`](simulacion_09.py#L27) | Aplica la ecuación y devuelve la reacción del blanco. |
| [`solucion_analitica`](simulacion_09.py#L33) | Construye la referencia sin reutilizar RK4. |
| [`calcular_modelo`](simulacion_09.py#L38) | Coordina el integrador, la referencia y las métricas. |
| [`comparar_escenarios`](simulacion_09.py#L51) | Organiza tres ejecuciones que cambian un parámetro. |
| [`verificar`](simulacion_09.py#L57) | Contrasta referencias, balance de energía y paso temporal. |
| [`guardar_resultados`](simulacion_09.py#L88) | Exporta resultados, con unidades relativas y alcance. |
| [`main`](simulacion_09.py#L102) | Lee argumentos y define el orden de ejecución. |

Para cada una documenta **entradas, salida, forma de arreglos, unidades, quién la llama y una comprobación**. Amplía el mapa con las funciones de [motor_contacto.py](motor_contacto.py) y [animaciones.py](animaciones.py), descritas en [EXPLICACION_FUNCIONES.md](EXPLICACION_FUNCIONES.md).

## Copilot como tutor

> Lee CONTACTO_AUX_09.md. Ayúdame a deducir la ley y la relación analítica antes de programar. Hazme una pregunta por paso y espera mi explicación. Después revisa mis funciones: argumentos, retorno, arreglo de estado y unidades. No cambies la ecuación del artículo sin avisarme. Diferencia fórmula cerrada, raíz de una ecuación implícita, cuadratura, serie aproximada y RK4. Ayúdame a comprobar mi código con un límite analítico y un balance de energía. No inventes propiedades ni resultados de células.

## Entrega y defensa

- Tu código, dependencias y módulos utilizados, con una modificación propia justificada.
- Derivación manuscrita o explicada de la relación analítica, referencia y supuestos.
- Tres CSV, tabla de métricas A/B/C, figura comparativa, visor y GIF.
- Tabla de funciones y tres ejemplos breves de ayuda de Copilot que revisaste.
- Defensa: localizar la ecuación, recorrer `main()`, explicar dos funciones elegidas por el docente, predecir un cambio y ejecutarlo.

Debes distinguir **indentación δ**, **δ/R**, **penetración con perforación** y **deformación unitaria local**. Aquí se calculan las dos primeras; el perfil es una reconstrucción cuasiestática adoptada. No se modelan rotura, transfección, daño ni un campo 3D de deformaciones. En los modelos con separación a δ>0, el último cuadro termina el contacto y no demuestra una huella permanente.

[Volver a la distribución](README.md).
