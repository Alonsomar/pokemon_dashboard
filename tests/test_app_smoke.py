import importlib
import sys
from pathlib import Path

# Ensure the project root is importable when tests run from any working directory.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))



def test_app_imports_and_has_layout():
    mod = importlib.import_module("app")
    assert hasattr(mod, "app"), "app.py debe exponer una variable `app` (instancia Dash)"
    app = mod.app
    assert getattr(app, "layout", None) is not None, "La app debe tener layout asignado"