from __future__ import annotations

from typing import List

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.orm import Mapped, attribute_keyed_dict, mapped_column, relationship

from . import Base
from .adaptation_target import AdaptationTarget


class Association(Base):
    __tablename__ = "nbs_target_assoc"
    nbs_id: Mapped[int] = mapped_column(
        ForeignKey("naturebasedsolution.id"), primary_key=True
    )
    target_id: Mapped[int] = mapped_column(
        ForeignKey("adaptationtarget.id"), primary_key=True
    )
    tg = relationship("AdaptationTarget")
    target = association_proxy("tg", "target")

    solution = relationship("NatureBasedSolution", back_populates="solution_targets")
    value: Mapped[int]


class NatureBasedSolution(Base):
    __tablename__ = "naturebasedsolution"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True, unique=True)
    definition: Mapped[str] = mapped_column(index=True)
    cobenefits: Mapped[str] = mapped_column(index=True)
    specificdetails: Mapped[str] = mapped_column(index=True)
    location: Mapped[str] = mapped_column(index=True)

    solution_targets = relationship(
        "Association",
        back_populates="solution",
        collection_class=attribute_keyed_dict("target"),
        cascade="all, delete-orphan",
    )

    adaptations = association_proxy(
        "solution_targets",
        "value",
        creator=lambda k, v: Association(target=k, value=v),
    )
    # TODO: geometry
