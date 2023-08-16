from models.orders import Orders
from api.api import Api
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
                    currData = Orders.getOrderByUser(userId, index, size)
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