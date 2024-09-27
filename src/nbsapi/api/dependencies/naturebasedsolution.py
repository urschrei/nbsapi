from typing import Annotated

from app.crud.naturebasedsolution import get_solution_by_name

# from app.schemas.auth import TokenData
# from app.utils.auth import decode_jwt, oauth2_scheme
from fastapi import Depends, HTTPException, status

# from jwt import PyJWTError
from nbsapi import models
from nbsapi.api.dependencies.core import DBSessionDep


async def get_current_solution(
    name: str, db_session: DBSessionDep
) -> models.NatureBasedSolution:
    credentials_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Could not find a solution with that name",
        headers={},
    )
    solution = await get_solution_by_name(db_session, name)
    if solution is None:
        raise credentials_exception
    return solution


SolutionDep = Annotated[models.NatureBasedSolution, Depends(get_current_solution)]
