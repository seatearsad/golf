import datetime
import json

from models import db
from common.Date import DateHelper
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


class Trend_commend(db.Model):
    __tablename__ = "trend_commend"
    userId = db.Column(db.Integer, ForeignKey('users.id'), primary_key=True, index=True)
    trendId = db.Column(db.Integer, ForeignKey('trend.id'), primary_key=True, index=True)
    date = db.Column(db.DateTime, default=datetime.datetime.now())

    trend = relationship('Trend')
    user = relationship('User')

    commend = relationship('Trend', backref='commend', viewonly=True)

    def __repr__(self):
        data = dict(userId=self.userId, name=self.user.username, icon=self.user.avatar,
                    trendId=self.trendId, date=str(self.date))
        return json.dumps(data)

    def saveCommend(data, userId):
        currData = Trend_commend(userId=userId, trendId=data.get('trendId'), date=DateHelper.date_string())
        db.session.add(currData)
        db.session.flush()
        db.session.commit()
        trend = Trend_commend.getTrendComment(userId, data.get('trendId'))
        return trend

    def getTrendComment(userId, trendId):
        trend = Trend_commend.query.filter_by(userId=userId, trendId=trendId).first()
        return trend
