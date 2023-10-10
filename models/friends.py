import datetime
import json

from models import db
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


class Friends(db.Model):
    __tablename__ = "friends"
    masterId = db.Column(db.Integer, ForeignKey('users.id'), primary_key=True, index=True)
    slaveId = db.Column(db.Integer, ForeignKey('users.id'), primary_key=True, index=True)
    date = db.Column(db.DateTime, default=datetime.datetime.now())

    master = relationship('User')
    slave = relationship('User')

    def __repr__(self):
        data = dict(masterId=self.masterId, master_name=self.master.username, master_icon=self.master.avatar,
                    slaveId=self.slaveId, slave_name=self.slave.username, slave_icon=self.slave.avatar,
                    date=str(self.date))
        return json.dumps(data)
