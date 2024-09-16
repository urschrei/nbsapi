from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from nbsapi.models import NatureBasedSolution as NbsDBModel


async def get_solution(db_session: AsyncSession, solution_id: int):
    user = (
        await db_session.scalars(select(NbsDBModel).where(NbsDBModel.id == solution_id))
    ).first()
    if not user:
        raise HTTPException(status_code=404, detail="Solution not found")
    return user


async def get_solution_by_name(db_session: AsyncSession, name: str):
    return (
        await db_session.scalars(select(NbsDBModel).where(NbsDBModel.name == name))
    ).first()
