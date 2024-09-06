import json
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from shapely.geometry import box, shape

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class NatureBasedSolution(BaseModel):
    name: str
    description: str
    category: str
    effectiveness: str
    location: str
    geometry: dict


# Example data
solutions = [
    NatureBasedSolution(
        name="Shade Trees",
        description="Trees provide shade, reducing urban heat.",
        category="heat",
        effectiveness="high",
        location="Central Park, NYC",
        geometry={"type": "Point", "coordinates": [-73.9654, 40.7829]},
    ),
    NatureBasedSolution(
        name="Bioswales",
        description="Bioswales capture and filter stormwater runoff.",
        category="flooding",
        effectiveness="moderate",
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


def filter_solutions_by_bbox_or_geojson(
    solutions: List[NatureBasedSolution],
    bbox: Optional[List[float]],
    geojson: Optional[dict],
) -> List[NatureBasedSolution]:
    if bbox:
        bbox_shape = box(*bbox)  # Create a shapely box from the bbox
        filtered = [s for s in solutions if bbox_shape.intersects(shape(s.geometry))]
        return filtered

    if geojson:
        try:
            geojson_shape = shape(geojson)
        except Exception as e:
            raise HTTPException(status_code=400, detail="Invalid GeoJSON provided")
        filtered = [s for s in solutions if geojson_shape.intersects(shape(s.geometry))]
        return filtered

    return solutions


@app.get("/solutions", response_model=List[NatureBasedSolution])
def get_solutions(
    category: str = Query(
        ...,
        enum=["heat", "flooding"],
        description="The category of nature-based solutions to retrieve. Options are 'heat' for excess heat mitigation and 'flooding' for flood mitigation.",
    ),
    bbox: Optional[List[float]] = Query(
        None,
        min_items=4,
        max_items=4,
        description="Bounding box specified as [west, south, east, north]. The list should contain exactly four float values.",
    ),
    geojson: Optional[str] = Query(
        None,
        description="GeoJSON polygon specifying the area of interest. The GeoJSON should be passed as a JSON string.",
    ),
):
    filtered_solutions = [s for s in solutions if s.category == category]

    if geojson:
        geojson_dict = json.loads(geojson)
        filtered_solutions = filter_solutions_by_bbox_or_geojson(
            filtered_solutions, None, geojson_dict
        )
    elif bbox:
        filtered_solutions = filter_solutions_by_bbox_or_geojson(
            filtered_solutions, bbox, None
        )

    return filtered_solutions


@app.get("/solutions/trees", response_model=List[NatureBasedSolution])
def get_trees(
    bbox: Optional[List[float]] = Query(
        None,
        min_items=4,
        max_items=4,
        description="Bounding box specified as [west, south, east, north]. The list should contain exactly four float values.",
    ),
    geojson: Optional[str] = Query(
        None,
        description="GeoJSON polygon specifying the area of interest. The GeoJSON should be passed as a JSON string.",
    ),
):
    tree_solutions = [s for s in solutions if s.name == "Shade Trees"]
    if geojson:
        geojson_dict = json.loads(geojson)
        filtered_trees = filter_solutions_by_bbox_or_geojson(
            tree_solutions, None, geojson_dict
        )
    elif bbox:
        filtered_trees = filter_solutions_by_bbox_or_geojson(tree_solutions, bbox, None)
    else:
        filtered_trees = tree_solutions
    return filtered_trees


@app.get("/solutions/bioswales", response_model=List[NatureBasedSolution])
def get_bioswales(
    bbox: Optional[List[float]] = Query(
        None,
        min_items=4,
        max_items=4,
        description="Bounding box specified as [west, south, east, north]. The list should contain exactly four float values.",
    ),
    geojson: Optional[str] = Query(
        None,
        description="GeoJSON polygon specifying the area of interest. The GeoJSON should be passed as a JSON string.",
    ),
):
    bioswale_solutions = [s for s in solutions if s.name == "Bioswales"]
    if geojson:
        geojson_dict = json.loads(geojson)
        filtered_bioswales = filter_solutions_by_bbox_or_geojson(
            bioswale_solutions, None, geojson_dict
        )
    elif bbox:
        filtered_bioswales = filter_solutions_by_bbox_or_geojson(
            bioswale_solutions, bbox, None
        )
    else:
        filtered_bioswales = bioswale_solutions
    return filtered_bioswales
