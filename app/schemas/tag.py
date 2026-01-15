from pydantic import BaseModel, Field

class TagBase(BaseModel):
    name: str = Field(min_length=1, max_length=50)

class TagCreate(TagBase):
    pass

class TagRead(TagBase):
    id: int

    class Config:
        from_attributes = True