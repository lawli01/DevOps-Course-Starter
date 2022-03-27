from enum import Enum
from typing import Optional


class ItemStatus(Enum):
    NOT_STARTED = 'Not Started'
    IN_PROGRESS = 'In Progress'
    COMPLETE = 'Complete'

    @staticmethod
    def from_str(label):
        if label in ('Not Started'):
            return ItemStatus.NOT_STARTED
        elif label in ('In Progress'):
            return ItemStatus.IN_PROGRESS
        elif label in ('Complete'):
            return ItemStatus.COMPLETE
        else:
            raise NotImplementedError


class Item:
    def __init__(self, id: Optional[str], title: str, status: ItemStatus):
        self.id = id
        self.title = title
        self.status = status
