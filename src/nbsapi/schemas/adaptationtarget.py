from enum import Enum

from pydantic import BaseModel, Field, conint, field_validator


class AdaptationTargetEnum(str, Enum):
    """The kinds of protection or enhancement that the NbS provides"""

    pluvial_flooding = "Pluvial flooding"
    drought = "Drought"
    heat = "Heat"
    coastal_fluvial_flooding = "Coastal and Fluvial flooding"
    groundwater = "Groundwater"


class AdaptationTarget(BaseModel):
    target: AdaptationTargetEnum
    value: conint(ge=0, le=100)
