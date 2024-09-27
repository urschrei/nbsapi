from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated


class AdaptationTargetBase(BaseModel):
    "An adaptation target"

    model_config = ConfigDict(from_attributes=True)

    type: str


class AdaptationTargetRead(BaseModel):
    "Adaptation targets associated with a Nature-Based Solution"

    model_config = ConfigDict(
        json_schema_extra={"examples": [{"adaptation": {"type": "Heat"}, "value": 80}]},
        from_attributes=True,
    )

    adaptation: AdaptationTargetBase
    value: Annotated[int, Field(ge=0, le=100)]
