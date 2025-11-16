# /tests/test_routes.py
import pytest
from backend import create_app


@pytest.fixture
def client():
    """Flask test client fixture."""
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home_page(client):
    """Check that the home page loads successfully."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Patient Dashboard" in response.data


def test_about_page(client):
    """Check that the about page renders."""
    response = client.get("/about")
    assert response.status_code == 200
    assert b"About" in response.data


def test_api_patients(client):
    """Verify /api/patients returns JSON."""
    response = client.get("/api/patients")
    assert response.status_code == 200
    data = response.get_json()
    assert "patients" in data
    assert isinstance(data["patients"], list)


def test_api_meta(client):
    """Verify metadata endpoint works."""
    response = client.get("/api/meta")
    assert response.status_code == 200
    meta = response.get_json()
    assert "app" in meta
    assert "version" in meta


def test_invalid_patient(client):
    """Verify invalid patient id returns 404."""
    response = client.get("/api/patients/9999")
    assert response.status_code == 404


def test_invalid_relation(client):
    """Verify unknown relation returns 404."""
    response = client.get("/api/relations/Unknown/None")
    assert response.status_code == 404
