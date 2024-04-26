import abc
from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class Payments:
    payment_id: str
    user_id: int
    user_subscription_id: int
    usd_amount: float
    pay_amount: float
    currency: str
    pay_address: str
    paid: bool
    created_at: datetime
    updated_at: datetime
    comment: str = None

    def update_payment(self, new_status: bool):
        if new_status:
            self.paid = True
            self.updated_at = datetime.now()
            return True
        return False


@dataclass
class PaymentProvider(abc.ABC):
    api: Any = None

    @abc.abstractmethod
    async def create_payment(self, usd_amount: float,
                             currency: str,
                             user_subscription_id: int):
        raise NotImplementedError

    @abc.abstractmethod
    async def check_payment(self, payment_id: str) -> bool:
        raise NotImplementedError
