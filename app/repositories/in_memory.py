from typing import Generic, TypeVar

T = TypeVar("T")


class InMemoryRepository(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    def list_all(self) -> list[T]:
        return self._items

    def get_by_id(self, item_id: int) -> T | None:
        for item in self._items:
            if getattr(item, "id", None) == item_id:
                return item
        return None

    def create(self, item: T) -> T:
        self._items.append(item)
        return item

    def update(self, item_id: int, updated_item: T) -> T | None:
        for index, current_item in enumerate(self._items):
            if getattr(current_item, "id", None) == item_id:
                self._items[index] = updated_item
                return updated_item
        return None

    def delete(self, item_id: int) -> bool:
        for index, current_item in enumerate(self._items):
            if getattr(current_item, "id", None) == item_id:
                self._items.pop(index)
                return True
        return False
