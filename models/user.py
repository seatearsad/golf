from models import db, base as DB
from common.Date import DateHelper


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=True, default='')
    password = db.Column(db.String(64), default='e10adc3949ba59abbe56e057f20f883e')
    gender = db.Column(db.Integer, default=0)
    avatar = db.Column(db.String(150), default='')
    openid = db.Column(db.String(64))
    session_key = db.Column(db.String(64))
    type = db.Column(db.Integer, default=0) #0wx 1平台
    status = db.Column(db.Integer, default=0)
    phone = db.Column(db.String(64), default='')
    login_time = db.Column(db.Integer, nullable=True, default=0)
    parentId = db.Column(db.Integer, nullable=True, default=0)

    def __repr__(self):
        return '<User %r>' %self.username

    def insertUserWxOne(openid, session_key, parentId):
        currData = User(openid=openid, session_key=session_key, type=0, status=0,
                        login_time=DateHelper.date_number(), parentId=parentId)
        db.session.add(currData)
        db.session.flush()
        userId = currData.id
        db.session.commit()

        return userId

    def getUserByOpenid(openid):
        user = User.query.filter_by(openid=openid).first()
        return user

    def updateWxInfo(data: dict, openid):
        user = User.getUserByOpenid(openid)
        user.username = data.get('nickName')
        user.gender = data.get('gender')
        user.avatar = data.get('avatarUrl')
        user.status = 1
        db.session.commit()

        return user

    def getList(keyword, index, size):
        if keyword != '':
            filter_str = (User.name.like('%' + keyword + '%'))
        else:
            filter_str = None

        dt: dict = DB.getList(User, filter_str, index, size)

        list = dt.get('list')
        allNum = dt.get('allNum')

        newList = []
        for store in list:
            newUser = User.handleUser(store)
            newList.append(newUser)

        return dict(list=newList, allNum=allNum)

    def handleUser(user):
        return dict(id=user.id, username=user.username, type=user.type, avatar=user.avatar, phone=user.phone,
                    status=user.status, gender=user.gender, login_time=DateHelper.date_string(user.login_time))