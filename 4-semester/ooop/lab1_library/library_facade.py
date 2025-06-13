import json
from typing import List, Optional
from models import Book, User, LibraryReport
from repositories import BookRepository, UserRepository, BorrowRepository
from search_strategies import SearchStrategyFactory
from observers import LibraryObserver
from config import LibraryConfig


class LibraryFacade:
    def __init__(self):
        self._book_repo = BookRepository()
        self._user_repo = UserRepository()
        self._borrow_repo = BorrowRepository()
        self._search_strategy = SearchStrategyFactory.create_strategy('composite')
        self._observers: List[LibraryObserver] = []
        self._config = LibraryConfig()

    def add_observer(self, observer: LibraryObserver):
        """Add an observer to the library"""
        self._observers.append(observer)

    def remove_observer(self, observer: LibraryObserver):
        """Remove an observer from the library"""
        if observer in self._observers:
            self._observers.remove(observer)

    def _notify_book_borrowed(self, user_id: int, book_id: int):
        """Notify all observers when a book is borrowed"""
        for observer in self._observers:
            observer.on_book_borrowed(user_id, book_id)

    def _notify_book_returned(self, user_id: int, book_id: int):
        """Notify all observers when a book is returned"""
        for observer in self._observers:
            observer.on_book_returned(user_id, book_id)

    def add_book(self, title: str, author: str, isbn: str, genre: str) -> int:
        """Add a new book to the library"""
        return self._book_repo.add(title, author, isbn, genre)

    def remove_book(self, book_id: int) -> bool:
        """Remove a book from the library"""
        return self._book_repo.remove(book_id)

    def search_books(self, keyword: str, strategy_type: str = None) -> List[Book]:
        """Search for books using the specified strategy"""
        if strategy_type:
            strategy = SearchStrategyFactory.create_strategy(strategy_type)
        else:
            strategy = self._search_strategy

        return strategy.search(self._book_repo.get_all(), keyword)

    def get_all_books(self) -> List[Book]:
        """Get all books in the library"""
        return self._book_repo.get_all()

    def register_user(self, name: str, email: str, address: str) -> int:
        """Register a new user"""
        return self._user_repo.add(name, email, address)

    def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self._user_repo.get_by_id(user_id)

    def get_book(self, book_id: int) -> Optional[Book]:
        """Get book by ID"""
        return self._book_repo.get_by_id(book_id)

    def get_all_users(self) -> List[User]:
        """Get all users"""
        return self._user_repo.get_all()

    def borrow_book(self, user_id: int, book_id: int) -> bool:
        """Borrow a book"""
        user = self._user_repo.get_by_id(user_id)
        book = self._book_repo.get_by_id(book_id)

        if not user or not book or not book.available:
            return False

        # Check book limit
        current_books = len(self._borrow_repo.get_borrowed_books(user_id))
        if current_books >= self._config.max_books_per_user:
            return False

        if self._borrow_repo.borrow_book(user_id, book_id):
            self._book_repo.set_availability(book_id, False)
            self._notify_book_borrowed(user_id, book_id)
            return True
        return False

    def return_book(self, user_id: int, book_id: int) -> bool:
        """Return a book"""
        if self._borrow_repo.return_book(user_id, book_id):
            self._book_repo.set_availability(book_id, True)
            self._notify_book_returned(user_id, book_id)
            return True
        return False

    def get_borrowed_books(self, user_id: int) -> List[Book]:
        """Get books borrowed by a user"""
        book_ids = self._borrow_repo.get_borrowed_books(user_id)
        books = []
        for book_id in book_ids:
            book = self._book_repo.get_by_id(book_id)
            if book:
                books.append(book)
        return books

    def generate_report(self) -> LibraryReport:
        """Generate a library report"""
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
        """Save library data to a file"""
        try:
            data = {
                'books': [book.to_dict() for book in self._book_repo.get_all()],
                'users': [user.to_dict() for user in self._user_repo.get_all()],
                'borrowed_books': self._borrow_repo.get_all_borrowed()
            }
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False

    def load_data(self, filename: str) -> bool:
        """Load library data from a file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Clear current data
            self._book_repo = BookRepository()
            self._user_repo = UserRepository()
            self._borrow_repo = BorrowRepository()

            # Load books
            for book_data in data.get('books', []):
                book = Book.from_dict(book_data)
                self._book_repo._books.append(book)
                self._book_repo._next_id = max(self._book_repo._next_id, book.id + 1)

            # Load users
            for user_data in data.get('users', []):
                user = User.from_dict(user_data)
                self._user_repo._users.append(user)
                self._user_repo._next_id = max(self._user_repo._next_id, user.id + 1)

            # Load borrow information
            self._borrow_repo._borrowed_books = data.get('borrowed_books', {})
            # Convert keys to int (JSON serializes them as strings)
            self._borrow_repo._borrowed_books = {
                int(k): v for k, v in self._borrow_repo._borrowed_books.items()
            }

            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False

    def get_config(self) -> dict:
        """Get current configuration"""
        return self._config.get_config()

    def update_config(self, **kwargs):
        """Update configuration settings"""
        self._config.update_config(**kwargs)
