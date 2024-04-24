from dataclasses import dataclass
from datetime import datetime


@dataclass
class Channels:
    channel_id: int
    channel_name: str
    channel_invite_link: str
    created_at: datetime
    updated_at: datetime
