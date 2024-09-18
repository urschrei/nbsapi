from pydantic import BaseModel


class AdaptationTargetBase(BaseModel):
    id: int
    type: str

    class Config:
        from_attributes = True


class AssociationRead(BaseModel):
    adaptation: AdaptationTargetBase
    value: int

    class Config:
        from_attributes = True
