import abc
import logging
from dataclasses import asdict
import aiomysql
from tgbot.models.channels import Channels
from tgbot.models.payments import Payments
from tgbot.models.subscriptions import Subscriptions, UserSubscriptions
from tgbot.models.users import Users


class DatabaseRepository(abc.ABC):
    @abc.abstractmethod
    async def create_user(self, user: Users) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_user_by_id(self, user_id: int) -> Users:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_all_subscriptions(self) -> list[Subscriptions]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_subscription_by_id(self, subscription_id: int) -> Subscriptions:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_current_subscription_by_user_id(self, user_id: int) -> dict:
        raise NotImplementedError

    @abc.abstractmethod
    async def create_user_subscription(self, user_subscription: UserSubscriptions) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def update_user_subscription_by_id(self, user_subscription_id: int, paid: bool):
        raise NotImplementedError

    @abc.abstractmethod
    async def create_payment(self, payment: Payments) -> Payments:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_payment_by_id(self, payment_id: int) -> Payments:
        raise NotImplementedError

    @abc.abstractmethod
    async def update_payment(self, payment: Payments):
        raise NotImplementedError

    @abc.abstractmethod
    async def register_channel(self, channel: Channels) -> Channels:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_all_channels(self) -> list[Channels]:
        raise NotImplementedError


class MYSQLRepository(DatabaseRepository):
    def __init__(self, db_connection: aiomysql.Connection):
        self.conn: aiomysql.Connection = db_connection

    async def create_user(self, user: Users):
        async with self.conn.cursor() as cursor:
            user_data = asdict(user)
            columns = ', '.join(user_data.keys())
            values = ', '.join(['%s'] * len(user_data))
            query = f'INSERT INTO users ({columns}) VALUES ({values})'
            await cursor.execute(query, tuple(user_data.values()))
        await self.conn.commit()

    async def get_user_by_id(self, user_id: int) -> Users:
        async with self.conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute('SELECT * FROM users WHERE user_id = %s', (user_id,))
            user_data = await cursor.fetchone()
            return Users(**user_data)

    async def get_all_subscriptions(self) -> list[Subscriptions]:
        async with self.conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute('SELECT * FROM subscriptions')
            subscriptions_data = await cursor.fetchall()
            return [Subscriptions(**sub) for sub in subscriptions_data]

    async def get_subscription_by_id(self, subscription_id: int) -> Subscriptions:
        async with self.conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute('SELECT * FROM subscriptions WHERE id = %s', (subscription_id,))
            subscription_data = await cursor.fetchone()
            return Subscriptions(**subscription_data)

    async def get_current_subscription_by_user_id(self, user_id: int) -> dict:
        async with self.conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute('SELECT * FROM Subscriptions '
                                 'JOIN user_subscriptions '
                                 'ON Subscriptions.subscription_id = user_subscriptions.subscription_id '
                                 'WHERE user_id = %s '
                                 'AND paid = 1 '
                                 'AND subscription_end_date > NOW() '
                                 'AND subscription_start_date < NOW()',
                                 (user_id,))
            user_subscription_data = await cursor.fetchone()
            return user_subscription_data

    async def create_user_subscription(self, user_subscription: UserSubscriptions) -> None:
        async with self.conn.cursor(aiomysql.DictCursor) as cursor:
            user_subscription_data = asdict(user_subscription)
            columns = ', '.join(user_subscription_data.keys())
            values = ', '.join(['%s'] * len(user_subscription_data))
            query = f'INSERT INTO user_subscriptions ({columns}) VALUES ({values})'
            await cursor.execute(query, tuple(user_subscription_data.values()))
            user_sub_id = cursor.lastrowid
            logging.info(f'New User_subscription_id: {user_sub_id}')
        await self.conn.commit()
        return user_sub_id

    async def update_user_subscription_by_id(self, user_subscription_id: int, paid: bool):
        async with self.conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute('UPDATE user_subscriptions SET paid = %s WHERE user_subscription_id = %s',
                                 (paid, user_subscription_id))
        await self.conn.commit()

    async def create_payment(self, payment: Payments) -> None:
        async with self.conn.cursor() as cursor:
            payment_data = asdict(payment)
            columns = ', '.join(payment_data.keys())
            values = ', '.join(['%s' for _ in payment_data.values()])
            query = f'INSERT INTO Payments ({columns}) VALUES ({values})'
            await cursor.execute(query, tuple(payment_data.values()))
        await self.conn.commit()

    async def get_payment_by_id(self, payment_id: str) -> Payments:
        async with self.conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute('SELECT * FROM Payments WHERE payment_id = %s', (payment_id,))
            payment_data = await cursor.fetchone()
            return Payments(**payment_data)

    async def update_payment(self, payment: Payments) -> Payments:
        async with self.conn.cursor() as cursor:
            payment_data = asdict(payment)
            columns_values = ', '.join([
                f'{column} = %({column})s' for column in payment_data.keys()
            ])
            query = (f'UPDATE Payments SET {columns_values} '
                     f'WHERE payment_id = %(payment_id)s')
            await cursor.execute(query, payment_data)
        await self.conn.commit()
        return await self.get_payment_by_id(payment.payment_id)

    async def register_channel(self, channel: Channels) -> Channels:
        async with self.conn.cursor() as cursor:
            channel_data = asdict(channel)
            columns = ', '.join(channel_data.keys())
            values = ', '.join(['%s' for _ in channel_data.values()])
            query = f'INSERT INTO Channels ({columns}) VALUES ({values})'
            await cursor.execute(query, tuple(channel_data.values()))
        await self.conn.commit()

    async def get_all_channels(self) -> list[Channels]:
        async with self.conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute('SELECT * FROM Channels')
            channels_data = await cursor.fetchall()
            return [Channels(**channel) for channel in channels_data]
