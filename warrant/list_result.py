from typing import Generic, List, TypeVar

T = TypeVar('T')


class ListResult(Generic[T]):
    def __init__(self, results: List[T], prev_cursor: str = "", next_cursor: str = "") -> None:
        self.results = results
        self.prev_cursor = prev_cursor
        self.next_cursor = next_cursor

    # @staticmethod
    # def from_json(obj):
    #     return
