from typing import List, Optional

from fastapi import FastAPI, Query
from geojson import Polygon
from pydantic import BaseModel

app = FastAPI()


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


@app.get("/solutions", response_model=List[NatureBasedSolution])
def get_solutions(
    category: str = Query(..., enum=["heat", "flooding"]),
    bbox: Optional[List[float]] = Query(None, min_items=4, max_items=4),
    geojson: Optional[str] = None,
):
    # Here we would filter solutions based on bbox or geojson, if provided.
    filtered_solutions = [s for s in solutions if s.category == category]
    return filtered_solutions


@app.get("/solutions/trees", response_model=NatureBasedSolution)
def get_trees():
    return next(s for s in solutions if s.name == "Shade Trees")


@app.get("/solutions/bioswales", response_model=NatureBasedSolution)
def get_bioswales():
    return next(s for s in solutions if s.name == "Bioswales")
