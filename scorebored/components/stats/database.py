from aioli_rdbms.model import Model, fields
from scorebored.components.game import GameModel


class StatsKeyModel(Model):
    __tablename__ = "stats_key"

    id = fields.Integer(primary_key=True)


class StatsModel(Model):
    __tablename__ = "stats"

    id = fields.Integer(primary_key=True)
    stats_key = fields.ForeignKey(StatsKeyModel)
    game = fields.ForeignKey(GameModel)
    score_for = fields.Integer(default=0)
    score_against = fields.Integer(default=0)
    matches_played = fields.Integer(default=0)
    matches_won = fields.Integer(default=0)
    matches_lost = fields.Integer(default=0)
