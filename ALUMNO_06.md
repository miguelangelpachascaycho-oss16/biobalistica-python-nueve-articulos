> **MATERIAL AUXILIAR ANTERIOR. Esta ficha no constituye una asignación de biobalística en células o tejidos. Consulta [la revisión vigente](REVISION_BIOBALISTICA.md).**

# Alumno 06 · Impacto y deformación del blanco

## Artículo distinto asignado

**Brilliantov, Spahn, Hertzsch y Pöschel (1996). A model for collisions in granular gases.** Physical Review E 53, 5382-5392. [DOI 10.1103/PhysRevE.53.5382](https://doi.org/10.1103/PhysRevE.53.5382).

[Lectura](https://arxiv.org/html/cond-mat/0203598). Prepublicación completa de autores en arXiv, depositada en 2002; artículo de 1996.

**Localización:** Ecuaciones (23)-(24), fuerza viscosa y dinámica normal; ecuación (20), aproximación cuasiestática.

**Ley que vas a representar:** `F=k δ^(3/2)+d sqrt(δ) δ'; d=3Ak/2`.

**Adaptación declarada:** Se usa el límite esfera rígida–blanco deformable del contacto equivalente. Solo dirección normal. Se corta al desaparecer la fuerza repulsiva según la corrección de Schwager y Pöschel (ficha 08), declarada como complemento.

Todos los casos de esta edición calculan la indentación del **blanco deformable**, con esfera rígida. Se trabaja en coordenadas relativas y con propiedades docentes. No son calibraciones de células ni reproducciones completas de los experimentos del artículo. Consulta [cómo se dibuja y qué se mide](MODELO_DEFORMACION_BLANCO.md).

## Construir la simulación analítica

Serie de tiempo corto δ≈t-(4d/15)t^(5/2)-(4/35)t^(7/2), con m=k=v0=1, y solución elástica límite. La serie es deducción docente y se limita a t≤0.12.

**Tu derivación individual:** Obtener los primeros términos sustituyendo δ≈t en la aceleración. Reducir la ventana y medir el error de la serie.

Consulta [las deducciones y límites](SOLUCIONES_ANALITICAS.md). Identifica si tu resultado es cerrado, implícito, semianalítico o una aproximación. No presentes una integración numérica como solución analítica.

## Paso a paso en VS Code

1. Sigue la [instalación común](README.md#instalación-y-ejecución). Conserva `motor_contacto.py` y `animaciones.py` junto al programa.
2. Antes de ver el ejemplo, dibuja la esfera, el blanco y las fuerzas. Define δ, v, m, la reacción y la convención de signos.
3. Escribe `m δ''=-F(δ,δ')`, las condiciones iniciales y la condición de separación. Desarrolla a mano tu relación analítica.
4. Crea tu propio `mi_simulacion_06.py` siguiendo [Aprende a construir](APRENDE_A_CONSTRUIR.md). Primero implementa el cálculo de F; comprueba un valor a mano. Luego construye la referencia analítica de tu caso.
5. Ejecuta la referencia preparada para contrastar tu implementación:

   ```powershell
   .\.venv\Scripts\python.exe simulacion_06.py --escenario A --verificar --animar
   ```

6. Abre `resultados/alumno_06/visor.html`: reproduce, pausa y cambia el tiempo. Observa cómo la esfera desplaza la superficie del blanco. La curva de δ(t) usa exactamente el mismo estado que la escena.
7. Ejecuta los tres escenarios:

   ```powershell
   .\.venv\Scripts\python.exe simulacion_06.py --escenario todos --verificar --animar
   ```

8. El parámetro `d` toma A=0.03, B=0.12, C=0.3. Predice qué pasará con la indentación máxima, la fuerza, la restitución y la energía antes de compararlos.
9. Abre `comparacion.png`, `metricas.json` y los CSV. Explica el error numérico frente a la referencia y el error de aproximación cuando corresponda. Un vacío en las columnas de referencia significa que la serie ya está fuera de su ventana de validez.
10. Reduce el paso a la mitad con `--paso 0.001`, cambia `--salida resultados/mi_refinamiento_06` y compara. Distingue resolución del integrador y número de cuadros del GIF.
11. Implementa tu reto personal y ejecuta tu archivo desde una terminal nueva. Explica cada función sin leer respuestas de Copilot.

## Funciones que debes explicar

| Función | Propósito |
|---|---|
| [`parametros_escenario`](simulacion_06.py#L20) | Transforma el parámetro del escenario en constantes de la ley. |
| [`fuerza_contacto`](simulacion_06.py#L27) | Aplica la ecuación y devuelve la reacción del blanco. |
| [`solucion_analitica`](simulacion_06.py#L33) | Construye la referencia sin reutilizar RK4. |
| [`calcular_modelo`](simulacion_06.py#L38) | Coordina el integrador, la referencia y las métricas. |
| [`comparar_escenarios`](simulacion_06.py#L51) | Organiza tres ejecuciones que cambian un parámetro. |
| [`verificar`](simulacion_06.py#L57) | Contrasta referencias, balance de energía y paso temporal. |
| [`guardar_resultados`](simulacion_06.py#L88) | Exporta resultados, con unidades relativas y alcance. |
| [`main`](simulacion_06.py#L102) | Lee argumentos y define el orden de ejecución. |

Para cada una documenta **entradas, salida, forma de arreglos, unidades, quién la llama y una comprobación**. Amplía el mapa con las funciones de [motor_contacto.py](motor_contacto.py) y [animaciones.py](animaciones.py), descritas en [EXPLICACION_FUNCIONES.md](EXPLICACION_FUNCIONES.md).

## Copilot como tutor

> Lee ALUMNO_06.md. Ayúdame a deducir la ley y la relación analítica antes de programar. Hazme una pregunta por paso y espera mi explicación. Después revisa mis funciones: argumentos, retorno, arreglo de estado y unidades. No cambies la ecuación del artículo sin avisarme. Diferencia fórmula cerrada, raíz de una ecuación implícita, cuadratura, serie aproximada y RK4. Ayúdame a comprobar mi código con un límite analítico y un balance de energía. No inventes propiedades ni resultados de células.

## Entrega y defensa

- Tu código, dependencias y módulos utilizados, con una modificación propia justificada.
- Derivación manuscrita o explicada de la relación analítica, referencia y supuestos.
- Tres CSV, tabla de métricas A/B/C, figura comparativa, visor y GIF.
- Tabla de funciones y tres ejemplos breves de ayuda de Copilot que revisaste.
- Defensa: localizar la ecuación, recorrer `main()`, explicar dos funciones elegidas por el docente, predecir un cambio y ejecutarlo.

Debes distinguir **indentación δ**, **δ/R**, **penetración con perforación** y **deformación unitaria local**. Aquí se calculan las dos primeras; el perfil es una reconstrucción cuasiestática adoptada. No se modelan rotura, transfección, daño ni un campo 3D de deformaciones. En los modelos con separación a δ>0, el último cuadro termina el contacto y no demuestra una huella permanente.

[Volver a la distribución](README.md).
