# from nbsapi.api.dependencies.auth import validate_is_authenticated

from fastapi import APIRouter, Depends

from nbsapi.api.dependencies.core import DBSessionDep
from nbsapi.crud.naturebasedsolution import get_solution
from nbsapi.schemas.naturebasedsolution import NatureBasedSolutionRead

router = APIRouter(
    prefix="/api/solutions",
    tags=["solutions"],
    responses={404: {"description": "Not found"}},
)


@router.get("/solutions/{solution_id}", response_model=NatureBasedSolutionRead)
async def read_nature_based_solution(solution_id: int, db_session: DBSessionDep):
    solution = await get_solution(db_session, solution_id)
    return solution
