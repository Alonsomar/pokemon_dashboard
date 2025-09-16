import importlib

def test_app_imports_and_has_layout():
    mod = importlib.import_module("app")
    assert hasattr(mod, "app"), "app.py debe exponer una variable `app` (instancia Dash)"
    app = getattr(mod, "app")
    assert getattr(app, "layout", None) is not None, "La app debe tener layout asignado"
