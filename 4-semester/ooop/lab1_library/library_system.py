from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
import json
from dataclasses import dataclass, asdict
from enum import Enum


# Strategy Pattern для пошуку
class SearchStrategy(ABC):
    @abstractmethod
    def search(self, books: List['Book'], keyword: str) -> List['Book']:
        pass


class TitleSearchStrategy(SearchStrategy):
    def search(self, books: List['Book'], keyword: str) -> List['Book']:
        return [book for book in books if keyword.lower() in book.title.lower()]


class AuthorSearchStrategy(SearchStrategy):
    def search(self, books: List['Book'], keyword: str) -> List['Book']:
        return [book for book in books if keyword.lower() in book.author.lower()]


class GenreSearchStrategy(SearchStrategy):
    def search(self, books: List['Book'], keyword: str) -> List['Book']:
        return [book for book in books if keyword.lower() in book.genre.lower()]


class CompositeSearchStrategy(SearchStrategy):
    def search(self, books: List['Book'], keyword: str) -> List['Book']:
        results = []
        for book in books:
            if (keyword.lower() in book.title.lower() or
                    keyword.lower() in book.author.lower() or
                    keyword.lower() in book.genre.lower()):
                results.append(book)
        return results


# Data classes для інкапсуляції даних
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


# Repository Pattern для управління даними
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


# Observer Pattern для подій
class LibraryObserver(ABC):
    @abstractmethod
    def on_book_borrowed(self, user_id: int, book_id: int):
        pass

    @abstractmethod
    def on_book_returned(self, user_id: int, book_id: int):
        pass


class LibraryEventLogger(LibraryObserver):
    def on_book_borrowed(self, user_id: int, book_id: int):
        print(f"[LOG] Book {book_id} borrowed by user {user_id}")

    def on_book_returned(self, user_id: int, book_id: int):
        print(f"[LOG] Book {book_id} returned by user {user_id}")


# Command Pattern для операцій
class Command(ABC):
    @abstractmethod
    def execute(self) -> Any:
        pass


class BorrowBookCommand(Command):
    def __init__(self, library: 'LibraryFacade', user_id: int, book_id: int):
        self.library = library
        self.user_id = user_id
        self.book_id = book_id

    def execute(self) -> bool:
        return self.library.borrow_book(self.user_id, self.book_id)


class ReturnBookCommand(Command):
    def __init__(self, library: 'LibraryFacade', user_id: int, book_id: int):
        self.library = library
        self.user_id = user_id
        self.book_id = book_id

    def execute(self) -> bool:
        return self.library.return_book(self.user_id, self.book_id)


# Singleton Pattern для конфігурації
class LibraryConfig:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.max_books_per_user = 5
            self.default_search_strategy = "composite"
            self._initialized = True


# Factory Pattern для створення стратегій пошуку
class SearchStrategyFactory:
    @staticmethod
    def create_strategy(strategy_type: str) -> SearchStrategy:
        strategies = {
            'title': TitleSearchStrategy(),
            'author': AuthorSearchStrategy(),
            'genre': GenreSearchStrategy(),
            'composite': CompositeSearchStrategy()
        }
        return strategies.get(strategy_type, CompositeSearchStrategy())


