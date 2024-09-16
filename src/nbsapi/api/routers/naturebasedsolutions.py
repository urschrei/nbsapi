# from nbsapi.api.dependencies.auth import validate_is_authenticated
import json
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pyproj import Geod
from shapely.geometry import box, shape

from nbsapi.api.dependencies.core import DBSessionDep
from nbsapi.crud.naturebasedsolution import get_solution
from nbsapi.schemas.adaptationtarget import AdaptationTargetEnum
from nbsapi.schemas.naturebasedsolution import NatureBasedSolution

router = APIRouter(
    prefix="/api/solutions",
    tags=["solutions"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/{solution_id}",
    response_model=NatureBasedSolution,
    dependencies=[],
)
async def solution_details(
    solution_id: int,
    db_session: DBSessionDep,
):
    """
    Get any solution details
    """
    solution = await get_solution(db_session, solution_id)
    return solution


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


@router.get("/solutions", response_model=List[NatureBasedSolution])
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
