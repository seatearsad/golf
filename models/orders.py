import datetime

from models import db, base as DB
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
import json
from common.Date import DateHelper


class Orders(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    orderNo = db.Column(db.String(20), unique=True, index=True, nullable=True, default='')
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
        data = dict(id=self.id, orderNo=self.orderNo, userId=self.userId, storeId=self.storeId, courseId=self.courseId,
                    reservation_date=str(self.reservation_date), reservation_time=str(self.reservation_time),
                    member=self.member, car= self.car, caddie=self.caddie, coach=self.coach,
                    price=str(self.price), create_time=str(self.create_time), pay_time=str(self.pay_time),
                    status=self.status)
        return json.dumps(data)

    def insertData(data: dict):
        currData = Orders(userId=data.get('userId'), storeId=data.get('storeId'), courseId=data.get('courseId'),
                          reservation_date=data.get('date'), reservation_time=data.get('time'),
                          member=data.get('member'), car=data.get('car'), caddie=data.get('caddie'),
                          coach=data.get('coach'), price=data.get('price'), create_time=DateHelper.date_string(),
                          pay_time=DateHelper.date_string(), status=data.get('status'))
        db.session.add(currData)
        db.session.flush()
        orderId = currData.id
        db.session.commit()
        order = Orders.getOrderById(orderId)
        return order

    def getOrderById(orderId):
        order: Orders = Orders.query.filter_by(id=orderId).first()
        return order

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
            newOrder = Orders.handleStore(order)
            newList.append(newOrder)

        return dict(list=newList, allNum=allNum)

    def getOrderByUser(userId, index, size):
        filter_str = (Orders.userId == userId)

        dt: dict = DB.getList(Orders, filter_str, index, size)

        list = dt.get('list')
        allNum = dt.get('allNum')

        newList = []
        for order in list:
            newOrder = Orders.handleStore(order)
            newList.append(newOrder)

        return dict(list=newList, allNum=allNum)
    def handleStore(order):
        return dict(id=order.id, orderNo=order.orderNo,
                    storeId=order.storeId, storeName=order.store.name, storeType=order.store.type,
                    userId=order.userId, userName=order.user.username,
                    courseId=order.courseId, courseName=order.course.name,
                    courseUnit=order.course.unit, courseUnitVol=order.course.unit_vol,
                    reservation_date=str(order.reservation_date), reservation_time=str(order.reservation_time),
                    member=order.member, car=order.car, caddie=order.caddie,
                    coach=order.coach, price=str(order.price), create_time=str(order.create_time),
                    pay_time=str(order.pay_time), status=order.status)
