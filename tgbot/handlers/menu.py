import datetime

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from infrastructure.database.repo import MYSQLRepository
from infrastructure.nowpayments.types import NowPayment
from tgbot.config import Config
from tgbot.keyboards.inline import main_menu_keyboard, MenuKeyboardCD, MenuLevels, subscription_selection_keyboard, \
    crypto_selection_keyboard, payment_confirmation_keyboard
from tgbot.models.payments import NowPaymentsProvider
from tgbot.models.users import Users
from tgbot.services.use_cases import issue_subscription_invoice_to_user

menu_router = Router()


async def starting_message(db_repo: MYSQLRepository, db_user: Users, config: Config) -> tuple[str, InlineKeyboardMarkup]:
    user_subscription = await db_repo.get_current_subscription_by_user_id(db_user.user_id)
    channels = await db_repo.get_all_channels()
    if user_subscription:
        text = '''
ВЫ уже подписаны на каналы.
Ваша текущая подписка: {subscription_name}
Можете перейти в каналы, нажав на кнопку ниже.
'''.format(subscription_name=user_subscription['subscription_name'])
    else:
        text = '''
Здравствуйте! Наши каналы предполагают платный контент.

Пожалуйста, оплатите доступ в этом боте, чтобы получить доступ ко всему материалу в каналах.
'''
    reply_markup = main_menu_keyboard(
        channels=channels,
        support_url=config.misc.support_url
    )
    return text, reply_markup


@menu_router.message(CommandStart())
async def user_start(message: Message,
                     db_repo: MYSQLRepository,
                     config: Config,
                     db_user: Users = None
                     ):
    if not db_user:
        user = Users(
            user_id=message.from_user.id,
            full_name=message.from_user.full_name,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now()
        )
        await db_repo.create_user(user)
    db_user = await db_repo.get_user_by_id(message.from_user.id)
    text, keyboard = await starting_message(db_repo, db_user, config)
    await message.answer(text, reply_markup=keyboard)


@menu_router.callback_query(MenuKeyboardCD.filter(F.level == MenuLevels.MAIN_MENU))
async def back_to_main_menu(query: CallbackQuery,
                            db_repo: MYSQLRepository,
                            db_user: Users,
                            config: Config
                            ):
    text, keyboard = await starting_message(db_repo, db_user, config)
    await query.message.edit_text(text, reply_markup=keyboard)


@menu_router.callback_query(MenuKeyboardCD.filter(F.level == MenuLevels.SUBSCRIPTION_SELECTION))
async def subscription_selection(query: CallbackQuery, db_repo: MYSQLRepository):
    subscriptions = await db_repo.get_all_subscriptions()
    keyboard = subscription_selection_keyboard(subscriptions)
    text = 'У нас есть несколько видов подписок:'
    subs_rows = [
        f'{num}. {subscription.subscription_name} ({subscription.duration} дней): {subscription.subscription_price}'
        for num, subscription in enumerate(subscriptions, start=1)
        ]
    text += '\n' + '\n\n'.join(subs_rows)
    await query.message.edit_text(text, reply_markup=keyboard)


@menu_router.callback_query(MenuKeyboardCD.filter(F.level == MenuLevels.PAYMENT))
async def crypto_selection(query: CallbackQuery,
                           db_repo: MYSQLRepository,
                           callback_data: MenuKeyboardCD,
                           state: FSMContext
                           ):
    subscription_id = int(callback_data.parameter)
    subscription = await db_repo.get_subscription_by_id(subscription_id)
    await state.update_data(subscription_id=subscription_id)
    text = f'Вы выбрали: {subscription.subscription_name}.\n'
    text += f'Стоимость подписки: {subscription.subscription_price} $\n'
    text += 'Выберите криптовалюту для оплаты:'
    keyboard = crypto_selection_keyboard(
        ['BTC',
         'ETH',
         'USDTTRC20'
         ]
    )
    await query.message.edit_text(text, reply_markup=keyboard)


@menu_router.callback_query(MenuKeyboardCD.filter(F.level == MenuLevels.CRYPTO_SELECTION))
async def payment_creation(query: CallbackQuery,
                           db_repo: MYSQLRepository,
                           callback_data: MenuKeyboardCD,
                           nowpayments: NowPaymentsProvider,
                           state: FSMContext,
                           db_user: Users
                           ):
    await query.answer()
    await query.message.delete_reply_markup()
    currency = callback_data.parameter
    state_data = await state.get_data()
    subscription_id = state_data.get('subscription_id')
    # logging.info(f'subscription_id: {subscription_id}')
    invoice: NowPayment = await issue_subscription_invoice_to_user(
        db_repo=db_repo,
        payment_provider=nowpayments,
        subscription_id=subscription_id,
        user_id=query.from_user.id,
        currency=currency
    )
    text = (
        f'Пожалуйста, отправьте не менее <b>{invoice.pay_amount:.6f} {currency.upper()}</b> на адрес ниже. '
        f'Ваш ID платежа: {invoice.payment_id}. \n\n'
        f'🔎 Адрес: <code>{invoice.pay_address}</code>\n'
        f'💰 Сумма: <code>{invoice.pay_amount:.6f}</code>\n\n'
    )
    keyboard = payment_confirmation_keyboard(
        payment_id=invoice.payment_id,
        subscription_id=subscription_id
    )
    await query.message.edit_text(text, reply_markup=keyboard)


