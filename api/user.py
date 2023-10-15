import json
import requests
from flask import request

from api.api import Api
from common.saveImg import save_img_file, save_qr_code, del_image_path
from common.Date import DateHelper
from models.config import Config
from models.footprint import FootPrint
from models.trend import Trend
from models.friends import Friends
from models.trend_comment import Trend_comment
from models.trend_commend import Trend_commend
from models.member_order import Member_order
from models.adapay_record import Adapay_record
from models.record import Record
from models.user import User, db
from common.payment import Adapay


class UserApi(Api):
    def handleRequest(self, data: dict):
        match self.action:
            case 'wx_login':
                currData = self.getWxOpenid(data)
                parentId = data.get('userId')
                platform = data.get('platform')
                print(currData)
                if not currData.get('errcode') is None:
                    return self.error('Invalid Code')
                else:
                    user = User.getUserByUnionid(currData.get('unionid'))
                    if user is None:
                        if platform == 'a':
                            userId = User.insertUserWxOne(currData.get('openid'), currData.get('session_key'), parentId,
                                                          currData.get('unionid'))
                            currData['userId'] = userId
                        else:
                            currData['userId'] = 0
                    else:
                        currData['userId'] = user.id

                        if platform == 'a':
                            user.openid = currData.get('openid')
                            user.session_key = currData.get('session_key')
                            user.unionid = currData.get('unionid')

                        if user.status != 0:
                            currData['nickName'] = user.username
                            currData['avatar'] = user.avatar
                            currData['phone'] = user.phone
                            currData['invite_code'] = user.invite_code
                            currData['level'] = user.level
                        else:
                            if str(parentId) != '0':
                                user.parentId = parentId

                        db.session.commit()

            case 'updateInfo':
                user = User.updateWxInfo(json.loads(data.get('data')), data.get('openid'))
                # token = self.getAccessToken(data)

                currData = dict(userId=user.id)
            case 'getQrcode':
                user = User.getUserByUnionid(data.get('unionid'))
                token = self.getAccessToken(data)
                qrcode = self.getQrcode(token, user.id, data.get('platform'))
                currData = dict(path=qrcode)
            case 'footprint':
                userId = data.get('userId')
                foot = FootPrint.getUserFoot(userId)
                reData = dict()
                if not foot is None:
                    reData = eval(str(foot))

                currData = reData
            case 'saveFoot':
                userId = data.get('userId')
                data = json.loads(data.get('data'))
                foot = FootPrint.getUserFoot(userId)
                if foot is None:
                    foot = FootPrint.addUserFoot(userId, data)

                currData = eval(str(foot))
            case 'sendTrend':
                savePath = save_img_file(request.files.get('file'), 'user', 'trend')
                currData = dict(imgPath=savePath)
            case 'delTrendImg':
                path = data.get('savePath')
                pathList = path.split(';')
                for imgPath in pathList:
                    if not imgPath is None:
                        del_image_path(imgPath)

                currData = None
            case 'saveTrend':
                userId = data.get('userId')
                saveData = json.loads(data.get('data'))
                trend = Trend.saveTrend(saveData, userId)
                currData = eval(str(trend))
            case 'getAllTrend':
                userId = data.get('userId')
                index = data.get('page')
                size = data.get('pageSize')
                friends = Friends.getFriendList(userId)

                currData = Trend.getList("", index, size)
                currData['friends'] = friends
            case 'followUser':
                userId = data.get('userId')
                followId = data.get('followId')
                Friends.insert_data(userId, followId)
                friends = Friends.getFriendList(userId)
                currData = friends
            case 'getFriends':
                userId = data.get('userId')
                friendList = Friends.getFriendList(userId)
                friends = User.getUsersByFriends(friendList)
                currData = friends
            case 'searchUserByPhone':
                userId = data.get('userId')
                phone = data.get('phone')
                friends = Friends.getFriendList(userId)
                currData = User.getFindUserByPhone(userId, phone, friends)
            case 'saveTrendComment':
                userId = data.get('userId')
                saveData = json.loads(data.get('data'))
                comment = Trend_comment.saveComment(saveData, userId)
                currData = eval(str(comment))
            case 'saveTrendCommend':
                userId = data.get('userId')
                saveData = json.loads(data.get('data'))
                commend = Trend_commend.getTrendComment(userId, saveData.get('trendId'))
                if commend is None:
                    commend = Trend_commend.saveCommend(saveData, userId)
                    currData = eval(str(commend))
                else:
                    return self.error('您已经赞过了')

            case 'saveRecord':
                userId = data.get('userId')
                saveData = json.loads(data.get('data'))
                record = Record.saveRecord(saveData, userId)
                currData = eval(str(record))
            case 'getRecord':
                userId = data.get('userId')
                recordList = Record.getUserRecord(userId)
                currData = eval(str(recordList))
            case 'getUserPhone':
                userId = data.get('userId')
                code = data.get('code')
                platform = data.get('platform')
                token = self.getAccessToken(data)
                phone = self.getUserPhone(token, code, userId, platform)
                currData = dict(phone=phone)
            case 'getConfigFee':
                dealer_fee = Config.getValueByName('dealer_fee')
                dealer_discount = Config.getValueByName('dealer_discount')
                dealer_base_fee = Config.getValueByName('dealer_base_fee')
                member_fee = Config.getValueByName('member_fee')
                currData = dict(dealer_fee=dealer_fee, dealer_discount=dealer_discount,
                                dealer_base_fee=dealer_base_fee, member_fee=member_fee)
            case 'createMemberOrder':
                userId = data.get('userId')
                level = int(data.get('level'))
                price = 0
                title = ''

                if level == 1:
                    price = Config.getValueByName('dealer_fee')
                    title = '经销商费用'
                elif level == 2:
                    price = Config.getValueByName('member_fee')
                    title = '会员费用'

                insertData = dict(userId=userId, level=level, price=price)

                order = Member_order.insertData(insertData)

                if order is None:
                    return self.error('订单创建失败')
                else:
                    adapay = Adapay()
                    user = User.getUserById(userId)
                    desc = user.username + title + ':' + userId
                    response = adapay.createOrder(order.orderNo, user.openid, order.price, title, desc)
                    if response.get('status') != "succeeded":
                        response['created_time'] = int(DateHelper.date_number())
                        order.status = -1
                    else:
                        order.status = 1

                    db.session.commit()
                    Adapay_record.insertData(response)

                currData = response
            case 'updateMemberOrder':
                userId = data.get('userId')
                order_no = data.get('order_no')
                status = data.get('status')
                order = Member_order.getOrderByOrderNo(order_no)
                if status == 'success':
                    order.status = 2
                else:
                    order.status = -2

                db.session.commit()
                currData = None
            case 'getUserData':
                userId = data.get('userId')
                memberNum = User.getChildrenByUserId(userId)
                user = User.getUserById(userId)

                currData = dict(member=memberNum, balance=str(user.balance))
            case 'getMemberList':
                userId = data.get('userId')
                currData = User.getMemberListByUserId(userId)
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

    def getQrcode(self, token, userId, platform):
        url = 'https://api.weixin.qq.com/wxa/getwxacodeunlimit?access_token=' + token
        params = {
            'scene': 'userId=' + str(userId),
            'page': 'pages/index/index',
            'check_path': False
        }
        response = requests.post(url, json=params)
        path = save_qr_code(response.content, userId, platform)
        return path

    @staticmethod
    def getUserPhone(token, code, userId, platform):
        url = 'https://api.weixin.qq.com/wxa/business/getuserphonenumber?access_token=' + token
        params = {
            "code": code
        }
        response = requests.post(url, json=params)
        print(response.json())
        phone_info = response.json().get('phone_info')
        phone = phone_info.get('phoneNumber')
        User.updateUserPhone(userId, phone)
        return phone


class UserAdmin(Api):
    def handleRequest(self, data: dict):
        match self.action:
            case 'getUserList':
                keyword = data.get('keyword')
                index = data.get('page')
                size = data.get('pageSize')
                currData = User.getList(keyword, index, size)
            case 'getAllTrend':
                index = data.get('page')
                size = data.get('pageSize')
                currData = Trend.getList("", index, size)
            case _:
                currData = None

        return self.success(currData)
