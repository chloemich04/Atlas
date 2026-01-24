from pydantic import BaseModel, Field
from app.schemas.tag import TagRead
from app.schemas.category import CategoryRead

class ItemBase(BaseModel):
    name : str = Field(min_length=1, max_length=200)
    description : str | None = Field(default=None, max_length=1000)
    category_id : int | None = None
    


class ItemCreate(ItemBase):
    tag_ids: list[int] = []

class ItemUpdate(ItemBase):
    name : str | None = Field(default=None, min_length=1, max_length=200)
    description : str | None = Field(default=None, max_length=1000) 
    category_id : int | None = None
    tag_ids: list[int] | None = None

class ItemRead(ItemBase):
    id : int
    tags: list[TagRead] = []
    category: CategoryRead | None = None

    class Config:
        from_attributes = True
