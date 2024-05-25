from enum import IntEnum
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from tgbot.models.channels import Channels
from tgbot.models.subscriptions import Subscriptions


class MenuLevels(IntEnum):
    MAIN_MENU = 1
    SUBSCRIPTION_SELECTION = 2
    PAYMENT = 3
    CRYPTO_SELECTION = 4
    PAYMENT_CONFIRMATION = 5


class MenuKeyboardCD(CallbackData, prefix='main_menu'):
    level: MenuLevels
    parameter: str = None


def main_menu_keyboard(channels: list[Channels], support_url: str = None):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text='📊 Подписки',
        callback_data=MenuKeyboardCD(
            level=MenuLevels.SUBSCRIPTION_SELECTION,
        )
    )
    if channels:
        for channel in channels:
            keyboard.button(
                text=f'🔗 {channel.channel_name}',
                url=channel.channel_invite_link
            )
    if support_url:
        keyboard.button(
            text='🔗 Связь с администрацией',
            url=support_url
        )
    keyboard.adjust(2)
    return keyboard.as_markup()


def subscription_selection_keyboard(subscriptions: list[Subscriptions]):
    keyboard = InlineKeyboardBuilder()
    for subscription in subscriptions:
        keyboard.button(
            text=f'📊 {subscription.subscription_name} - {subscription.subscription_price} $',
            callback_data=MenuKeyboardCD(
                level=MenuLevels.PAYMENT,
                parameter=str(subscription.subscription_id)
            )
        )
    keyboard.button(
        text='↩️ Назад',
        callback_data=MenuKeyboardCD(level=MenuLevels.MAIN_MENU)
    )
    keyboard.adjust(1)
    return keyboard.as_markup()


def crypto_selection_keyboard(currencies: list[str]):
    keyboard = InlineKeyboardBuilder()
    for currency in currencies:
        keyboard.button(
            text=f'💰 {currency}',
            callback_data=MenuKeyboardCD(
                level=MenuLevels.CRYPTO_SELECTION,
                parameter=currency,
            )
        )
    keyboard.adjust(2)
    keyboard.button(
        text='↩️ Назад',
        callback_data=MenuKeyboardCD(level=MenuLevels.SUBSCRIPTION_SELECTION)
    )
    return keyboard.as_markup()


def payment_confirmation_keyboard(payment_id: int, subscription_id: int):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text='✅ Я оплатил',
        callback_data=MenuKeyboardCD(
            level=MenuLevels.PAYMENT_CONFIRMATION,
            parameter=str(payment_id)
        )
    )
    keyboard.button(
        text='❌ Отмена',
        callback_data=MenuKeyboardCD(
            level=MenuLevels.PAYMENT,
            parameter=str(subscription_id)
        )
    )
    keyboard.adjust(1)
    return keyboard.as_markup()
