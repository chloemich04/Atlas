from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemRead, ItemUpdate
from app.api.deps import get_current_user
from app.models.user import User
from app.models.tag import Tag


router = APIRouter(prefix="/items", tags=["items"])

@router.post("/", response_model=ItemRead)
def create_item(
    item_in: ItemCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
    ) -> Item:
    item = Item(
        name=item_in.name, 
        description=item_in.description, 
        category_id=item_in.category_id,
        user_id=current_user.id,
    )
    tags = []
    if item_in.tag_ids:
        tags = db.query(Tag).filter(Tag.id.in_(item_in.tag_ids)).all()
        if len(tags) != len(set(item_in.tag_ids)):
            raise HTTPException(status_code=400, detail="One or more tags not found")
    item.tags = tags

    db.add(item)
    db.commit()
    db.refresh(item)

    return item

@router.get("/", response_model=list[ItemRead])
def list_items(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    q: str | None = Query(default=None, min_length=1),
    category_id: int | None = Query(default=None, ge=1),
    current_user: User = Depends(get_current_user),
    ) -> list[Item]:

    query = db.query(Item).filter(Item.user_id == current_user.id)

    if q:
        query = query.filter(Item.name.ilike(f"%{q}%"))
    
    if category_id is not None:
        query = query.filter(Item.category_id == category_id)


    return query.offset(skip).limit(limit).all()

@router.get("/{item_id}", response_model=ItemRead)
def get_item(
    item_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
    ) -> Item:

    item = db.query(Item).filter(Item.id == item_id, Item.user_id == current_user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.put("/{item_id}", response_model=ItemRead)
def update_item(
    item_id: int,
    item_in: ItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Item:
    item = db.query(Item).filter(Item.id == item_id, Item.user_id == current_user.id).first()

    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    if item_in.name is not None:
        item.name = item_in.name

    if item_in.description is not None:
        item.description = item_in.description

    if item_in.category_id is not None:
        item.category_id = item_in.category_id

    if item_in.tag_ids is not None:
        if item_in.tag_ids:
            tags = db.query(Tag).filter(Tag.id.in_(item_in.tag_ids)).all()
            if len(tags) != len(set(item_in.tag_ids)):
                raise HTTPException(status_code=400, detail="One or more tags not found")
            item.tags = tags
        else:
            item.tags = []
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{item_id}", response_model=ItemRead)
def delete_item(
    item_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    ) -> Item:

    item = db.query(Item).filter(Item.id == item_id, Item.user_id == current_user.id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(item)
    db.commit()
    return item