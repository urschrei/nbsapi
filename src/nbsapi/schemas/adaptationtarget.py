from pydantic import BaseModel


class AdaptationTargetBase(BaseModel):
    id: int
    target: str

    class Config:
        from_attributes = True


class AssociationRead(BaseModel):
    target: AdaptationTargetBase
    value: int

    class Config:
        from_attributes = True
