import datetime
import random
import string

from sqlalchemy import func
from models import db, base as DB
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from models.store import Store
import json
from common.Date import DateHelper


class Orders(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    orderNo = db.Column(db.String(30), unique=True, index=True, nullable=True, default='')
    userId = db.Column(db.Integer, ForeignKey('users.id'), index=True)
    storeId = db.Column(db.Integer, ForeignKey('store.id'), index=True)
    courseId = db.Column(db.Integer, ForeignKey('course.id'), index=True)
    reservation_date = db.Column(db.Date, nullable=True, default='')
    reservation_time = db.Column(db.Time, nullable=True, default='')
    member = db.Column(db.Integer, default=0)
    car = db.Column(db.Integer, default=0)
    caddie = db.Column(db.Integer, default=0)
    coach = db.Column(db.Integer, default=0)
    price = db.Column(db.DECIMAL(10, 2), default=0)
    create_time = db.Column(db.DateTime)
    pay_time = db.Column(db.DateTime, default=datetime.datetime.now())
    status = db.Column(db.Integer, default=0)

    store = relationship('Store')
    user = relationship('User')
    course = relationship('Course')

    def __repr__(self):
        data = dict(id=self.id, orderNo=self.orderNo, userId=self.userId, storeId=self.storeId,
                    storeName=self.store.name, courseId=self.courseId,
                    reservation_date=str(self.reservation_date), reservation_time=str(self.reservation_time),
                    member=self.member, car=self.car, caddie=self.caddie, coach=self.coach,
                    price=str(self.price), create_time=str(self.create_time), pay_time=str(self.pay_time),
                    status=self.status)
        return json.dumps(data)

    @staticmethod
    def insertData(data: dict):
        currTime = DateHelper.date_string()
        orderNo = Orders.getOrderNo(currTime)

        currData = Orders(userId=data.get('userId'), orderNo=orderNo, storeId=data.get('storeId'),
                          courseId=data.get('courseId'),
                          reservation_date=data.get('date'), reservation_time=data.get('time'),
                          member=data.get('member'), car=data.get('car'), caddie=data.get('caddie'),
                          coach=data.get('coach'), price=data.get('price'), create_time=currTime,
                          pay_time=currTime, status=data.get('status'))
        db.session.add(currData)
        db.session.flush()
        orderId = currData.id
        db.session.commit()
        order = Orders.getOrderById(orderId)
        return order

    @staticmethod
    def getOrderById(orderId):
        order: Orders = Orders.query.filter_by(id=orderId).first()
        return order

    @staticmethod
    def getOrderByOrderNo(orderNo):
        order: Orders = Orders.query.filter_by(orderNo=orderNo).first()
        return order

    @staticmethod
    def getList(id, index, size):
        if id != '' and id != '0' and id != 0:
            filter_str = (Orders.id == id)
        else:
            filter_str = None

        dt: dict = DB.getList(Orders, filter_str, index, size)

        list = dt.get('list')
        allNum = dt.get('allNum')

        newList = []
        for order in list:
            newOrder = Orders.handleOrder(order)
            newList.append(newOrder)

        return dict(list=newList, allNum=allNum)

    @staticmethod
    def getOrderByUser(userId, status, index, size, storeType):
        filter_arr = {Orders.userId == userId}
        if int(status) != 0:
            filter_arr.add(Orders.status == status)
        if int(storeType) != -1:
            filter_arr.add(Store.type == storeType)

        allNum = db.session.query(func.count(Orders.id)).join(Store, Orders.storeId == Store.id).filter(*filter_arr).scalar()
        list = db.session.query(Orders).order_by(Orders.id.desc()).join(Store, Orders.storeId == Store.id).filter(*filter_arr).limit(size).offset((int(index) - 1) * int(size))

        newList = []
        for order in list:
            newOrder = Orders.handleOrder(order)
            newList.append(newOrder)

        return dict(list=newList, allNum=allNum)

    @staticmethod
    def handleOrder(order):
        return dict(id=order.id, orderNo=order.orderNo,
                    storeId=order.storeId, storeName=order.store.name, storeType=order.store.type,
                    storeLogo=order.store.logo,
                    userId=order.userId, userName=order.user.username,
                    courseId=order.courseId, courseName=order.course.name,
                    courseUnit=order.course.unit, courseUnitVol=order.course.unit_vol,
                    reservation_date=str(order.reservation_date), reservation_time=str(order.reservation_time),
                    member=order.member, car=order.car, caddie=order.caddie,
                    coach=order.coach, price=str(order.price), create_time=str(order.create_time),
                    pay_time=str(order.pay_time), status=order.status)

    @staticmethod
    def getAllNumByStatus(status=1):
        if status == -1:
            filterStr = {1 == 1}
        else:
            filterStr = {Orders.status == status}

        allNum = DB.getAllNum(Orders, filterStr)
        return allNum

    @staticmethod
    def getOrderByNo(orderNo):
        order: Orders = Orders.query.filter_by(orderNo=orderNo).first()
        return order

    @staticmethod
    def getOrderNo(currTime):
        random_string = ''
        for i in range(8):
            random_string += random.choice(string.digits)

        orderNo = currTime.replace('-', '').replace(':', '').replace(' ', '')[2:] + random_string

        order = Orders.getOrderByNo(orderNo)
        if not order is None:
            orderNo = Orders.getOrderNo(currTime)

        return orderNo
