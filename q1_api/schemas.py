from datetime import date

from pydantic import BaseModel


class BookCreate(BaseModel):
    title: str
    author: str
    published_at: date
    summary: str | None = None


class BookResponse(BookCreate):
    id: int

    model_config = {"from_attributes": True}
