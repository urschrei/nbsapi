# from nbsapi.api.dependencies.auth import validate_is_authenticated
from typing import List

from fastapi import APIRouter, Depends

from nbsapi.api.dependencies.core import DBSessionDep
from nbsapi.crud.adaptationtarget import get_target, get_targets
from nbsapi.schemas.adaptationtarget import AdaptationTargetBase

router = APIRouter(
    prefix="/api/targets",
    tags=["targets"],
    responses={404: {"description": "Not found"}},
)


@router.get("/target", response_model=List[AdaptationTargetBase])
async def read_targets(db_session: DBSessionDep):
    """Retrieve all available adaptation targets"""
    targets = await get_targets(db_session)
    return targets
