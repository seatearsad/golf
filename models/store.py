from models import db, base as DB
from sqlalchemy.orm import sessionmaker, relationship
from models.course import Course
from sqlalchemy import func
import json


class Store(db.Model):
    __tablename__ = "store"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), unique=True, index=True)
    city_id = db.Column(db.Integer, default=0)
    type = db.Column(db.Integer)
    address = db.Column(db.String(200), nullable=True, default='')
    lat = db.Column(db.DECIMAL(10, 6), default=0)
    lng = db.Column(db.DECIMAL(10, 6), default=0)
    phone = db.Column(db.String(100), nullable=True, default='')
    logo = db.Column(db.String(50), nullable=True, default='')
    intro = db.Column(db.Text, nullable=True, default='')
    score = db.Column(db.Float, nullable=True, default=0.00)
    designer = db.Column(db.String(50), nullable=True, default='')
    status = db.Column(db.Integer)
    images = db.Column(db.Text, nullable=True, default='')

    # course = relationship('Course', backref='course')

    def __repr__(self):
        return '<Store %r>' % self.name

    def insertData(data: dict):
        currData = Store(name=data.get('name'), city_id=data.get('city')[2], type=data.get('type'),
                         address=data.get('address'), lat=data.get('lat'),
                         lng=data.get('lng'), phone=data.get('phone'), intro=data.get('intro'),
                         status=data.get('status'), designer=data.get('designer'), images=';'.join(data.get('images')))
        db.session.add(currData)
        db.session.flush()
        store_id = currData.id
        db.session.commit()
        store = Store.getStoreById(store_id)
        return store

    def getStoreById(id):
        store: Store = Store.query.filter_by(id=id).first()
        return store

    def getList(keyword, index, size):
        if keyword != '':
            filter_str = (Store.name.like('%' + keyword + '%'))
        else:
            filter_str = None

        dt: dict = DB.getList(Store, filter_str, index, size)

        list = dt.get('list')
        allNum = dt.get('allNum')
        # if keyword != '':
        #     allNum = db.session.query(func.count(Store.id)).filter(Store.name.like('%'+keyword+'%')).scalar()
        #     list = Store.query.filter(Store.name.like('%'+keyword+'%')).limit(size).offset((int(index)-1)*int(size))
        # else:
        #     allNum = db.session.query(func.count(Store.id)).scalar()
        #     list = Store.query.limit(size).offset((int(index)-1)*int(size))

        newList = []
        for store in list:
            newStore = Store.handleStore(store)
            newList.append(newStore)

        return dict(list=newList, allNum=allNum)

    def handleStore(store):
        cityStr = str(store.city_id)
        city = [cityStr[:2], cityStr[:4], cityStr]
        if store.images != '':
            images = store.images.split(';')
        else:
            images = []
        return dict(id=store.id, name=store.name, type=store.type, city=city, address=store.address, lng=str(store.lng),
                    lat=str(store.lat), phone=store.phone, intro=store.intro, logo=store.logo, designer=store.designer,
                    status=store.status,images=images, course=eval(str(store.course)))

    def getListOrderByDistance(keyword, index, size, lat=0, lng=0, storeType=-1, city=''):
        filter_arr = {Store.status == 1}
        if keyword != '':
            filter_arr.add(Store.name.like('%' + keyword + '%'))

        if storeType != -1:
            filter_arr.add(Store.type == storeType)

        if city != '':
            filter_arr.add(Store.city_id.like(city + '%'))

        loc_latitude = lat
        loc_longitude = lng
        re = func.acos(
            func.sin(func.radians(loc_latitude)) * func.sin(func.radians(Store.lat)) + func.cos(
                func.radians(loc_latitude)) * func.cos(func.radians(Store.lat)) * func.cos(
                func.radians(Store.lng) - (func.radians(loc_longitude)))) * 6371

        newList = []
        for row, distance in db.session.query(Store, re.label('distance')).order_by(re.asc()).filter(*filter_arr).limit(size).offset(
                (int(index) - 1) * int(size)):
            store = Store.handleStore(row)
            store['distance'] = round(distance)
            newList.append(store)

        allNum = db.session.query(func.count(Store.id)).filter(*filter_arr).scalar()

        return dict(list=newList, allNum=allNum)
