from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from nbsapi.models import Association
from nbsapi.models import NatureBasedSolution as NbsDBModel
from nbsapi.schemas.adaptationtarget import AdaptationTargetBase
from nbsapi.schemas.naturebasedsolution import AssociationRead, NatureBasedSolutionRead


async def get_solution(db_session: AsyncSession, solution_id: int):
    solution = (
        await db_session.scalars(
            select(NbsDBModel)
            .options(joinedload(NbsDBModel.solution_targets).joinedload(Association.tg))
            .where(NbsDBModel.id == solution_id)
        )
    ).first()
    if not solution:
        raise HTTPException(status_code=404, detail="Solution not found")
    solution_read = NatureBasedSolutionRead(
        id=solution.id,
        name=solution.name,
        definition=solution.definition,
        cobenefits=solution.cobenefits,
        specificdetails=solution.specificdetails,
        location=solution.location,
        adaptations=[
            AssociationRead(
                target=AdaptationTargetBase(id=assoc.tg.id, target=assoc.tg.target),
                value=assoc.value,
            )
            for assoc in solution.solution_targets
        ],
    )
    return solution_read


async def get_solution_by_name(db_session: AsyncSession, name: str):
    return (
        await db_session.scalars(select(NbsDBModel).where(NbsDBModel.name == name))
    ).first()
