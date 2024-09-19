from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from nbsapi.models import AdaptationTarget, Association
from nbsapi.models import NatureBasedSolution as NbsDBModel
from nbsapi.schemas.adaptationtarget import AdaptationTargetBase
from nbsapi.schemas.naturebasedsolution import (
    AdaptationTargetRead,
    NatureBasedSolutionCreate,
    NatureBasedSolutionRead,
)


async def build_nbs_schema_from_model(db_solution: NbsDBModel):
    """FastAPI seems to struggle with automatic serialisation of the the db model to the schema
    so we're doing it manually for now
    """
    solution_read = NatureBasedSolutionRead(
        id=db_solution.id,
        name=db_solution.name,
        definition=db_solution.definition,
        cobenefits=db_solution.cobenefits,
        specificdetails=db_solution.specificdetails,
        location=db_solution.location,
        adaptations=[
            AdaptationTargetRead(
                adaptation=AdaptationTargetBase(id=assoc.tg.id, type=assoc.tg.target),
                value=assoc.value,
            )
            for assoc in db_solution.solution_targets
        ],
    )
    return solution_read


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
    return await build_nbs_schema_from_model(solution)


async def get_filtered_solutions(
    db_session: AsyncSession, targets: Optional[List[AdaptationTargetRead]]
):
    query = select(NbsDBModel)
    if targets:
        query = query.join(Association).join(AdaptationTarget)
        # add WHERE clauses encompassing both fields for each target
        clauses = or_(
            and_(
                AdaptationTarget.target == target.adaptation.type,
                Association.value == target.value,
            )
            for target in targets
        )
    res = (await db_session.scalars(query.where(clauses))).unique()
    if res:
        res = [await build_nbs_schema_from_model(model) for model in res]
    return res


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
        target_id = adaptation.adaptation.id
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
        db_session.add(association)
    db_session.add(db_solution)
    await db_session.commit()
    await db_session.refresh(db_solution)
    return await build_nbs_schema_from_model(db_solution)
