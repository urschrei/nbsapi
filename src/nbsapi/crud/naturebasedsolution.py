from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from nbsapi.models import AdaptationTarget, Association
from nbsapi.models import NatureBasedSolution as NbsDBModel
from nbsapi.schemas.adaptationtarget import AdaptationTargetBase
from nbsapi.schemas.naturebasedsolution import (
    AssociationRead,
    NatureBasedSolutionCreate,
    NatureBasedSolutionRead,
)


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


# async def create_nature_based_solution(
#     db_session: AsyncSession, solution: NatureBasedSolutionCreate
# ):
#     db_solution = NbsDBModel(
#         name=solution.name,
#         definition=solution.definition,
#         cobenefits=solution.cobenefits,
#         specificdetails=solution.specificdetails,
#         location=solution.location,
#     )
#     for adaptation in solution.adaptations:
#         target_id = adaptation.target.id
#         value = adaptation.value
#         target = (
#             await db_session.scalars(
#                 select(AdaptationTarget).where(AdaptationTarget.id == target_id)
#             )
#         ).first()
#         # db_session.get(AdaptationTarget, target_id)
#         if not target:
#             raise HTTPException(
#                 status_code=404,
#                 detail=f"AdaptationTarget with id {target_id} not found",
#             )
#         association = Association(tg=target, value=value)
#         db_solution.solution_targets.append(association)
#     db_session.add(db_solution)
#     db_session.commit()
#     db_session.refresh(db_solution)
#     return db_solution


async def create_nature_based_solution(
    db_session: AsyncSession, solution: NatureBasedSolutionCreate
):
    db_solution = NbsDBModel(
        name=solution.name,
        definition=solution.definition,
        cobenefits=solution.cobenefits,
        specificdetails=solution.specificdetails,
        location=solution.location,
    )
    for adaptation in solution.adaptations:
        target_id = adaptation.target.id
        value = adaptation.value
        # Properly execute the select statement
        result = await db_session.execute(
            select(AdaptationTarget).where(AdaptationTarget.id == target_id)
        )
        target = result.scalars().first()
        if not target:
            raise HTTPException(
                status_code=404,
                detail=f"AdaptationTarget with id {target_id} not found",
            )
        association = Association(tg=target, value=value)
        db_solution.solution_targets.append(association)
    db_session.add(db_solution)
    await db_session.commit()
    await db_session.refresh(db_solution)
    return db_solution
