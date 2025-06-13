from abc import ABC, abstractmethod


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


class EmailNotificationObserver(LibraryObserver):
    def on_book_borrowed(self, user_id: int, book_id: int):
        # Simulate email sending
        print(f"[EMAIL] Sending confirmation email for book {book_id} to user {user_id}")

    def on_book_returned(self, user_id: int, book_id: int):
        # Simulate email sending
        print(f"[EMAIL] Sending return confirmation email for book {book_id} to user {user_id}")


class StatisticsObserver(LibraryObserver):
    def __init__(self):
        self.borrow_count = 0
        self.return_count = 0

    def on_book_borrowed(self, user_id: int, book_id: int):
        self.borrow_count += 1
        print(f"[STATS] Total borrows: {self.borrow_count}")

    def on_book_returned(self, user_id: int, book_id: int):
        self.return_count += 1
        print(f"[STATS] Total returns: {self.return_count}")