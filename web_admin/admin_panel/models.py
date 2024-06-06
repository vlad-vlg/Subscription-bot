from django.db import models


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
    user_subscription_id = models.AutoField(primary_key=True, verbose_name='ID подписки пользователя')
    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='ID пользователя')
    subscription = models.ForeignKey(Subscriptions, on_delete=models.CASCADE, verbose_name='ID подписки')
    subscription_start = models.DateTimeField(verbose_name='Дата начала подписки')
    valid_until = models.DateTimeField(verbose_name='Дата окончания подписки')
    paid = models.BooleanField(verbose_name='Оплачена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        db_table = 'user_subscriptions'
        verbose_name = 'Подписка пользователя'
        verbose_name_plural = 'Подписки пользователей'

    def __str__(self):
        return f'{self.user_subscription_id} - {self.user}- {self.subscription}'


class Payments(models.Model):
    payment_id = models.CharField(max_length=255, primary_key=True, verbose_name='ID платежа')
    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='ID пользователя')
    user_subscription = models.ForeignKey(UserSubscriptions, on_delete=models.CASCADE,
                                          verbose_name='ID подписки пользователя')
    pay_address = models.CharField(max_length=255, verbose_name='Адрес платежа')
    currency = models.CharField(max_length=10, verbose_name='Валюта')
    usd_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма в USD')
    pay_amount = models.DecimalField(max_digits=10, decimal_places=8, verbose_name='Сумма в валюте платежа')
    paid = models.BooleanField(verbose_name='Статус оплаты')
    comment = models.TextField(null=True, verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        db_table = 'payments'
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'

    def __str__(self):
        return f'{self.payment_id} - {self.user}- {self.user_subscription}'


class Channels(models.Model):
    channel_id = models.BigIntegerField(primary_key=True, verbose_name='ID канала')
    channel_name = models.CharField(max_length=255, verbose_name='Название канала')
    channel_invite_link = models.CharField(max_length=255, verbose_name='Invite ссылка')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        db_table = 'channels'
        verbose_name = 'Канал'
        verbose_name_plural = 'Каналы'

    def __str__(self):
        return f'{self.channel_id} - {self.channel_name}'


class PaidContent(models.Model):
    paid_content_id = models.AutoField(primary_key=True, verbose_name='ID платного контента')
    content_name = models.CharField(max_length=255, verbose_name='Название контента')
    url = models.CharField(max_length=255, verbose_name='URL')
    content_HTML = models.TextField(null=True, verbose_name='HTML содержимое')

    class Meta:
        db_table = 'paid_content'
        verbose_name = 'Платный контент'

    def __str__(self):
        return f'{self.paid_content_id} - {self.content_name}'
