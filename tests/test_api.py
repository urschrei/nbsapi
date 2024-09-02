import json

from fastapi.testclient import TestClient

from nbsapi.api import app

client = TestClient(app)


def test_get_trees_with_bbox():
    # A bbox that includes Central Park, NYC, where the "Shade Trees" solution is located
    bbox = [-74.1, 40.7, -73.9, 40.8]  # This bbox should include the Central Park point

    response = client.get("/solutions/trees", params={"bbox": bbox})
    assert response.status_code == 200
    data = response.json()

    # Check that the "Shade Trees" solution is included
    assert len(data) == 1
    assert data[0]["name"] == "Shade Trees"

    # Test with a bbox that does not include Central Park, NYC
    bbox = [-74.2, 40.6, -74.15, 40.7]
    response = client.get("/solutions/trees", params={"bbox": bbox})
    assert response.status_code == 200
    data = response.json()

    # No solutions should be returned since the bbox does not cover Central Park
    assert len(data) == 0


def test_get_bioswales_with_geojson():
    geojson = {
        "type": "Polygon",
        "coordinates": [
            [
                [-73.945, 40.728],
                [-73.945, 40.730],
                [-73.943, 40.730],
                [-73.943, 40.728],
                [-73.945, 40.728],
            ]
        ],
    }
    geojson_str = json.dumps(geojson)
    response = client.get(f"/solutions/bioswales?geojson={geojson_str}")
    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Bioswales"

    # Test with a GeoJSON polygon that does not include Greenpoint, NYC
    geojson = {
        "type": "Polygon",
        "coordinates": [
            [
                [-74.000, 40.000],
                [-74.000, 40.002],
                [-73.998, 40.002],
                [-73.998, 40.000],
                [-74.000, 40.000],
            ]
        ],
    }
    geojson_str = json.dumps(geojson)
    response = client.get(f"/solutions/bioswales?geojson={geojson_str}")
    assert response.status_code == 200
    data = response.json()

    assert len(data) == 0
