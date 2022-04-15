from enum import Enum
from flask_login import UserMixin

class Role(str, Enum):
    WRITER = 'WRITER'
    READER = 'READER'


class User(UserMixin):
    def __init__(self, id: str, role: Role):
        self.id = id
        self.role = role


user_id_to_role = {
    '6570173': Role.WRITER
}