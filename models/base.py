from models import db
from sqlalchemy import func


def search_all(table_class):
    data_list = table_class.query.all()
    return data_list


def add_one(table_class, *args):
    print(table_class)
    data = table_class(username=args[0], password=args[1])
    db.session.add(data)
    db.session.commit()


def getList(currClass, filter_str, index, size, classItem=None):
    if classItem is None:
        classItem = currClass.id

    if isinstance(filter_str, set):
        allNum = db.session.query(func.count(classItem)).filter(*filter_str).scalar()
        currList = currClass.query.order_by(classItem.desc()).filter(*filter_str).limit(size).offset(
            (int(index) - 1) * int(size))
    elif not filter_str is None:
        allNum = db.session.query(func.count(classItem)).filter(filter_str).scalar()
        currList = currClass.query.order_by(classItem.desc()).filter(filter_str).limit(size).offset(
            (int(index) - 1) * int(size))
    else:
        allNum = db.session.query(func.count(classItem)).scalar()
        currList = currClass.query.order_by(classItem.desc()).limit(size).offset((int(index) - 1) * int(size))

    return dict(list=currList, allNum=allNum)


def getAllNum(currClass, filter_str):
    allNum = db.session.query(func.count(currClass.id)).filter(*filter_str).scalar()

    return allNum
