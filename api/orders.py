from models.orders import Orders
from models.user import User
from models.adapay_record import Adapay_record
from models import db
from api.api import Api
from common.payment import Adapay
from common.Date import DateHelper
import json


class OrdersApi(Api):
    def handleRequest(self, data: dict):
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
                storeType = data.get('type')
                currData = Orders.getOrderByUser(userId, status, index, size, storeType)
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
                print(order)
                title = order.user.username + '预约：' + order.store.name
                desc = '预约时间：' + str(order.reservation_date) + ' ' + str(order.reservation_time)
                adapay = Adapay()
                response = adapay.createOrder(order.orderNo, user.openid, order.price, title, desc)
                if response.get('status') != "succeeded":
                    response['created_time'] = int(DateHelper.date_number())
                    order.status = -1
                else:
                    order.status = 1

                db.session.commit()
                Adapay_record.insertData(response)
                currData = response
            case 'updateMemberOrder':
                userId = data.get('userId')
                order_no = data.get('order_no')
                status = data.get('status')
                order = Orders.getOrderByNo(order_no)
                if status == 'success':
                    order.status = 2
                else:
                    order.status = -2

                db.session.commit()
                currData = None
            case _:
                currData = None

        return self.success(currData)


class OrdersAdmin(Api):
    def handleRequest(self, data: dict):
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

