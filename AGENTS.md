# Cómo colaborar con el agente (Codex) en este repo

## Entorno
- Python 3.12
- Instala deps: `pip install -r requirements.txt -r requirements-dev.txt`
- Tests: `pytest -q`
- Tests UI (Dash): `pytest -q tests/test_app_ui_smoke.py`
- Lint/Format: `ruff check . && ruff format .`

## Convenciones
- PRs atómicos (<300 líneas, 1 objetivo).
- Añadir/ajustar tests por cada cambio en `app.py`, `layout.py`, `plot_utils.py`.
- No romper la API pública; mantener estructura de carpetas.

## Tareas típicas que puede ejecutar el agente
- **Tests**: crear tests de humo adicionales (IDs estables en componentes), añadir tests de callbacks con `dash[testing]`.
- **Housekeeping**: ruff fixes, docstrings, tipado ligero.
- **CI**: mejorar matrices de Python, añadir badges, optimizar cache.

## Criterios de aceptación
- `pytest -q` y `ruff check .` verdes en CI.
- PR con resumen + justificación de cambios.
