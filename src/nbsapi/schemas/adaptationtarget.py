from pydantic import BaseModel, ConfigDict, conint


class AdaptationTargetBase(BaseModel):
    "An adaptation target"

    model_config = ConfigDict(from_attributes=True)

    id: int
    type: str


class AdaptationTargetRead(BaseModel):
    "Adaptation targets associated with a Nature-Based Solution"

    model_config = ConfigDict(from_attributes=True)

    adaptation: AdaptationTargetBase
    value: conint(ge=0, le=100)
