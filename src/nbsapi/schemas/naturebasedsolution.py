from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from nbsapi.schemas.adaptationtarget import (
    AdaptationTargetRead,
)


class NatureBasedSolutionBase(BaseModel):
    name: str = Field(..., examples=["Coastal Restoration"])
    definition: str = Field(..., examples=["Definition of the solution"])
    cobenefits: str = Field(..., examples=["Improved biodiversity"])
    specificdetails: str = Field(..., examples=["Detailed information"])
    location: str = Field(..., examples=["Coastal Area X"])


class NatureBasedSolutionCreate(NatureBasedSolutionBase):
    adaptations: List[AdaptationTargetRead] = Field(
        default_factory=list,
        description="List of adaptation types and their corresponding values",
        examples=[
            [
                {"adaptation": {"id": 1, "type": "Heat"}, "value": 10},
                {"adaptation": {"id": 2, "type": "Pluvial Flooding"}, "value": 20},
            ]
        ],
    )


class NatureBasedSolutionUpdate(BaseModel):
    name: Optional[str] = Field(None, examples=["Riprap"])
    definition: Optional[str] = Field(None, examples=["Updated definition"])
    cobenefits: Optional[str] = Field(None, examples=["Enhanced ecosystem services"])
    specificdetails: Optional[str] = Field(
        None, examples=["Updated detailed information"]
    )
    location: Optional[str] = Field(None, examples=["Updated Coastal Area Y"])
    adaptations: Optional[List[AdaptationTargetRead]] = Field(
        None,
        description="List of adaptation types and their corresponding values",
        examples=[
            [
                {"adaptation": {"id": 1, "type": "Heat"}, "value": 10},
                {"adaptation": {"id": 2, "type": "Pluvial Flooding"}, "value": 20},
            ]
        ],
    )


class NatureBasedSolutionRead(NatureBasedSolutionBase):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    id: int
    adaptations: List[AdaptationTargetRead] = Field(
        alias="solution_targets",
        description="List of AdaptationTarget and their corresponding values",
        default_factory=list,
    )
