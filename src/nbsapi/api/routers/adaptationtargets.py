# from nbsapi.api.dependencies.auth import validate_is_authenticated

from fastapi import APIRouter, Depends

from nbsapi.api.dependencies.core import DBSessionDep
from nbsapi.crud.adaptationtarget import get_target
from nbsapi.schemas.adaptationtarget import AdaptationTargetBase

router = APIRouter(
    prefix="/api/targets",
    tags=["targets"],
    responses={404: {"description": "Not found"}},
)


@router.get("/targets/{target_id}", response_model=AdaptationTargetBase)
async def read_nature_based_solution(target_id: int, db_session: DBSessionDep):
    target = await get_target(db_session, target_id)
    return target
