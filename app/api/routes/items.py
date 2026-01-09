from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemRead, ItemUpdate

router = APIRouter(prefix="/items", tags=["items"])

@router.post("/", response_model=ItemRead)
def create_item(item_in: ItemCreate, db: Session = Depends(get_db)) -> Item:
    item = Item(
        name=item_in.name, 
        description=item_in.description, 
        category_id=item_in.category_id
        )
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
    ) -> list[Item]:
    query = db.query(Item)

    if q:
        query = query.filter(Item.name.ilike(f"%{q}%"))

    return query.offset(skip).limit(limit).all()

@router.get("/{item_id}", response_model=ItemRead)
def get_item(item_id: int, db: Session = Depends(get_db)) -> Item:
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.put("/{item_id}", response_model=ItemRead)
def update_item(
    item_id: int,
    item_in: ItemCreate,
    db: Session = Depends(get_db),
) -> Item:
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    if item_in.name is not None:
        item.name = item_in.name

    if item_in.description is not None:
        item.description = item_in.description

    db.commit()
    db.refresh(item)
    return item


@router.delete("/{item_id}", response_model=ItemRead)
def delete_item(item_id: int, db: Session = Depends(get_db)) -> Item:
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(item)
    db.commit()
    return item