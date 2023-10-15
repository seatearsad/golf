import os
import json
import common.Date as Date
import common.payment as Ada
from models import db
from models.member_order import Member_order
from models.orders import Orders
from models.user import User


class Adapay_callback:
    @staticmethod
    def init_data(request_data):
        print(request_data)
        current_path = os.path.dirname(os.path.abspath(__file__))
        ROOT_DIR = os.path.abspath(os.path.join(current_path, '..'))
        path = ROOT_DIR + '/callback'

        if not os.path.exists(path):
            os.makedirs(path)

        file_path = path + '/' + str(Date.DateHelper.date_number()) + '.txt'

        with open(file_path, "w") as fh:
            fh.write(str(request_data))

        adapay = Ada.Adapay()
        checkSign = adapay.checkSign(str(request_data.get('data')), str(request_data.get('sign')))
        print(checkSign[0])
        if checkSign[0]:
            data = json.loads(request_data.get('data'))
            order_no = data.get('order_no')
            order_arr = order_no.split('_')

            if order_arr[0] == 'member':
                orderClass = Member_order
            else:
                orderClass = Orders

            order = orderClass.getOrderByOrderNo(order_no)
            if order is None:
                return order
            else:
                if data.get('status') == 'succeeded':
                    order.pay_time = Date.DateHelper.date_string()
                    if order_arr[0] == 'member':
                        userId = order.userId
                        user = User.getUserById(userId)
                        user.level = order.level
                        order.status = 10
                    else:
                        order.status = 5
                else:
                    order.status = 3

                db.session.commit()

            return 'Success'
        else:
            return 'Sign Error'
