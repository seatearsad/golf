from datetime import datetime
import time


class DateHelper:
    def date_string(date=0):
        if date == 0:
            dateNum = time.time()
        else:
            dateNum = date

        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(dateNum)) #dateNum.strftime('%Y-%m-%d %H:%M:%S')

    def date_number(dateStr=''):
        if dateStr == '':
            date = time.time()
        else:
            date = time.mktime(time.strptime(str(dateStr), '%Y-%m-%d %H:%M:%S'))

        return date

    def time_differ(dateStr):
        timeNum = DateHelper.date_number(dateStr)
        currNum = DateHelper.date_number()

        differ = currNum - timeNum
        differNum = round(differ/60)

        timeDesc = ''

        if differNum < 60:
            timeDesc = str(differNum) + '分钟前'
        elif 60 <= differNum < 1440:
            timeDesc = str(round(differNum/60)) + '小时前'
        elif differNum >= 1440:
            timeDesc = str(round(differNum / (24*60))) + '天前'

        return timeDesc
