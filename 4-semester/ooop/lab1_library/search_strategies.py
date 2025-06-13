from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from models import Book


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