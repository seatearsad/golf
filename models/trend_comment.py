import datetime
import json

from models import db
from common.Date import DateHelper
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


class Trend_comment(db.Model):
    __tablename__ = "trend_comment"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.Integer, ForeignKey('users.id'), index=True)
    trendId = db.Column(db.Integer, ForeignKey('trend.id'), index=True)
    content = db.Column(db.Text, default='')
    replyId = db.Column(db.Integer, default=0)
    date = db.Column(db.DateTime, default=datetime.datetime.now())

    trend = relationship('Trend')
    user = relationship('User')

    comment = relationship('Trend', backref='comment', viewonly=True)

    def __repr__(self):
        data = dict(id=self.id, userId=self.userId, name=self.user.username, icon=self.user.avatar,
                    trendId=self.trendId, content=self.content,
                    replyId=self.replyId, date=str(self.date))
        return json.dumps(data)

    def saveComment(data, userId):
        currData = Trend_comment(userId=userId, content=data.get('content'), trendId=data.get('trendId'),
                                 replyId=data.get('replyId'), date=DateHelper.date_string())
        db.session.add(currData)
        db.session.flush()
        id = currData.id
        db.session.commit()
        trend = Trend_comment.getTrendComment(id)
        return trend

    def getTrendComment(id):
        trend = Trend_comment.query.filter_by(id=id).first()
        return trend
