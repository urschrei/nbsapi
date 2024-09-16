from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

# from .naturebasedsolution import NatureBasedSolution, nbs_target_assoc


class AdaptationTarget(Base):
    __tablename__ = "adaptationtarget"
    id: Mapped[int] = mapped_column(primary_key=True)
    target: Mapped[str] = mapped_column(index=True, unique=True)
    value: Mapped[int] = mapped_column(index=True)
    solutions: Mapped[List["NatureBasedSolution"]] = relationship(
        secondary="nbs_target_assoc", back_populates="targets"
    )
