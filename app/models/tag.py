from sqlalchemy import String, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

item_tags = Table(
    "item_tags",
    Base.metadata,
    Column("item_id", ForeignKey("items.id"), primary_key=True),
    Column("tags_id", ForeignKey("tags.id"), primary_key=True),
)

class Tag(Base):
    __tablename__ =  "tags"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)

    items = relationship("Item", secondary=item_tags, back_populates="tags")
    