# Facade Pattern для спрощення інтерфейсу
class LibraryFacade:
    def __init__(self):
        self._book_repo = BookRepository()
        self._user_repo = UserRepository()
        self._borrow_repo = BorrowRepository()
        self._search_strategy = SearchStrategyFactory.create_strategy('composite')
        self._observers: List[LibraryObserver] = []
        self._config = LibraryConfig()

    def add_observer(self, observer: LibraryObserver):
        self._observers.append(observer)

    def remove_observer(self, observer: LibraryObserver):
        if observer in self._observers:
            self._observers.remove(observer)

    def _notify_book_borrowed(self, user_id: int, book_id: int):
        for observer in self._observers:
            observer.on_book_borrowed(user_id, book_id)

    def _notify_book_returned(self, user_id: int, book_id: int):
        for observer in self._observers:
            observer.on_book_returned(user_id, book_id)

    def add_book(self, title: str, author: str, isbn: str, genre: str) -> int:
        return self._book_repo.add(title, author, isbn, genre)

    def remove_book(self, book_id: int) -> bool:
        return self._book_repo.remove(book_id)

    def search_books(self, keyword: str, strategy_type: str = None) -> List[Book]:
        if strategy_type:
            strategy = SearchStrategyFactory.create_strategy(strategy_type)
        else:
            strategy = self._search_strategy

        return strategy.search(self._book_repo.get_all(), keyword)

    def register_user(self, name: str, email: str, address: str) -> int:
        return self._user_repo.add(name, email, address)

    def get_user(self, user_id: int) -> Optional[User]:
        return self._user_repo.get_by_id(user_id)

    def get_book(self, book_id: int) -> Optional[Book]:
        return self._book_repo.get_by_id(book_id)

    def borrow_book(self, user_id: int, book_id: int) -> bool:
        user = self._user_repo.get_by_id(user_id)
        book = self._book_repo.get_by_id(book_id)

        if not user or not book or not book.available:
            return False

        # Перевірка ліміту книг
        current_books = len(self._borrow_repo.get_borrowed_books(user_id))
        if current_books >= self._config.max_books_per_user:
            return False

        if self._borrow_repo.borrow_book(user_id, book_id):
            self._book_repo.set_availability(book_id, False)
            self._notify_book_borrowed(user_id, book_id)
            return True
        return False

    def return_book(self, user_id: int, book_id: int) -> bool:
        if self._borrow_repo.return_book(user_id, book_id):
            self._book_repo.set_availability(book_id, True)
            self._notify_book_returned(user_id, book_id)
            return True
        return False

    def get_borrowed_books(self, user_id: int) -> List[Book]:
        book_ids = self._borrow_repo.get_borrowed_books(user_id)
        books = []
        for book_id in book_ids:
            book = self._book_repo.get_by_id(book_id)
            if book:
                books.append(book)
        return books

    def generate_report(self) -> LibraryReport:
        total_books = self._book_repo.count_total()
        available_books = self._book_repo.count_available()
        borrowed_books = total_books - available_books
        total_users = self._user_repo.count_total()
        active_borrowers = self._borrow_repo.count_active_borrowers()

        return LibraryReport(
            total_books=total_books,
            available_books=available_books,
            borrowed_books=borrowed_books,
            total_users=total_users,
            active_borrowers=active_borrowers
        )

    def save_data(self, filename: str) -> bool:
        try:
            data = {
                'books': [book.to_dict() for book in self._book_repo.get_all()],
                'users': [user.to_dict() for user in self._user_repo.get_all()],
                'borrowed_books': self._borrow_repo.get_all_borrowed()
            }
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False

    def load_data(self, filename: str) -> bool:
        try:
            with open(filename, 'r') as f:
                data = json.load(f)

            # Очищуємо поточні дані
            self._book_repo = BookRepository()
            self._user_repo = UserRepository()
            self._borrow_repo = BorrowRepository()

            # Завантажуємо книги
            for book_data in data.get('books', []):
                book = Book.from_dict(book_data)
                self._book_repo._books.append(book)
                self._book_repo._next_id = max(self._book_repo._next_id, book.id + 1)

            # Завантажуємо користувачів
            for user_data in data.get('users', []):
                user = User.from_dict(user_data)
                self._user_repo._users.append(user)
                self._user_repo._next_id = max(self._user_repo._next_id, user.id + 1)

            # Завантажуємо інформацію про позички
            self._borrow_repo._borrowed_books = data.get('borrowed_books', {})
            # Конвертуємо ключі в int (JSON серіалізує їх як строки)
            self._borrow_repo._borrowed_books = {
                int(k): v for k, v in self._borrow_repo._borrowed_books.items()
            }

            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False


