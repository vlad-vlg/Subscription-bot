import datetime

from aiogram import Router, Bot
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_MEMBER
from aiogram.types import ChatMemberUpdated

from infrastructure.database.repo import MYSQLRepository
from tgbot.models.channels import Channels

channel_router = Router()


@channel_router.my_chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def bot_joined_channel(chat_member_updated: ChatMemberUpdated, db_repo: MYSQLRepository, bot: Bot):
    if chat_member_updated.new_chat_member.user.id == bot.id:
        invite_link = await chat_member_updated.chat.create_invite_link(
            name='Bot Invite Link'
        )
        await db_repo.register_channel(
            Channels(
                channel_id=chat_member_updated.chat.id,
                channel_name=chat_member_updated.chat.title,
                channel_invite_link=invite_link.invite_link,
                created_at=datetime.datetime.now(),
                updated_at=datetime.datetime.now()
            )
        )
        await bot.send_message(
            chat_id=chat_member_updated.chat.id,
            text=f'Channel ID: <code>{chat_member_updated.chat.id}</code> was registered'
        )
        return


@channel_router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def user_joined_channel(chat_member_updated: ChatMemberUpdated, db_repo: MYSQLRepository):
    subscription = await db_repo.get_current_subscription_by_user_id(chat_member_updated.from_user.id)
    if not subscription:
        await chat_member_updated.chat.ban(
            user_id=chat_member_updated.from_user.id
        )
