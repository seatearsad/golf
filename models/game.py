import json
import datetime

from sqlalchemy import func
from models import db, base as DB
from common.Date import DateHelper
from models.game_score import Game_score


class Game(db.Model):
    __tablename__ = "game"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_id = db.Column(db.Integer, default=0)
    store_id = db.Column(db.Integer, default=0)
    hole_count = db.Column(db.Integer, default=0)
    pars = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now())
    status = db.Column(db.Integer, default=0)
    end_time = db.Column(db.DateTime, default=datetime.datetime.now())

    def __repr__(self):
        data = dict(id=self.id, create_id=self.create_id, store_id=self.store_id, hole_count=self.hole_count,
                    pars=self.pars, create_time=str(self.create_time), status=self.status, end_time=str(self.end_time),
                    userList=eval(str(self.userList)))
        return json.dumps(data)

    @staticmethod
    def insert_data(data, userId):
        currData = Game(create_id=userId, store_id=data.get('store_id'), hole_count=data.get('hole_count'),
                        pars=data.get('pars'), status=1)
        db.session.add(currData)
        db.session.flush()
        db.session.commit()
        return currData

    @staticmethod
    def getGameById(gameId):
        game = Game.query.filter(Game.id == gameId).first()
        return game

    @staticmethod
    def endGame(gameId):
        game = Game.getGameById(gameId)
        game.status = 10
        game.end_time = DateHelper.date_string()

        db.session.commit()

    @staticmethod
    def getGameByUser(userId):
        filterArr = {Game_score.user_id == userId}
        filterArr.add(Game.status < 10)
        games = Game_score.query.join(Game, Game.id == Game_score.game_id).filter(*filterArr).all()

        return games

    @staticmethod
    def getGameListByUser(userId, index, size):
        filter_arr = {Game_score.user_id == userId}
        filter_arr.add(Game.status == 10)

        allNum = db.session.query(func.count(Game.id)).join(Game_score, Game_score.game_id == Game.id).filter(
            *filter_arr).scalar()
        list = db.session.query(Game).order_by(Game.id.desc()).join(Game_score, Game_score.game_id == Game.id).filter(
            *filter_arr).limit(size).offset((int(index) - 1) * int(size))

        newList = []
        for game in list:
            newGame = eval(str(game))
            newList.append(newGame)

        return dict(list=newList, allNum=allNum)
