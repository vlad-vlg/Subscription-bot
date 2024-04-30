import abc
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from infrastructure.nowpayments.api import NowPaymentsAPI
from infrastructure.nowpayments.types import PaymentStatus


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
    api: Any

    @abc.abstractmethod
    async def create_payment(self, usd_amount: float,
                             currency: str,
                             user_subscription_id: int):
        raise NotImplementedError

    @abc.abstractmethod
    async def check_payment(self, payment_id: str) -> bool:
        raise NotImplementedError


@dataclass
class NowPaymentsProvider(PaymentProvider):
    api = NowPaymentsAPI

    async def create_payment(self, usd_amount: float,
                             currency: str,
                             user_subscription_id: int):
        await self.api.get_api_status()

        return await self.api.create_payment(
            price_amount=usd_amount,
            price_currency='usd',
            pay_currency=currency,
            order_id=str(user_subscription_id),
            order_description='Subscription Payment',
        )

    async def check_payment(self, payment_id: str) -> bool:
        await self.api.get_api_status()

        payment_status = await self.api.get_payment_status(payment_id)
        if payment_status.payment_status in (
            PaymentStatus.CONFIRMED,
            PaymentStatus.FINISHED,
            PaymentStatus.SENDING,
            PaymentStatus.WAITING
        ):
            return True
        return False
