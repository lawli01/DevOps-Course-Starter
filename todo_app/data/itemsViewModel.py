from todo_app.data.item import Item, ItemStatus
from typing import List


class ItemsViewModel:
    def __init__(self, items: List[Item]):
        self._items = items

    @property
    def items(self) -> List[Item]:
        return self._items

    @property
    def to_do_items(self) -> List[Item]:
        return list(filter(lambda x: x.status == ItemStatus.NOT_STARTED, self._items))

    @property
    def doing_items(self) -> List[Item]:
        return list(filter(lambda x: x.status == ItemStatus.IN_PROGRESS, self._items))

    @property
    def done_items(self) -> List[Item]:
        return list(filter(lambda x: x.status == ItemStatus.COMPLETE, self._items))