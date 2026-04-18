import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app, get_book_service
from models import Base
from service import BookService

# StaticPool garante que todas as conexões usem o mesmo banco em memória
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    # sobrescreve get_book_service injetando o serviço apontado para o banco de teste
    def override_service():
        db = TestingSession()
        try:
            yield BookService(db)
        finally:
            db.close()

    app.dependency_overrides[get_book_service] = override_service
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def test_create_book(client):
    response = client.post("/books", json={
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "published_at": "2008-08-01",
        "summary": "Boas práticas de desenvolvimento de software.",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Clean Code"
    assert data["author"] == "Robert C. Martin"
    assert "id" in data


def test_search_by_title(client):
    client.post("/books", json={
        "title": "The Pragmatic Programmer",
        "author": "David Thomas",
        "published_at": "1999-10-20",
    })
    response = client.get("/books/search?title=pragmatic")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert "Pragmatic" in results[0]["title"]


def test_search_by_author(client):
    client.post("/books", json={
        "title": "Refactoring",
        "author": "Martin Fowler",
        "published_at": "1999-07-08",
    })
    response = client.get("/books/search?author=fowler")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["author"] == "Martin Fowler"


def test_get_book_not_found(client):
    response = client.get("/books/999")
    assert response.status_code == 404
