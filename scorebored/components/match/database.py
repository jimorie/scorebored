import datetime

from aioli_rdbms.model import Model, fields

from scorebored.components.game.database import GameModel
from scorebored.components.side.database import SideModel


class MatchModel(Model):
    __tablename__ = "match"

    id = fields.Integer(primary_key=True)
    game = fields.ForeignKey(GameModel)
    created_at = fields.DateTime(default=datetime.datetime.utcnow)
    updated_at = fields.DateTime(default=datetime.datetime.utcnow)


class MatchResultModel(Model):
    __tablename__ = "match_result"

    id = fields.Integer(primary_key=True)
    match = fields.ForeignKey(MatchModel)
    side = fields.ForeignKey(SideModel)
    score = fields.Integer(default=0)
