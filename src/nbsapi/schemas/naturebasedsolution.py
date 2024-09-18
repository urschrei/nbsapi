from typing import Dict, List, Optional

from pydantic import BaseModel, Field
from schemas.adaptationtarget import (
    AdaptationTargetRead,
)


class NatureBasedSolutionBase(BaseModel):
    name: str = Field(..., example="Coastal Restoration")
    definition: str = Field(..., example="Definition of the solution")
    cobenefits: str = Field(..., example="Improved biodiversity")
    specificdetails: str = Field(..., example="Detailed information")
    location: str = Field(..., example="Coastal Area X")


class NatureBasedSolutionCreate(NatureBasedSolutionBase):
    adaptations: List[AdaptationTargetRead] = Field(
        default_factory=list,
        description="List of adaptation types and their corresponding values",
        example=[
            {"adaptation": {"id": 1, "type": "Heat"}, "value": 10},
            {"adaptation": {"id": 2, "type": "Pluvial Flooding"}, "value": 20},
        ],
    )


class NatureBasedSolutionUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Riprap")
    definition: Optional[str] = Field(None, example="Updated definition")
    cobenefits: Optional[str] = Field(None, example="Enhanced ecosystem services")
    specificdetails: Optional[str] = Field(None, example="Updated detailed information")
    location: Optional[str] = Field(None, example="Updated Coastal Area Y")
    adaptations: Optional[List[AdaptationTargetRead]] = Field(
        None,
        description="List of adaptation types and their corresponding values",
        example=[
            {"adaptation": {"id": 1, "type": "Heat"}, "value": 10},
            {"adaptation": {"id": 2, "type": "Pluvial Flooding"}, "value": 20},
        ],
    )


class NatureBasedSolutionRead(NatureBasedSolutionBase):
    id: int
    adaptations: List[AdaptationTargetRead] = Field(
        alias="solution_targets",
        description="List of AdaptationTarget and their corresponding values",
        default_factory=list,
    )

    class Config:
        from_attributes = True
        populate_by_name = True
