from typing import Dict, List, Optional

from pydantic import BaseModel, Field
from schemas.adaptationtarget import (
    # AdaptationAssociation,
    AdaptationTargetBase,
    AssociationRead,
)


class NatureBasedSolutionBase(BaseModel):
    name: str = Field(..., example="Coastal Restoration")
    definition: str = Field(..., example="Definition of the solution")
    cobenefits: str = Field(..., example="Improved biodiversity")
    specificdetails: str = Field(..., example="Detailed information")
    location: str = Field(..., example="Coastal Area X")


class NatureBasedSolutionCreate(NatureBasedSolutionBase):
    adaptations: List[AssociationRead] = Field(
        default_factory=list,
        description="List of AdaptationTarget and their corresponding values",
        example=[
            {"target": {"id": 1, "target": "Heat"}, "value": 10},
            {"target": {"id": 2, "target": "Pluvial Flooding"}, "value": 20},
        ],
    )


class NatureBasedSolutionUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Coastal Restoration Updated")
    definition: Optional[str] = Field(None, example="Updated definition")
    cobenefits: Optional[str] = Field(None, example="Enhanced ecosystem services")
    specificdetails: Optional[str] = Field(None, example="Updated detailed information")
    location: Optional[str] = Field(None, example="Updated Coastal Area Y")
    adaptations: Optional[List[AssociationRead]] = Field(
        None,
        description="Optional list of AdaptationTarget and their corresponding values",
        example=[
            {"target": {"id": 1, "target": "Heat"}, "value": 10},
            {"target": {"id": 2, "target": "Pluvial Flooding"}, "value": 20},
        ],
    )


class NatureBasedSolutionRead(NatureBasedSolutionBase):
    id: int
    adaptations: List[AssociationRead] = Field(
        alias="solution_targets",
        description="List of AdaptationTarget and their corresponding values",
        default_factory=list,
    )

    class Config:
        from_attributes = True
        populate_by_name = True


# class NatureBasedSolutionRead(NatureBasedSolutionBase):
#     id: int
#     adaptations: List[AdaptationAssociation] = Field(
#         default_factory=list,
#         description="List of AdaptationTarget and their corresponding values",
#     )

#     class Config:
#         orm_mode = True
