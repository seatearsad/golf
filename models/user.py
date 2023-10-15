from models import db, base as DB
from common.Date import DateHelper
import random
import string
import datetime


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=True, default='')
    password = db.Column(db.String(64), default='e10adc3949ba59abbe56e057f20f883e')
    gender = db.Column(db.Integer, default=0)
    avatar = db.Column(db.String(150), default='')
    openid = db.Column(db.String(64))
    unionid = db.Column(db.String(64), default='')
    session_key = db.Column(db.String(64))
    type = db.Column(db.Integer, default=0)  # 0wx 1平台
    level = db.Column(db.Integer, default=0)  # 0未选择 1经销商 2会员
    status = db.Column(db.Integer, default=0)
    phone = db.Column(db.String(64), default='')
    balance = db.Column(db.DECIMAL(10, 2), default=0)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now())
    login_time = db.Column(db.Integer, nullable=True, default=0)
    parentId = db.Column(db.Integer, nullable=True, default=0)
    invite_code = db.Column(db.String(10), default='', index=True)

    def __repr__(self):
        return '<User %r>' % self.username

    @staticmethod
    def insertUserWxOne(openid, session_key, parentId, unionid=''):
        code = User.generateCode(6)
        currData = User(openid=openid, unionid=unionid, session_key=session_key, type=0, status=0, level=0,
                        login_time=DateHelper.date_number(), parentId=parentId, invite_code=code)
        db.session.add(currData)
        db.session.flush()
        userId = currData.id
        db.session.commit()

        return userId

    @staticmethod
    def getUserByOpenid(openid):
        user = User.query.filter_by(openid=openid).first()
        if not user is None and user.invite_code == '':
            code = User.generateCode(6)
            user.invite_code = code
            db.session.commit()
        return user

    @staticmethod
    def getUserByUnionid(unionid):
        user = User.query.filter_by(unionid=unionid).first()
        if not user is None and user.invite_code == '':
            code = User.generateCode(6)
            user.invite_code = code
            db.session.commit()
        return user

    @staticmethod
    def getUserById(userId):
        user = User.query.filter_by(id=userId).first()
        return user

    @staticmethod
    def updateWxInfo(data: dict, openid):
        user = User.getUserByOpenid(openid)
        user.username = data.get('nickName')
        user.gender = data.get('gender')
        user.avatar = data.get('avatarUrl')
        user.status = 1
        db.session.commit()

        return user

    @staticmethod
    def updateUserPhone(userId, phone):
        user = User.query.filter_by(id=userId).first()
        user.phone = phone
        db.session.commit()

    @staticmethod
    def getList(keyword, index, size):
        if keyword != '':
            filter_str = (User.name.like('%' + keyword + '%'))
        else:
            filter_str = None

        dt: dict = DB.getList(User, filter_str, index, size)

        list = dt.get('list')
        allNum = dt.get('allNum')

        newList = []
        for user in list:
            newUser = User.handleUser(user)
            newList.append(newUser)

        return dict(list=newList, allNum=allNum)

    @staticmethod
    def handleUser(user):
        return dict(id=user.id, username=user.username, type=user.type, level=user.level, avatar=user.avatar, phone=user.phone,
                    status=user.status, gender=user.gender, invite_code=user.invite_code ,
                    create_time=str(user.create_time), login_time=DateHelper.date_string(user.login_time))

    @staticmethod
    def getAllNumByStatus(status=1):
        filterStr = {User.status == status}
        allNum = DB.getAllNum(User, filterStr)
        return allNum

    @staticmethod
    def getChildrenByUserId(userId):
        filterStr = {User.parentId == userId}
        filterStr.add(User.status == 1)
        childrenNum = DB.getAllNum(User, filterStr)

        return childrenNum

    @staticmethod
    def getUsersByFriends(friendList):
        friends = User.query.filter(User.id.in_(friendList)).all()
        newList = []
        for user in friends:
            newUser = User.handleUser(user)
            newList.append(newUser)

        return newList

    @staticmethod
    def getFindUserByPhone(userId, phone, friends):
        userList = User.query.filter(User.phone == phone).all()

        newList = []
        for user in userList:
            newUser = User.handleUser(user)
            print(user.id)
            if user.id != int(userId):
                if user.id in friends:
                    newUser['isFriend'] = 1
                else:
                    newUser['isFriend'] = 0
                newList.append(newUser)

        return newList

    @staticmethod
    def getMemberListByUserId(userId):
        filterStr = {User.parentId == userId}
        filterStr.add(User.status == 1)

        allNum = DB.getAllNum(User, filterStr)
        allList = User.query.filter(*filterStr).all()

        inactive = []
        agent = []
        member = []

        for user in allList:
            if user.level == 0:
                inactive.append(User.handleUser(user))
            elif user.level == 1:
                agent.append(User.handleUser(user))
            else:
                member.append(User.handleUser(user))

        return dict(num=allNum, inactive=inactive, agent=agent, member=member)

    @staticmethod
    def generateCode(length):
        random_string = ''
        for i in range(length):
            random_string += random.choice(string.ascii_uppercase + string.digits)

        user = User.query.filter_by(invite_code=random_string).first()
        if not user is None:
            random_string = User.generateCode(length)
        return random_string
