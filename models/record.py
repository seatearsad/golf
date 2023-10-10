import datetime
import json

from models import db
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from common.Date import DateHelper


class Record(db.Model):
    __tablename__ = "record"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.Integer, ForeignKey('users.id'), index=True)
    cityId = db.Column(db.Integer)
    storeId = db.Column(db.Integer, ForeignKey('store.id'), index=True)
    stem = db.Column(db.Integer)
    date = db.Column(db.Date, default='')

    user = relationship('User')
    store = relationship('Store')

    def __repr__(self):
        data = dict(id=self.id, userId=self.userId, cityId=self.cityId, storeId=self.storeId,
                    stem=self.stem, date=str(self.date), storeName=self.store.name)
        return json.dumps(data)

    def saveRecord(data, userId):
        currData = Record(userId=userId, cityId=data.get('cityId'), storeId=data.get('storeId'),
                          stem=data.get('stemNum'), date=data.get('date'))
        db.session.add(currData)
        db.session.flush()
        id = currData.id
        db.session.commit()
        record = Record.getRecord(id)
        return record

    def getRecord(id):
        record = Record.query.filter_by(id=id).first()
        return record

    def getUserRecord(userId):
        recordList = Record.query.order_by(Record.stem.asc()).filter_by(userId=userId).all()
        return recordList