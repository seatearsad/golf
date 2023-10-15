import datetime
import json
from models import db


class Income_record(db.Model):
    __tablename__ = "income_record"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.Integer, index=True)
    type = db.Column(db.Integer, default=1)
    amount = db.Column(db.DECIMAL(10, 2), default=0)
    orderNo = db.Column(db.String(30), index=True, default='')
    order_type = db.Column(db.Integer, default=0)
    desc = db.Column(db.String(100), default='')
    create_time = db.Column(db.DateTime, default=datetime.datetime.now())
    status = db.Column(db.Integer, default=0)

    def __repr__(self):
        data = dict(id=self.id, orderNo=self.orderNo, userId=self.userId, type=self.type,
                    amount=str(self.amount), order_type=self.order_type, desc=self.desc,
                    create_time=str(self.create_time), status=self.status)
        return json.dumps(data)
