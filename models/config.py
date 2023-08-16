from models import db


class Config(db.Model):
    __tablename__ = "config"
    name = db.Column(db.String(50), primary_key=True, index=True)
    value = db.Column(db.String(200), default='')
    info = db.Column(db.String(200), default='')
    type = db.Column(db.Integer, default=0)
    status = db.Column(db.Integer, default=1)

    def __repr__(self):
        return '<Config %r>' % self.name

    def getValueByName(name: str):
        data = Config.query.filter_by(name=name).first()

        return data.value
