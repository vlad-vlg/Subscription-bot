from dataclasses import dataclass
from datetime import datetime


@dataclass
class Users:
    user_id: int
    full_name: str
    created_at: datetime
    updated_at: datetime
    username: str = None
    is_active: bool = False
