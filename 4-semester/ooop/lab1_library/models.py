from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Book:
    id: int
    title: str
    author: str
    isbn: str
    genre: str
    available: bool = True

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'Book':
        return cls(**data)


@dataclass
class User:
    id: int
    name: str
    email: str
    address: str
    active: bool = True

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        return cls(**data)


@dataclass
class LibraryReport:
    total_books: int
    available_books: int
    borrowed_books: int
    total_users: int
    active_borrowers: int