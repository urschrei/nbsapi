from pydantic import BaseModel


class AdaptationTargetBase(BaseModel):
    "An adaptation target"

    id: int
    type: str

    class Config:
        from_attributes = True


class AdaptationTargetRead(BaseModel):
    "Adaptation targets associated with a Nature-Based Solution"

    adaptation: AdaptationTargetBase
    value: int

    class Config:
        from_attributes = True
