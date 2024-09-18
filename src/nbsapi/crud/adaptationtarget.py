from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from nbsapi.models.adaptation_target import AdaptationTarget
from nbsapi.schemas.adaptationtarget import AdaptationTargetBase


async def get_target(db_session: AsyncSession, target_id: int):
    target = (
        await db_session.scalars(
            select(AdaptationTarget).where(AdaptationTarget.id == target_id)
        )
    ).first()
    if not target:
        raise HTTPException(status_code=404, detail="Adaptation target not found")
    actual = AdaptationTargetBase(id=target.id, type=target.target)
    return actual
