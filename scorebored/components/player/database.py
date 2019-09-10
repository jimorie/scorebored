from aioli_rdbms.model import Model, fields
from scorebored.components.stats import StatsModel


class PlayerModel(Model):
    __tablename__ = "player"

    id = fields.Integer(primary_key=True)
    name = fields.String(max_length=64, unique=True)
    stats = fields.ForeignKey(StatsModel)
