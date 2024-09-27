from pydantic import Field, BaseModel, ConfigDict
from typing_extensions import Annotated


class AdaptationTargetBase(BaseModel):
    "An adaptation target"

    model_config = ConfigDict(from_attributes=True)

    id: int
    type: str


class AdaptationTargetRead(BaseModel):
    "Adaptation targets associated with a Nature-Based Solution"

    model_config = ConfigDict(from_attributes=True)

    adaptation: AdaptationTargetBase
    value: Annotated[int, Field(ge=0, le=100)]
