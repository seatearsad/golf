from models.user import User, db
from models.config import Config
from api.api import Api
import requests
import json
from common.saveImg import save_qr_code


class UserApi(Api):
    def init_data(self, data: dict):
        print("init_data", data)
        is_continue = super().init_data(data)
        if is_continue != 'OK':
            return is_continue
        else:
            match self.action:
                case 'wx_login':
                    currData = self.getWxOpenid(data)
                    parentId = data.get('userId')
                    if not currData.get('errcode') is None:
                        return self.error('Invalid Code')
                    else:
                        user = User.getUserByOpenid(currData.get('openid'))
                        if user is None:
                            userId = User.insertUserWxOne(currData.get('openid'), currData.get('session_key'), parentId)
                            currData['userId'] = userId
                        else:
                            currData['userId'] = user.id
                            if user.status != 0:
                                currData['nickName'] = user.username
                                currData['avatar'] = user.avatar
                            else:
                                if str(parentId) != '0':
                                    user.parentId = parentId
                                    db.session.commit()

                case 'updateInfo':
                    user = User.updateWxInfo(json.loads(data.get('data')), data.get('openid'))
                    currData = dict(userId=user.id)
                case 'getQrcode':
                    user = User.getUserByOpenid(data.get('openid'))
                    token = self.getAccessToken(data)
                    qrcode = self.getQrcode(token, user.id)
                    currData = dict(path=qrcode)
                case _:
                    currData = None

            return self.success(currData)

    def getWxOpenid(self, data: dict):
        code = data.get('code')
        platform = data.get('platform')
        appId = Config.getValueByName('app_id_' + platform)
        secretId = Config.getValueByName('secret_id_' + platform)

        url = 'https://api.weixin.qq.com/sns/jscode2session?appid=' + appId + '&secret=' + secretId + '&js_code=' + code + '&grant_type=authorization_code'

        req_result = requests.get(url)

        return req_result.json()

    def getAccessToken(self, data):
        openId = data.get('openid')
        platform = data.get('platform')
        appId = Config.getValueByName('app_id_' + platform)
        secretId = Config.getValueByName('secret_id_' + platform)

        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + appId + '&secret=' + secretId

        req_result = requests.get(url)

        print(req_result.json())

        return req_result.json().get('access_token')

    def getQrcode(self, token, userId):
        url = 'https://api.weixin.qq.com/wxa/getwxacodeunlimit?access_token=' + token
        params = {
            'scene': 'userId=' + str(userId),
            'page': 'pages/index/index',
            'check_path': False
        }
        response = requests.post(url, json=params)
        path = save_qr_code(response.content, userId)
        return path


class UserAdmin(Api):
    def init_data(self, data: dict):
        print("init_data", data)
        is_continue = super().init_data(data)
        if is_continue != 'OK':
            return is_continue
        else:
            match self.action:
                case 'getUserList':
                    keyword = data.get('keyword')
                    index = data.get('page')
                    size = data.get('pageSize')
                    currData = User.getList(keyword, index, size)
                case _:
                    currData = None

            return self.success(currData)
