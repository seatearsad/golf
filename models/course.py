import json

from models import db, base as DB
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Course(db.Model):
    __tablename__ = "course"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    storeId = db.Column(db.Integer, ForeignKey('store.id'), index=True)
    name = db.Column(db.String(100), nullable=True, default='')
    intro = db.Column(db.Text, nullable=True, default='')
    hole_count = db.Column(db.Integer, default=0)
    pars = db.Column(db.Integer, default=0)
    distance = db.Column(db.DECIMAL(10, 2), default=0)
    normal_price = db.Column(db.DECIMAL(10, 2), default=0)
    holiday_price = db.Column(db.DECIMAL(10, 2), default=0)
    open_time = db.Column(db.String(50), nullable=True, default='')
    close_time = db.Column(db.String(50), nullable=True, default='')
    images = db.Column(db.String(200), nullable=True, default='')
    status = db.Column(db.Integer, default=1)
    unit = db.Column(db.String(20), nullable=True, default='')
    unit_vol = db.Column(db.Integer, default=0)

    store = relationship('Store')

    course = relationship('Store', backref='course', viewonly=True)

    def __repr__(self):
        data = dict(id=self.id, storeId=self.storeId, name=self.name, intro=self.intro, hole_count=self.hole_count,
                    pars=self.pars, distance=str(self.distance), normal_price=str(self.normal_price),
                    holiday_price=str(self.holiday_price),open_time=self.open_time, close_time=self.close_time,
                    status=self.status, unit=self.unit, unit_vol=self.unit_vol)
        return json.dumps(data)

    def insertData(data: dict):
        currData = Course(name=data.get('name'), storeId=data.get('storeId'), intro=data.get('intro'),
                          hole_count=data.get('hole_count'), pars=data.get('pars'),
                          distance=data.get('distance'), normal_price=data.get('normal_price'),
                          holiday_price=data.get('holiday_price'),
                          open_time=data.get('open_time'), close_time=data.get('close_time'),
                          status=data.get('status'), unit=data.get('unit'), unit_vol=data.get('unit_vol'))
        db.session.add(currData)
        db.session.flush()
        course_id = currData.id
        db.session.commit()
        course = Course.getCourseById(course_id)
        return course

    def getCourseById(id):
        course: Course = Course.query.filter_by(id=id).first()
        return course
