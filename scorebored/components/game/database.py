from aioli_rdbms.model import Model, fields


class GameModel(Model):
    __tablename__ = "game"

    id = fields.Integer(primary_key=True)
    name = fields.String(max_length=64, unique=True)
    side_size_min = fields.Integer(default=1)
    side_size_max = fields.Integer(default=2)
    side_count_min = fields.Integer(default=2)
    side_count_max = fields.Integer(default=2)
