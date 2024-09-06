import json
import os
from contextlib import asynccontextmanager
from enum import Enum
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from shapely.geometry import box, shape


# Load solutions from JSON fixture on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    global solutions
    json_file_path = os.path.join(os.path.dirname(__file__), "solutions.json")
    with open(json_file_path, "r") as f:
        solutions_data = json.load(f)
        solutions = [NatureBasedSolution(**solution) for solution in solutions_data]
    yield


app = FastAPI(lifespan=lifespan)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Category(str, Enum):
    heat = "Heat stress mitigation"
    flood = "Flood mitigation"
    energy = "Energy efficiency"


class NatureBasedSolution(BaseModel):
    name: str
    description: str = Field(..., max_length=500)

    @validator("description")
    def description_length(cls, value):
        if len(value) > 500:
            raise ValueError("Description must be 500 characters or less.")
        return value

    category: Category
    effectiveness: str
    location: str
    geometry: dict


solutions = []


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
    category: Category = Query(
        ..., description="The category of nature-based solutions to retrieve."
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
