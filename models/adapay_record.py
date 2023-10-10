from models import db
from common.Date import DateHelper
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


class Adapay_record(db.Model):
    __tablename__ = "adapay_record"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    adapay_id = db.Column(db.String(100), default='')
    object = db.Column(db.String(50), default='')
    order_no = db.Column(db.String(30), default='')
    party_order_id = db.Column(db.String(30), default='')
    pay_amt = db.Column(db.DECIMAL(10, 2), default=0)
    pay_channel = db.Column(db.String(20), default='')
    prod_mode = db.Column(db.String(10), default='')
    query_url = db.Column(db.String(100), default='')
    expend = db.Column(db.Text, default='')
    status = db.Column(db.String(10), default='')
    error_code = db.Column(db.String(50), default='')
    error_msg = db.Column(db.String(50), default='')
    error_type = db.Column(db.String(50), default='')
    invalid_param = db.Column(db.String(50), default='')
    created_time = db.Column(db.Integer, nullable=True, default=0)

    def __repr__(self):
        return '<Admin %r>' % self.id

    @staticmethod
    def insertData(data: dict):
        currData = Adapay_record(adapay_id=data.get('id'), object=data.get('object'),
                                 order_no=data.get('order_no'), party_order_id=data.get('party_order_id'),
                                 pay_amt=data.get('pay_amt'), pay_channel=data.get('pay_channel'),
                                 prod_mode=data.get('prod_mode'), query_url=data.get('query_url'),
                                 expend=str(data.get('expend')), status=data.get('status'),
                                 error_code=data.get('error_code'), error_msg=data.get('error_msg'),
                                 error_type=data.get('error_type'), invalid_param=data.get('invalid_param'),
                                 created_time=data.get('created_time'))
        db.session.add(currData)
        db.session.flush()
        id = currData.id
        db.session.commit()

        return currData
