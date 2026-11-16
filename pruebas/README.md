# Verificación matemática

Ejecuta desde la raíz del repositorio, con las dependencias instaladas:

```powershell
.\.venv\Scripts\python.exe pruebas/verificar_celulas.py
.\.venv\Scripts\python.exe pruebas/verificar_piloto.py
.\.venv\Scripts\python.exe pruebas/verificar_piel.py
.\.venv\Scripts\python.exe pruebas/verificar_vesicula.py
.\.venv\Scripts\python.exe pruebas/verificar_nuevos.py
```

Las nuevas comprobaciones se guardan en `pruebas/resultados/`. `evidencia/` conserva las comprobaciones de las simulaciones que generaron los GIF de ejemplo. Estas pruebas comprueban fuerzas, energía, integración y límites analíticos; no constituyen validación experimental ni reproducción completa de los artículos.
