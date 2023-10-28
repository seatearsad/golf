import json
import datetime

from models import db, base as DB
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from common.Date import DateHelper


class Game_score(db.Model):
    __tablename__ = "game_score"
    game_id = db.Column(db.Integer, ForeignKey('game.id'), primary_key=True, index=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), primary_key=True, index=True)
    score = db.Column(db.String(250), default='')
    save_user = db.Column(db.Integer, default=0)
    update_time = db.Column(db.DateTime, default=datetime.datetime.now())

    game = relationship('Game')
    user = relationship('User')
    userList = relationship('Game', backref='userList', viewonly=True)

    def __repr__(self):
        data = dict(game_id=self.game_id, create_id=self.game.create_id, user_id=self.user_id, score=self.score,
                    hole_count=self.game.hole_count, pars=self.game.pars, username=self.user.username,
                    userAvatar=self.user.avatar)
        return json.dumps(data)

    @staticmethod
    def insert_data(gameId, addUser: list):
        for userId in addUser:
            currData = Game_score(game_id=gameId, user_id=userId)
            db.session.add(currData)

        db.session.commit()

        scores = Game_score.getGameScoreByGameId(gameId)

        return scores

    @staticmethod
    def getGameScoreByGameId(gameId):
        scores = Game_score.query.filter(Game_score.game_id == gameId).all()
        return scores

    @staticmethod
    def getScoreByUseGameId(userId, gameId):
        score = Game_score.query.filter_by(user_id=userId, game_id=gameId).first()
        return score

    @staticmethod
    def saveGameScore(userId, gameId, saveData):
        for uId in saveData:
            score: Game_score = Game_score.getScoreByUseGameId(uId, gameId)
            score.score = str(json.dumps(saveData[uId]))
            score.save_user = userId
            score.update_time = DateHelper.date_string()

        db.session.commit()
