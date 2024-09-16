from enum import Enum
from typing import Dict

from pydantic import BaseModel, Field, conint, field_validator
from schemas.adaptationtarget import AdaptationTargetEnum


class Category(str, Enum):
    heat = "Heat stress mitigation"
    flood = "Flood mitigation"
    energy = "Energy efficiency"


class NatureBasedSolution(BaseModel):
    name: str = Field(..., max_length=100)
    definition: str = Field(
        ..., max_length=500, description="Definition and primary function"
    )

    @field_validator("definition")
    def description_length(cls, value):
        if len(value) > 500:
            raise ValueError("Definition must be 500 characters or less.")
        return value

    specific_details: str = Field(..., max_length=500)

    @field_validator("specific_details")
    def spec_detail_length(cls, value):
        if len(value) > 500:
            raise ValueError("Specific details must be 500 characters or less.")
        return value

    # TODO: do we need both category AND adaptation target?
    adaptation_target: Dict[AdaptationTargetEnum, conint(ge=0, le=100)] = Field(
        ...,
        description="Adaptation target values (0-100) for each of the following: Pluvial flooding, Drought, Heat, Coastal and Fluvial flooding, Groundwater.",
    )
    cobenefits: str = Field(
        ...,
        max_length=200,
        description="Intended positive side effects of the solution",
    )
    category: Category
    location: str
    geometry: dict
