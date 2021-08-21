from enum import Enum
from typing import Optional

class ItemStatus(Enum):
    NOT_STARTED = 'Not Started'
    IN_PROGRESS = 'In Progress'
    COMPLETE = 'Complete'

class Item:
    def __init__(self, id: Optional[str], title: str, status: ItemStatus):
        self.id = id
        self.title = title
        self.status = status