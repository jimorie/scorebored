from aioli_rdbms.model import Model, fields

from scorebored.components.player import PlayerModel
from scorebored.components.stats import StatsKeyModel


class SideModel(Model):
    __tablename__ = "side"

    id = fields.Integer(primary_key=True)
    name = fields.String(max_length=64)
    member_key = fields.String(unique=True, max_length=64)
    stats_key = fields.ForeignKey(StatsKeyModel)


class SidePlayerModel(Model):
    __tablename__ = "side_player"

    id = fields.Integer(primary_key=True)
    side = fields.ForeignKey(SideModel)
    player = fields.ForeignKey(PlayerModel)
