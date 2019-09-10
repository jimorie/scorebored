from aioli.controller.schemas import fields, Schema
from scorebored.components.stats.schema import Stats


class Player(Schema):
    id = fields.Integer()
    name = fields.String()
    stats = fields.Nested(Stats)

    class Meta:
        dump_only = ["id"]


class PlayerLight(Player):
    class Meta:
        dump_only = ["id"]
        exclude = ["stats"]


class PlayerId(Schema):
    player_id = fields.Integer()
