from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import engine, get_db
from models import Base
from schemas import BookCreate, BookResponse
from service import BookService

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Biblioteca Virtual")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_book_service(db: Session = Depends(get_db)) -> BookService:
    return BookService(db)


@app.post("/books", response_model=BookResponse, status_code=201)
def create_book(book: BookCreate, service: BookService = Depends(get_book_service)):
    return service.create(book)


@app.get("/books", response_model=list[BookResponse])
def list_books(service: BookService = Depends(get_book_service)):
    return service.list_all()


@app.get("/books/search", response_model=list[BookResponse])
def search_books(
    title: str | None = Query(default=None),
    author: str | None = Query(default=None),
    service: BookService = Depends(get_book_service),
):
    return service.search(title, author)


@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int, service: BookService = Depends(get_book_service)):
    book = service.get_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return book
