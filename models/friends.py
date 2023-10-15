import datetime
import json

from models import db
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


class Friends(db.Model):
    __tablename__ = "friends"
    masterId = db.Column(db.Integer, primary_key=True, index=True)
    slaveId = db.Column(db.Integer, primary_key=True, index=True)
    date = db.Column(db.DateTime, default=datetime.datetime.now())

    def __repr__(self):
        data = dict(masterId=self.masterId, slaveId=self.slaveId, date=str(self.date))
        return json.dumps(data)

    @staticmethod
    def getFriendList(masterId):
        friends = Friends.query.filter_by(masterId=masterId).all()

        fList = []
        for item in friends:
            fList.append(item.slaveId)

        return fList

    @staticmethod
    def insert_data(masterId, slaveId):
        currData = Friends(masterId=masterId, slaveId=slaveId)
        db.session.add(currData)
        db.session.flush()
        db.session.commit()

        return currData
