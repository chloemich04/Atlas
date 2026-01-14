from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryRead
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/", response_model=CategoryRead)
def create_category(
    category_in: CategoryCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    ) -> Category:

    category = Category(name=category_in.name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.get("/", response_model=list[CategoryRead])
def list_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    ) -> list[Category]:

    return db.query(Category).all()

@router.get("/{category_id}", response_model=CategoryRead)
def get_category(
    category_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    ) -> Category:

    category = db.query(Category).filter(Category.id == category_id).first()

    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category