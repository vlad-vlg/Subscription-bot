import logging
from urllib.parse import urljoin
from infrastructure.nowpayments.exceptions import APINotAvailable
from infrastructure.nowpayments.types import NowPayment, PaymentUpdate
import aiohttp


class NowPaymentsAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.nowpayments.io/v1/'
        self.session = aiohttp.ClientSession()
        self.headers = {
            'Content_Type': 'application/json',
            'Accept': 'application/json',
            'x-api-key': self.api_key
        }

    async def __request(self, method, *relative_path_parts, **kwargs):
        parts = '/'.join(relative_path_parts)
        url = urljoin(self.base_url, parts)
        async with getattr(self.session, method)(url,
                                                 headers=self.headers,
                                                 verify_ssl=False,
                                                 **kwargs) as response:
            try:
                result = await response.json()

            except Exception as e:
                logging.exception(e)
                logging.info(f'{await response.text()}')
                # print(await response.text())
            return result

    async def get(self, *relative_path_parts, **kwargs):
        data = kwargs.pop('data', {})
        params = list(data.items())
        return await self.__request('get', *relative_path_parts, params=params, **kwargs)

    async def post(self, *relative_path_parts, **kwargs):
        data = kwargs.pop('data', {})
        return await self.__request('post', *relative_path_parts, json=data, **kwargs)

    async def get_api_status(self):
        result = await self.get('status')
        if result.get('message') != 'OK':
            raise APINotAvailable()
        return True

    async def create_payment(self, price_amount: float,
                             price_currency: str,
                             pay_currency: str,
                             order_id: str = None,
                             order_description: str = None,
                             ipn_callback_url: str = None,
                             pay_amount: float = None,
                             purchase_id: str = None,
                             payout_address: str = None,
                             payout_currency: str = None,
                             payout_extra_id: str = None,
                             is_fixed_rate: bool = False):
        data = {
            'price_amount': price_amount,
            'price_currency': price_currency,
            'pay_currency': pay_currency
        }
        if order_id:
            data['order_id'] = order_id
        if order_description:
            data['order_description'] = order_description
        if ipn_callback_url:
            data['ipn_callback_url'] = ipn_callback_url
        if pay_amount:
            data['pay_amount'] = pay_amount
        if purchase_id:
            data['purchase_id'] = purchase_id
        if payout_address:
            data['payout_address'] = payout_address
        if payout_currency:
            data['payout_currency'] = payout_currency
        if payout_extra_id:
            data['payout_extra_id'] = payout_extra_id
        if is_fixed_rate:
            data['fixed_rate'] = is_fixed_rate
        result = await self.post('payment', data=data)
        print(result)
        return NowPayment(**result)

    async def get_payment_status(self, payment_id: int):
        result = await self.get('payment', str(payment_id))
        print(result)
        return PaymentUpdate(**result)

    async def get_available_currencies(self):
        result = await self.get('currencies')
        currencies = result.get('currencies')
        print(currencies)
        return currencies


if __name__ == '__main__':
    async def main():
        api = NowPaymentsAPI('')
        price = 30
        print(await api.get_api_status())
        payment = await api.create_payment(price_amount=price,
                                           price_currency='usd',
                                           pay_currency='btc',
                                           order_id='123',
                                           order_description='test')
        print(payment)

        payment_status = await api.get_payment_status(payment.payment_id)
        print(payment_status)
        await api.session.close()


    import asyncio

    asyncio.run(main())
