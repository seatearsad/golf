from models.orders import Orders
from models.user import User
from api.api import Api
from common.payment import Adapay
import json

class OrdersApi(Api):
    def init_data(self, data: dict):
        print("init_data", data)
        is_continue = super().init_data(data)
        if is_continue != 'OK':
            return is_continue
        else:
            match self.action:
                case 'saveOrder':
                    orderData = data.get('data')
                    orderData: dict = json.loads(orderData)

                    order = Orders.insertData(orderData)
                    currData = eval(str(order))
                case 'userOrders':
                    userId = data.get('userId')
                    index = data.get('page')
                    size = data.get('pageSize')
                    status = data.get('status')
                    currData = Orders.getOrderByUser(userId, status, index, size)
                case 'getOrderById':
                    userId = data.get('userId')
                    orderId = data.get('orderId')
                    order = Orders.getOrderById(orderId)
                    currData = eval(str(order))
                case 'createPay':
                    userId = data.get('userId')
                    orderId = data.get('orderId')
                    order = Orders.getOrderById(orderId)
                    user = User.getUserById(userId)
                    adapay = Adapay()
                    adapay.createOrder(order.orderNo, user.openid)
                    currData = None
                case _:
                    currData = None

            print(currData)

        return self.success(currData)


class OrdersAdmin(Api):
    def init_data(self, data: dict):
        print("init_data", data)
        is_continue = super().init_data(data)
        if is_continue != 'OK':
            return is_continue
        else:
            match self.action:
                case 'getOrderList':
                    id = data.get('id')
                    index = data.get('page')
                    size = data.get('pageSize')
                    currData = Orders.getList(id, index, size)
                case _:
                    currData = None

            print(currData)

        return self.success(currData)