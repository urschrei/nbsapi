from __future__ import annotations

from typing import List

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base
from .adaptation_target import AdaptationTarget

nbs_target_assoc = Table(
    "nbs_target_assoc",
    Base.metadata,
    Column("nbs_id", ForeignKey("naturebasedsolution.id"), primary_key=True),
    Column("target_id", ForeignKey("adaptationtarget.id")),
    primary_key=True,
)


class NatureBasedSolution(Base):
    __tablename__ = "naturebasedsolution"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True, unique=True)
    definition: Mapped[str] = mapped_column(index=True)
    cobenefits: Mapped[str] = mapped_column(index=True)
    specificdetails: Mapped[str] = mapped_column(index=True)
    location: Mapped[str] = mapped_column(index=True)
    targets: Mapped[List[AdaptationTarget]] = relationship(
        secondary=nbs_target_assoc, back_populates="solutions"
    )
    # TODO: geometry
