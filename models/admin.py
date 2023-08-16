from models import db, base as DB
from common.Date import DateHelper

class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(64))
    type = db.Column(db.Integer)
    status = db.Column(db.Integer)
    token = db.Column(db.String(100), nullable=True, default='')
    expire = db.Column(db.Integer, nullable=True, default=0)

    def __repr__(self):
        return '<Admin %r>' %self.name

    def getAdminList(keyword, index, size):
        if keyword != '':
            filter_str = (Admin.name.like('%' + keyword + '%'))
        else:
            filter_str = None

        dt: dict = DB.getList(Admin, filter_str, index, size)

        list = dt.get('list')
        allNum = dt.get('allNum')

        newList = []
        for user in list:
            newUser = Admin.handleAdmin(user)
            newList.append(newUser)

        return dict(list=newList, allNum=allNum)

    def handleAdmin(currData):
        return dict(id=currData.id, name=currData.name, type=currData.type, status=currData.status, token=currData.token, expire=DateHelper.date_string(currData.expire))


