from fastapi.testclient import TestClient

from nbsapi.api import app

client = TestClient(app)


def test_get_solutions():
    response = client.get("/solutions?category=heat")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_get_trees():
    response = client.get("/solutions/trees")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Shade Trees"


def test_get_bioswales():
    response = client.get("/solutions/bioswales")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Bioswales"
