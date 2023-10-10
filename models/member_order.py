import datetime
import json
import random
import string

from models import db
from common.Date import DateHelper
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


class Member_order(db.Model):
    __tablename__ = "member_order"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    orderNo = db.Column(db.String(30), unique=True, index=True, nullable=True, default='')
    userId = db.Column(db.Integer, ForeignKey('users.id'), index=True)
    level = db.Column(db.Integer, default=0)
    price = db.Column(db.DECIMAL(10, 2), default=0)
    createTime = db.Column(db.DateTime, default=datetime.datetime.now())
    payTime = db.Column(db.DateTime, default=datetime.datetime.now())
    status = db.Column(db.Integer, default=0)

    user = relationship('User')

    def __repr__(self):
        data = dict(id=self.id, orderNo=self.orderNo, userId=self.userId, level=self.level,
                    price=self.price, createTime=self.createTime, payTime=self.payTime, status=self.status)
        return json.dumps(data)

    @staticmethod
    def insertData(data: dict):
        currTime = DateHelper.date_number()
        orderNo = Member_order.getOrderNo(currTime)

        currData = Member_order(userId=data.get('userId'), orderNo=orderNo, level=data.get('level'),
                                price=data.get('price'))
        db.session.add(currData)
        db.session.flush()
        orderId = currData.id
        db.session.commit()
        order = Member_order.getOrderById(orderId)
        return order

    @staticmethod
    def getOrderById(orderId):
        order: Member_order = Member_order.query.filter_by(id=orderId).first()
        return order

    @staticmethod
    def getOrderNo(timeNum):
        print(timeNum)
        num = int(timeNum * 1000)
        random_string = ''
        for i in range(2):
            random_string += random.choice(string.digits)
        orderNo = 'member_' + str(num) + random_string
        print(orderNo)
        return orderNo
