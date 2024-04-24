from dataclasses import dataclass
from datetime import datetime


@dataclass
class Subscriptions:
    subscription_name: str
    subscription_description: str
    subscription_price: int
    duration: int
    access_to_paid_content: bool
    created_at: datetime
    updated_at: datetime
    subscription_id: int = None


@dataclass
class UserSubscriptions:
    user_id: int
    subscription_id: int
    subscription_start_date: datetime
    subscription_end_date: datetime
    paid: bool
    created_at: datetime
    updated_at: datetime
    user_subscription_id: int = None
    