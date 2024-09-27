# from nbsapi.api.dependencies.auth import validate_is_authenticated

from typing import Dict, List, Optional

from fastapi import APIRouter, Body, Depends, Query

from nbsapi.api.dependencies.core import DBSessionDep
from nbsapi.crud.naturebasedsolution import (
    create_nature_based_solution,
    get_filtered_solutions,
    get_solution,
)
from nbsapi.schemas.adaptationtarget import AdaptationTargetRead
from nbsapi.schemas.naturebasedsolution import (
    NatureBasedSolutionCreate,
    NatureBasedSolutionRead,
)

router = APIRouter(
    prefix="/api/solutions",
    tags=["solutions"],
    responses={404: {"description": "Not found"}},
)


@router.get("/solutions/{solution_id}", response_model=NatureBasedSolutionRead)
async def read_nature_based_solution(solution_id: int, db_session: DBSessionDep):
    solution = await get_solution(db_session, solution_id)
    return solution


@router.post("/solutions", response_model=List[NatureBasedSolutionRead])
async def get_solutions(
    db_session: DBSessionDep,
    targets: List[AdaptationTargetRead] = Body(
        None, description="List of adaptation targets to filter by"
    ),
):
    """
    Filter solutions based on **optional** adaptation targets and their associated protection values.
    Solutions having targets with protection values **equal to or greater than** the specified values will be returned
    """
    # TODO: add optional bounding box and polygon params when we have PostGIS and geometry column
    solutions = await get_filtered_solutions(db_session, targets)
    return solutions


@router.post("/add_solution/", response_model=NatureBasedSolutionRead)
async def write_nature_based_solution(
    solution: NatureBasedSolutionCreate, db_session: DBSessionDep
):
    solution = await create_nature_based_solution(db_session, solution)
    return solution