# Template Method Pattern для CLI
class LibraryCLI:
    def __init__(self):
        self.library = LibraryFacade()
        self.library.add_observer(LibraryEventLogger())
        self._setup_sample_data()

    def _setup_sample_data(self):
        """Template method для ініціалізації даних"""
        self.library.add_book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565", "Fiction")
        self.library.add_book("To Kill a Mockingbird", "Harper Lee", "9780061120084", "Fiction")
        self.library.add_book("1984", "George Orwell", "9780451524935", "Dystopian")
        self.library.register_user("John Doe", "john@example.com", "123 Main St")

    def run(self):
        """Основний цикл CLI"""
        while True:
            self._display_menu()
            choice = input("Enter your choice: ")

            if choice == '0':
                print("Goodbye!")
                break

            self._handle_choice(choice)

    def _display_menu(self):
        """Відображення меню"""
        print("\nLibrary Management System")
        print("1. Add a book")
        print("2. Search for books")
        print("3. Register a user")
        print("4. Borrow a book")
        print("5. Return a book")
        print("6. View borrowed books")
        print("7. Generate report")
        print("8. Save data")
        print("9. Load data")
        print("10. Delete book")
        print("0. Exit")

    def _handle_choice(self, choice: str):
        """Обробка вибору користувача"""
        handlers = {
            '1': self._add_book,
            '2': self._search_books,
            '3': self._register_user,
            '4': self._borrow_book,
            '5': self._return_book,
            '6': self._view_borrowed_books,
            '7': self._generate_report,
            '8': self._save_data,
            '9': self._load_data,
            '10': self._delete_book
        }

        handler = handlers.get(choice)
        if handler:
            handler()
        else:
            print("Invalid choice. Please try again.")

    def _add_book(self):
        title = input("Enter title: ")
        author = input("Enter author: ")
        isbn = input("Enter ISBN: ")
        genre = input("Enter genre: ")
        book_id = self.library.add_book(title, author, isbn, genre)
        print(f"Book added with ID: {book_id}")

    def _search_books(self):
        keyword = input("Enter search keyword: ")
        results = self.library.search_books(keyword)
        print("\nSearch Results:")
        for book in results:
            status = "Available" if book.available else "Borrowed"
            print(f"ID: {book.id}, Title: {book.title}, Author: {book.author}, Status: {status}")

    def _register_user(self):
        name = input("Enter name: ")
        email = input("Enter email: ")
        address = input("Enter address: ")
        user_id = self.library.register_user(name, email, address)
        print(f"User registered with ID: {user_id}")

    def _borrow_book(self):
        try:
            user_id = int(input("Enter user ID: "))
            book_id = int(input("Enter book ID: "))
            command = BorrowBookCommand(self.library, user_id, book_id)
            success = command.execute()
            print("Book borrowed successfully" if success else "Failed to borrow book")
        except ValueError:
            print("Invalid input. Please enter valid numbers.")

    def _return_book(self):
        try:
            user_id = int(input("Enter user ID: "))
            book_id = int(input("Enter book ID: "))
            command = ReturnBookCommand(self.library, user_id, book_id)
            success = command.execute()
            print("Book returned successfully" if success else "Failed to return book")
        except ValueError:
            print("Invalid input. Please enter valid numbers.")

    def _view_borrowed_books(self):
        try:
            user_id = int(input("Enter user ID: "))
            books = self.library.get_borrowed_books(user_id)
            print("\nBorrowed Books:")
            for book in books:
                print(f"ID: {book.id}, Title: {book.title}, Author: {book.author}")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    def _generate_report(self):
        report = self.library.generate_report()
        print("\nLibrary Report:")
        print(f"Total Books: {report.total_books}")
        print(f"Available Books: {report.available_books}")
        print(f"Borrowed Books: {report.borrowed_books}")
        print(f"Total Users: {report.total_users}")
        print(f"Active Borrowers: {report.active_borrowers}")

    def _save_data(self):
        filename = input("Enter filename to save: ")
        success = self.library.save_data(filename)
        print("Data saved successfully" if success else "Failed to save data")

    def _load_data(self):
        filename = input("Enter filename to load: ")
        success = self.library.load_data(filename)
        print("Data loaded successfully" if success else "Failed to load data")

    def _delete_book(self):
        try:
            book_id = int(input("Enter book ID: "))
            success = self.library.remove_book(book_id)
            print("Deletion success" if success else "Invalid book ID")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


# Main execution
if __name__ == "__main__":
    cli = LibraryCLI()
    cli.run()