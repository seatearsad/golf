import adapay
from models.config import Config


class Adapay:
    def __init__(self):
        self.merchant_key = Config.getValueByName('adapay_merchant_key')
        self.app_id = Config.getValueByName('adapay_app_id')
        self.api_key = Config.getValueByName('adapay_api_key')
        self.mock_api_key = Config.getValueByName('adapay_mock_api_key')
        self.private_key = Config.getValueByName('adapay_private_key')

        config_info = {
            'api_key': self.api_key,
            'mock_api_key': self.mock_api_key,
            'private_key': self.private_key
        }

        adapay.mer_config = {
            'merchant_key': config_info  # merchant1为对应商户配置key 值，调用接口时需传入
        }

        self.adapay = adapay

    def createOrder(self, order_no, openid, price, title, desc):
        response = self.adapay.Payment.create(
            order_no=order_no,
            app_id=self.app_id,
            pay_channel='wx_lite',
            pay_amt='0.01',
            goods_title=title,
            goods_desc=desc,
            mer_key='merchant_key',
            device_info={'device_ip': '0.0.0.0'},
            expend={'open_id': openid},
            notify_url='http://58.87.70.236/api/adapay_callback'
        )

        print(response)

        return response
