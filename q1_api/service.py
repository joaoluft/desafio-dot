from sqlalchemy.orm import Session

from models import Book
from schemas import BookCreate


class BookService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, book: BookCreate) -> Book:
        db_book = Book(**book.model_dump())
        self.db.add(db_book)
        self.db.commit()
        self.db.refresh(db_book)
        return db_book

    def list_all(self) -> list[Book]:
        return self.db.query(Book).all()

    def search(self, title: str | None, author: str | None) -> list[Book]:
        query = self.db.query(Book)
        if title:
            query = query.filter(Book.title.ilike(f"%{title}%"))
        if author:
            query = query.filter(Book.author.ilike(f"%{author}%"))
        return query.all()

    def get_by_id(self, book_id: int) -> Book | None:
        return self.db.query(Book).filter(Book.id == book_id).first()
