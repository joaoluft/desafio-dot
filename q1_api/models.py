from sqlalchemy import Column, Integer, String, Date, Text

from database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    author = Column(String(255), nullable=False, index=True)
    published_at = Column(Date, nullable=False)
    summary = Column(Text, nullable=True)
