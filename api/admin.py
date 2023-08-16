from models.admin import Admin, db
from common import md5
from api.api import Api
import string
import random
from common.Date import DateHelper
from sqlalchemy import func
import json


class AdminAdmin(Api):
    def init_data(self, data: dict):
        print("init_data", data)
        is_continue = super().init_data(data)
        if is_continue != 'OK':
            return is_continue
        else:
            match self.action:
                case 'login':
                    userName = data.get("name")
                    password = md5.md5(data.get('password'))
                    if userName == "" or password == "":
                        return self.error("请输入用户名和密码")
                    else:
                        currAdmin = self.checkAdmin(userName, password)
                        if currAdmin is None:
                            return self.error("用户名密码错误")
                case 'adminList':
                    keyword = data.get('keyword')
                    index = data.get('page')
                    size = data.get('pageSize')
                    currAdmin = Admin.getAdminList(keyword, index, size)
                    if currAdmin is None:
                        currAdmin = []
                case 'admin_set':
                    userData = data.get('data')
                    userData = json.loads(userData)
                    if userData.get('id') == 0:
                        userData = self.innerData(userData)
                        db.session.add(userData)
                    else:
                        currData: Admin = Admin.query.filter_by(id=userData.get('id')).first()
                        currData.name = userData.get('name')
                        print('admin_set', userData.get('password'))
                        if userData.get('password') != '' and not userData.get('password') is None:
                            currData.password = md5.md5(userData.get('password'))
                        currData.type = userData.get('type')
                        currData.status = userData.get('status')
                    db.session.commit()
                    currAdmin = []
                case _:
                    currAdmin = None

            return self.success(currAdmin)

    def checkAdmin(self, userName, password):
        currData: Admin = Admin.query.filter_by(name=userName, password=password).first()
        if currData is None:
            return None
        else:
            token = self.generateToken()
            currData.token = token
            expire = DateHelper.date_number()
            currData.expire = expire
            db.session.commit()
            data = Admin.handleAdmin(currData)
        return data

    def innerData(self, currData:dict):
        print("innerData", currData)
        return Admin(name=currData.get('name'), type=currData.get('type'), status=currData.get('status'), password=md5.md5(currData.get('password')))
    def generateToken(self):
        number_str = 5
        string_str = 8
        for x in range(number_str):
            str = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(string_str))

        return str