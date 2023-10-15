import datetime
import json

from models import db, base as DB
from common.Date import DateHelper
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


class Trend(db.Model):
    __tablename__ = "trend"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.Integer, ForeignKey('users.id'), index=True)
    content = db.Column(db.Text, default='')
    images = db.Column(db.Text, default='')
    date = db.Column(db.DateTime, default=datetime.datetime.now())
    status = db.Column(db.Integer, default=1)

    user = relationship('User')

    def __repr__(self):
        data = dict(id=self.id, userId=self.userId, content=self.content, images=self.images, date=str(self.date), status=self.status)
        return json.dumps(data)

    def getUserTrend(id):
        trend = Trend.query.filter_by(id=id).first()
        return trend

    def saveTrend(data, userId):
        currData = Trend(userId=userId, content=data.get('content'), images=data.get('savePath'),
                         date=DateHelper.date_string(), status=1)
        db.session.add(currData)
        db.session.flush()
        id = currData.id
        db.session.commit()
        trend = Trend.getUserTrend(id)
        return trend

    def getList(keyword, index, size):
        if keyword != '':
            filter_str = (Trend.content.like('%' + keyword + '%'))
        else:
            filter_str = None

        dt: dict = DB.getList(Trend, filter_str, index, size)

        list = dt.get('list')
        allNum = dt.get('allNum')

        newList = []
        for trend in list:
            newTrend = Trend.handleTrend(trend)
            newList.append(newTrend)

        return dict(list=newList, allNum=allNum)

    def handleTrend(trend):
        if trend.images != '':
            images = trend.images.split(';')
        else:
            images = []

        time = DateHelper.time_differ(trend.date)

        return dict(id=trend.id, userId=trend.userId, name=trend.user.username, icon=trend.user.avatar, time=time,
                    content=trend.content, images=images, commend=eval(str(trend.commend)),
                    comment=eval(str(trend.comment)), date=str(trend.date), status=trend.status)
