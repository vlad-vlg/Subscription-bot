from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message

from infrastructure.database.repo import MYSQLRepository


class MYSQLDatabaseMiddleware(BaseMiddleware):
    def __init__(self, aiomysql_pool) -> None:
        self.aio_pool = aiomysql_pool

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        async with self.aio_pool.acquire() as conn:
            db_repo = MYSQLRepository(conn)
            data['conn'] = conn
            data['db_repo'] = db_repo
            effective_user = data.get('event_from_user')
            if effective_user:
                db_user = db_repo.get_user_by_id(effective_user.id)
                data['db_user'] = db_user

            result = await handler(event, data)
        return result
