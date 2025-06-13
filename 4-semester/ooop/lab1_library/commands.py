from abc import ABC, abstractmethod
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from library_facade import LibraryFacade


class Command(ABC):
    @abstractmethod
    def execute(self) -> Any:
        pass

    @abstractmethod
    def undo(self) -> Any:
        pass


class BorrowBookCommand(Command):
    def __init__(self, library: 'LibraryFacade', user_id: int, book_id: int):
        self.library = library
        self.user_id = user_id
        self.book_id = book_id
        self.executed = False

    def execute(self) -> bool:
        success = self.library.borrow_book(self.user_id, self.book_id)
        if success:
            self.executed = True
        return success

    def undo(self) -> bool:
        if self.executed:
            return self.library.return_book(self.user_id, self.book_id)
        return False


class ReturnBookCommand(Command):
    def __init__(self, library: 'LibraryFacade', user_id: int, book_id: int):
        self.library = library
        self.user_id = user_id
        self.book_id = book_id
        self.executed = False

    def execute(self) -> bool:
        success = self.library.return_book(self.user_id, self.book_id)
        if success:
            self.executed = True
        return success

    def undo(self) -> bool:
        if self.executed:
            return self.library.borrow_book(self.user_id, self.book_id)
        return False


class AddBookCommand(Command):
    def __init__(self, library: 'LibraryFacade', title: str, author: str,
                 isbn: str, genre: str):
        self.library = library
        self.title = title
        self.author = author
        self.isbn = isbn
        self.genre = genre
        self.book_id = None

    def execute(self) -> int:
        self.book_id = self.library.add_book(self.title, self.author,
                                           self.isbn, self.genre)
        return self.book_id

    def undo(self) -> bool:
        if self.book_id is not None:
            return self.library.remove_book(self.book_id)
        return False


class CommandInvoker:
    def __init__(self):
        self.history = []

    def execute_command(self, command: Command) -> Any:
        result = command.execute()
        self.history.append(command)
        return result

    def undo_last_command(self) -> bool:
        if self.history:
            last_command = self.history.pop()
            return last_command.undo()
        return False