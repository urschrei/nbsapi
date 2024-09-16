import json
import os
from contextlib import asynccontextmanager
from enum import Enum
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, conint, field_validator
from pyproj import Geod
from shapely.geometry import box, shape

from nbsapi.config import settings
from nbsapi.database import sessionmanager


# Load solutions from JSON fixture on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    global solutions
    json_file_path = os.path.join(os.path.dirname(__file__), "solutions.json")
    with open(json_file_path, "r") as f:
        solutions_data = json.load(f)
        solutions = [NatureBasedSolution(**solution) for solution in solutions_data]
    if sessionmanager._engine is not None:
        # Close the DB connection
        await sessionmanager.close()
    yield


app = FastAPI(lifespan=lifespan, title=settings.project_name)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AdaptationTargetEnum(str, Enum):
    """The kinds of protection or enhancement that the NbS provides"""

    pluvial_flooding = "Pluvial flooding"
    drought = "Drought"
    heat = "Heat"
    coastal_fluvial_flooding = "Coastal and Fluvial flooding"
    groundwater = "Groundwater"


class AdaptationTarget(BaseModel):
    target: AdaptationTargetEnum
    value: conint(ge=0, le=100)


class Category(str, Enum):
    heat = "Heat stress mitigation"
    flood = "Flood mitigation"
    energy = "Energy efficiency"


class NatureBasedSolution(BaseModel):
    name: str = Field(..., max_length=100)
    definition: str = Field(
        ..., max_length=500, description="Definition and primary function"
    )

    @field_validator("definition")
    def description_length(cls, value):
        if len(value) > 500:
            raise ValueError("Definition must be 500 characters or less.")
        return value

    specific_details: str = Field(..., max_length=500)

    @field_validator("specific_details")
    def spec_detail_length(cls, value):
        if len(value) > 500:
            raise ValueError("Specific details must be 500 characters or less.")
        return value

    # TODO: do we need both category AND adaptation target?
    adaptation_target: Dict[AdaptationTargetEnum, conint(ge=0, le=100)] = Field(
        ...,
        description="Adaptation target values (0-100) for each of the following: Pluvial flooding, Drought, Heat, Coastal and Fluvial flooding, Groundwater.",
    )
    cobenefits: str = Field(
        ...,
        max_length=200,
        description="Intended positive side effects of the solution",
    )
    category: Category
    location: str
    geometry: dict


solutions = []


def filter_solutions_by_bbox_or_geojson(
    solutions: List[
        "NatureBasedSolution"
    ],  # Assuming NatureBasedSolution has a 'geometry' attribute
    bbox: Optional[List[float]],
    geojson: Optional[dict],
) -> List["NatureBasedSolution"]:
    # Define the maximum allowable bounding box area in square meters (1 sq km = 1,000,000 sq meters)
    MAX_BBOX_AREA = 1_000_000.0
    geod = Geod(ellps="WGS84")
    if bbox:
        bbox_shape = box(*bbox)
        bbox_area, poly_perimeter = geod.geometry_area_perimeter(bbox_shape)
        if bbox_area > MAX_BBOX_AREA:
            raise HTTPException(
                status_code=400,
                detail="Bounding box area exceeds the maximum limit of 1 square kilometer.",
            )
        # Filter the solutions based on intersection with the bounding box
        filtered = [s for s in solutions if bbox_shape.intersects(shape(s.geometry))]
        return filtered

    if geojson:
        try:
            geojson_shape = shape(geojson)
        except Exception as e:
            raise HTTPException(status_code=400, detail="Invalid GeoJSON provided.")

        geojson_area, poly_perimeter = geod.geometry_area_perimeter(geojson_shape)
        if geojson_area > MAX_BBOX_AREA:
            raise HTTPException(
                status_code=400,
                detail="GeoJSON input area exceeds the maximum limit of 1 square kilometer.",
            )

        # Filter the solutions based on intersection with the GeoJSON shape
        filtered = [s for s in solutions if geojson_shape.intersects(shape(s.geometry))]
        return filtered

    return solutions


@app.get("/solutions", response_model=List[NatureBasedSolution])
def get_solutions(
    category: str = Query(
        ..., description="The category of nature-based solutions to retrieve."
    ),
    bbox: Optional[List[float]] = Query(
        None,
        min_items=4,
        max_items=4,
        description="Bounding box specified as [west, south, east, north]. The list should contain exactly four float values. Max 1 sq km",
    ),
    geojson: Optional[str] = Query(
        None,
        description="GeoJSON polygon specifying the area of interest. The GeoJSON should be passed as a JSON string.",
    ),
    adaptation_targets: Optional[List[AdaptationTargetEnum]] = Query(
        None, description="List of adaptation targets to filter by with values > 1"
    ),
):
    # Ensure either bbox or geojson is provided
    if not bbox and not geojson:
        raise HTTPException(
            status_code=400, detail="Either 'bbox' or 'geojson' must be provided."
        )

    # Prevent both bbox and geojson from being provided simultaneously
    if bbox and geojson:
        raise HTTPException(
            status_code=400,
            detail="You can provide only one of 'bbox' or 'geojson', not both.",
        )

    # Filter solutions by category
    filtered_solutions = [s for s in solutions if s.category == category]

    # Filter solutions by adaptation targets if provided
    if adaptation_targets:
        filtered_solutions = [
            s
            for s in filtered_solutions
            if any(
                target in s.adaptation_target and s.adaptation_target[target] > 1
                for target in adaptation_targets
            )
        ]

    # Filter solutions by bbox or GeoJSON
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
