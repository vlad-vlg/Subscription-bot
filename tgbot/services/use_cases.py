from datetime import datetime, timedelta

from infrastructure.database.repo import MYSQLRepository
from tgbot.models.payments import PaymentProvider, Payments
from tgbot.models.subscriptions import UserSubscriptions


async def issue_subscription_invoice_to_user(
        db_repo: MYSQLRepository,
        payment_provider: PaymentProvider,
        subscription_id: int,
        user_id: int,
        currency: str,
):
    # Get subscription info from DB
    # Create record for user_subscriptions
    # Create invoice
    # Insert invoice into DB
    # Return invoice info
    subscription = await db_repo.get_subscription_by_id(subscription_id)
    user_subscription_id = await db_repo.create_user_subscription(
        UserSubscriptions(
            user_id=user_id,
            subscription_id=subscription_id,
            subscription_start_date=datetime.now(),
            subscription_end_date=datetime.now() + timedelta(
                days=subscription.duration
            ),
            paid=False,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
    )
    invoice = await payment_provider.create_payment(
        usd_amount=subscription.subscription_price,
        currency=currency,
        user_subscription_id=user_subscription_id,
    )
    await db_repo.create_payment(
        Payments(
            payment_id=invoice.payment_id,
            user_id=user_id,
            user_subscription_id=user_subscription_id,
            usd_amount=subscription.subscription_price,
            pay_amount=invoice.pay_amount,
            currency=currency,
            pay_address=invoice.pay_address,
            paid=False,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            comment=f'Subscription invoice for user_id: {user_id} {subscription_id}'
        )
    )
    return invoice


async def activate_subscription_by_payment_id(
        db_repo: MYSQLRepository,
        payment_provider: PaymentProvider,
        payment_id: str,
):
    # Get payment info from DB
    # Check payment status
    # Update payment status
    # Update user_subscription status
    payment = await db_repo.get_payment_by_id(payment_id)
    payment_status = await payment_provider.check_payment(payment_id)
    if payment_status:
        payment.update_payment(True)
        await db_repo.update_payment(payment)
        await db_repo.update_user_subscription_by_id(
            user_subscription_id=payment.user_subscription_id,
            paid=payment_status,
        )
        return True
    return False



