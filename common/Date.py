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
            date = time.mktime(time.strptime(dateStr,'%Y-%m-%d %H:%M:%S'))

        return date