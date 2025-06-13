from typing import List, Dict, Optional
from models import Book, User


class BookRepository:
    def __init__(self):
        self._books: List[Book] = []
        self._next_id = 1

    def add(self, title: str, author: str, isbn: str, genre: str) -> int:
        book = Book(self._next_id, title, author, isbn, genre)
        self._books.append(book)
        self._next_id += 1
        return book.id

    def remove(self, book_id: int) -> bool:
        for i, book in enumerate(self._books):
            if book.id == book_id:
                del self._books[i]
                return True
        return False

    def get_by_id(self, book_id: int) -> Optional[Book]:
        for book in self._books:
            if book.id == book_id:
                return book
        return None

    def get_all(self) -> List[Book]:
        return self._books.copy()

    def count_available(self) -> int:
        return sum(1 for book in self._books if book.available)

    def count_total(self) -> int:
        return len(self._books)

    def set_availability(self, book_id: int, available: bool) -> bool:
        book = self.get_by_id(book_id)
        if book:
            book.available = available
            return True
        return False


class UserRepository:
    def __init__(self):
        self._users: List[User] = []
        self._next_id = 1

    def add(self, name: str, email: str, address: str) -> int:
        user = User(self._next_id, name, email, address)
        self._users.append(user)
        self._next_id += 1
        return user.id

    def get_by_id(self, user_id: int) -> Optional[User]:
        for user in self._users:
            if user.id == user_id:
                return user
        return None

    def get_all(self) -> List[User]:
        return self._users.copy()

    def count_total(self) -> int:
        return len(self._users)


class BorrowRepository:
    def __init__(self):
        self._borrowed_books: Dict[int, List[int]] = {}  # user_id -> [book_ids]

    def borrow_book(self, user_id: int, book_id: int) -> bool:
        if user_id not in self._borrowed_books:
            self._borrowed_books[user_id] = []

        if book_id not in self._borrowed_books[user_id]:
            self._borrowed_books[user_id].append(book_id)
            return True
        return False

    def return_book(self, user_id: int, book_id: int) -> bool:
        if user_id in self._borrowed_books and book_id in self._borrowed_books[user_id]:
            self._borrowed_books[user_id].remove(book_id)
            return True
        return False

    def get_borrowed_books(self, user_id: int) -> List[int]:
        return self._borrowed_books.get(user_id, []).copy()

    def count_active_borrowers(self) -> int:
        return sum(1 for user_id in self._borrowed_books if self._borrowed_books[user_id])

    def get_all_borrowed(self) -> Dict[int, List[int]]:
        return self._borrowed_books.copy()