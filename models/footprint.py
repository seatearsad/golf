from models import db, base as DB
from models.store import Store
import json
from sqlalchemy import ForeignKey


class FootPrint(db.Model):
    __tablename__ = "footprint"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.Integer, ForeignKey('users.id'), index=True)
    cities = db.Column(db.Text, default='')
    stores = db.Column(db.Text, default='')

    def __repr__(self):
        data = dict(id=self.id, userId=self.userId, cities=self.cities, stores=self.stores)
        return json.dumps(data)

    @staticmethod
    def getUserFoot(userId):
        foot = FootPrint.query.filter_by(userId=userId).first()
        if not foot is None:
            storeList = Store.handleStoreNameById(foot.stores.split(';'))
            foot.stores = storeList
            foot.cities = foot.cities.split(';')
        return foot

    @staticmethod
    def addUserFoot(userId, data):
        currData = FootPrint(userId=userId, cities=data.get('city'), stores=data.get('store'))
        db.session.add(currData)
        db.session.flush()
        id = currData.id
        db.session.commit()
        foot = FootPrint.getUserFoot(userId)
        return foot
