import json
from unittest.mock import patch

from fastapi.testclient import TestClient

from nbsapi.api import AdaptationTargetEnum, NatureBasedSolution, app

client = TestClient(app)

# Sample mock data as instances of the NatureBasedSolution model
mock_solutions = [
    NatureBasedSolution(
        name="Shade Trees",
        definition="Trees provide shade, reducing urban heat.",
        specific_details="Planting trees helps to mitigate heat island effects in urban areas.",
        adaptation_target={AdaptationTargetEnum.heat: 90},
        cobenefits="Improves air quality",
        category="Heat stress mitigation",
        location="Central Park, NYC",
        geometry={"type": "Point", "coordinates": [-73.9654, 40.7829]},
    ),
    NatureBasedSolution(
        name="Bioswales",
        definition="Bioswales capture and filter stormwater runoff.",
        specific_details="Bioswales are vegetated channels that slow and filter runoff.",
        adaptation_target={AdaptationTargetEnum.pluvial_flooding: 80},
        cobenefits="Supports biodiversity",
        category="Flood mitigation",
        location="Greenpoint, NYC",
        geometry={
            "type": "Polygon",
            "coordinates": [
                [
                    [-73.9442, 40.7294],
                    [-73.9442, 40.7294],
                    [-73.9442, 40.7294],
                    [-73.9442, 40.7294],
                ]
            ],
        },
    ),
]


# Mock the function that loads the solutions during startup
@patch("nbsapi.api.lifespan", return_value=None)
@patch("nbsapi.api.solutions", mock_solutions)
def test_get_trees_with_bbox(mock_load_solutions):
    # A bbox that includes Central Park, NYC, where the "Shade Trees" solution is located
    bbox = [
        -73.968,
        40.781,
        -73.962,
        40.784,
    ]  # This bbox should include the Central Park point

    response = client.get("/solutions/trees", params={"bbox": bbox})
    assert response.status_code == 200
    data = response.json()

    # Check that the "Shade Trees" solution is included
    assert len(data) == 1
    assert data[0]["name"] == "Shade Trees"

    # Test with a bbox that does not include Central Park, NYC
    bbox = [-73.970, 40.785, -73.968, 40.787]
    response = client.get("/solutions/trees", params={"bbox": bbox})
    assert response.status_code == 200
    data = response.json()

    # No solutions should be returned since the bbox does not cover Central Park
    assert len(data) == 0


# Mock the function that loads the solutions during startup
@patch("nbsapi.api.lifespan", return_value=None)
@patch("nbsapi.api.solutions", mock_solutions)
def test_get_trees_with_large_bbox(mock_load_solutions):
    # A bbox that includes a much larger area, designed to fail (larger than 1 square kilometer)
    # This is a bounding box of approximately 10 km x 10 km in NYC
    large_bbox = [-74.3, 40.5, -73.7, 41.0]

    response = client.get("/solutions/trees", params={"bbox": large_bbox})

    # The response should fail with a 400 status due to the large bounding box
    assert response.status_code == 400
    assert (
        "Bounding box area exceeds the maximum limit of 1 square kilometer"
        in response.json()["detail"]
    )


# This ensures the test will fail by checking that an exception is raised for an overly large bbox


@patch("nbsapi.api.lifespan", return_value=None)
@patch("nbsapi.api.solutions", mock_solutions)
def test_get_bioswales_with_geojson(mock_load_solutions):
    geojson = {
        "type": "Polygon",
        "coordinates": [
            [
                [-73.9493, 40.7243],
                [-73.9493, 40.7345],
                [-73.9391, 40.7345],
                [-73.9391, 40.7243],
                [-73.9493, 40.7243],
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
