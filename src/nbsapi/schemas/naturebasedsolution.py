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
    adaptations: Dict[str, int] = Field(
        default_factory=dict,
        description="Mapping of AdaptationTarget IDs to their corresponding values",
        example={"Heat": 10, "Drought": 20},
    )


class NatureBasedSolutionUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Coastal Restoration Updated")
    definition: Optional[str] = Field(None, example="Updated definition")
    cobenefits: Optional[str] = Field(None, example="Enhanced ecosystem services")
    specificdetails: Optional[str] = Field(None, example="Updated detailed information")
    location: Optional[str] = Field(None, example="Updated Coastal Area Y")
    adaptations: Optional[Dict[str, int]] = Field(
        None,
        description="Optional mapping of AdaptationTarget IDs to their corresponding values",
        example={"Heat": 15, "Drought": 25},
    )


class NatureBasedSolutionRead(NatureBasedSolutionBase):
    id: int
    adaptations: List[AssociationRead] = Field(
        alias="solution_targets",
        description="List of AdaptationTarget and their corresponding values",
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
