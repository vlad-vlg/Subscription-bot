from django.db import models

# Create your models here.
# @dataclass
# class Users:
#     user_id: int
#     full_name: str
#     created_at: datetime
#     updated_at: datetime
#     username: str = None
#     is_active: bool = False


class Users(models.Model):
    user_id = models.BigIntegerField(primary_key=True,
                                     verbose_name='ID пользователя')
    full_name = models.CharField(max_length=255, verbose_name='Полное имя')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    username = models.CharField(max_length=100, null=True, verbose_name='Username')
    is_active = models.BooleanField(default=False)

    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.user_id} - {self.full_name}'


# @dataclass
# class Subscriptions:
#     subscription_name: str
#     subscription_description: str
#     subscription_price: int
#     duration: int
#     access_to_paid_content: bool
#     created_at: datetime
#     updated_at: datetime
#     subscription_id: int = None
#
#
# @dataclass
# class UserSubscriptions:
#     user_id: int
#     subscription_id: int
#     subscription_start_date: datetime
#     subscription_end_date: datetime
#     paid: bool
#     created_at: datetime
#     updated_at: datetime
#     user_subscription_id: int = None


class Subscriptions(models.Model):
    subscription_id = models.AutoField(primary_key=True, verbose_name='ID подписки')
    subscription_name = models.CharField(max_length=255, verbose_name='Название подписки')
    subscription_description = models.TextField(verbose_name='Описание подписки')
    subscription_price = models.IntegerField(verbose_name='Цена подписки')
    duration = models.IntegerField(verbose_name='Длительность подписки')
    access_to_paid_content = models.BooleanField(verbose_name='Доступ к платному контенту')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        db_table = 'subscriptions'
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.subscription_id} - {self.subscription_name}'


class UserSubscriptions(models.Model):
    user_id: int
    subscription_id: int
    subscription_start_date: datetime
    subscription_end_date: datetime
    paid: bool
    created_at: datetime
    updated_at: datetime
    user_subscription_id: int = None