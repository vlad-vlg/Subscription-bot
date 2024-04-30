from pydantic import BaseModel, Field
from typing import Optional, List


class PaymentStatus:
    WAITING = 'waiting'
    CONFIRMING = 'confirming'
    CONFIRMED = 'confirmed'
    SENDING = 'sending'
    PARTIALLY_PAID = 'partially_paid'
    FINISHED = 'finished'
    FAILED = 'failed'
    REFUNDED = 'refunded'
    EXPIRED = 'expired'


class NowPayment(BaseModel):
    payment_id: str
    payment_status: str
    pay_address: str
    price_amount: float
    price_currency: str
    pay_amount: float
    pay_currency: str
    order_id: Optional[str]
    order_description: Optional[str]
    ipn_callback_url: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]
    purchase_id: Optional[str]
    amount_received: Optional[float]
    payin_extra_id: Optional[str]
    smart_contract: Optional[str]
    network: Optional[str]
    network_precision: Optional[int]
    time_limit: Optional[int]
    burning_percent: Optional[int]
    expiration_estimate_date: Optional[str]


class PaymentUpdate(BaseModel):
    payment_id: int
    invoice_id: Optional[int]
    payment_status: str
    pay_address: str
    payin_extra_id: Optional[str]
    price_amount: float
    price_currency: str
    pay_amount: float
    actually_paid: float
    pay_currency: str
    order_id: str
    order_description: str
    purchase_id: int
    outcome_amount: Optional[float]
    outcome_currency: str
    payout_hash: Optional[str]
    payin_hash: Optional[str]
    created_at: str
    updated_at: str
    burning_percent: str
    type: str
