from aiogram import Router, Bot
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_MEMBER
from aiogram.types import ChatMemberUpdated

from infrastructure.database.repo import MYSQLRepository

channel_router = Router()


@channel_router.my_chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def on_channel_join(chat_member: ChatMemberUpdated, db_repo: MYSQLRepository, bot: Bot):
    if chat_member.new_chat_member.user.id == bot.id:
        invitation_link = await chat_member.chat.create_invite_link(
            name='Bot Invite Link',
        )
        await db_repo.register_channel(
            Channel(
                channel_id=chat_member.chat.id,
                channel_name=chat_member.chat.title,
                created_at=chat_member.date,
                updated_at=chat_member.date,
                channel_invite_link=invitation_link.invite_link
            )
        )
        await bot.send_message(
            chat_id=chat_member.chat.id,
            text=f'Channel ID: <code>{chat_member.chat.id}</code> was registered'
        )
        return