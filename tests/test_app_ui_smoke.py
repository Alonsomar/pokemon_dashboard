"""Smoke tests for the Dash UI using dash[testing]."""

import importlib

import pytest

pytest.importorskip("dash.testing.application", reason="dash[testing] extra is required")


@pytest.fixture
def dash_app():
    """Return the Dash app instance exposed by app.py."""
    module = importlib.import_module("app")
    return module.app


def test_app_serves_main_layout(dash_duo, dash_app):
    """The server should start and render the main heading."""
    dash_duo.start_server(dash_app)

    dash_duo.wait_for_element("#body-container")
    dash_duo.wait_for_text_to_equal("h1", "Pokémon Dashboard")
    assert dash_duo.driver.title == "Pokemon Dashboard"


def test_app_renders_at_least_one_graph(dash_duo, dash_app):
    """The landing page should render at least one dcc.Graph."""
    dash_duo.start_server(dash_app)

    dash_duo.wait_for_element(".dash-graph")
    graphs = dash_duo.driver.find_elements("css selector", ".dash-graph")
    assert graphs, "Se esperaba al menos un componente dcc.Graph en el layout inicial"
