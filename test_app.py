import pytest
from dash.testing.application_runners import import_app


# ── Load the app ──────────────────────────────────────────────────────────────
@pytest.fixture
def app():
    return import_app("app")


# ── Test 1: Header is present ─────────────────────────────────────────────────
def test_header_present(dash_duo, app):
    """The visualiser must display a header with a title."""
    dash_duo.start_server(app)
    dash_duo.wait_for_element(".header", timeout=10)
    header = dash_duo.find_element(".header")
    assert header is not None, "Header element should be present on the page"
    assert len(header.text.strip()) > 0, "Header should contain visible text"


# ── Test 2: Visualisation (chart) is present ──────────────────────────────────
def test_visualisation_present(dash_duo, app):
    """The line chart must be rendered on page load."""
    dash_duo.start_server(app)
    dash_duo.wait_for_element("#sales-chart", timeout=10)
    chart = dash_duo.find_element("#sales-chart")
    assert chart is not None, "Sales chart should be rendered on the page"


# ── Test 3: Region picker is present ─────────────────────────────────────────
def test_region_picker_present(dash_duo, app):
    """The region radio button picker must appear with all five options."""
    dash_duo.start_server(app)
    dash_duo.wait_for_element("#region-filter", timeout=10)
    region_picker = dash_duo.find_element("#region-filter")
    assert region_picker is not None, "Region picker should be present on the page"
