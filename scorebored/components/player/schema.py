from aioli.controller.schemas import fields, Schema


class Player(Schema):
    id = fields.Integer()
    name = fields.String()

    class Meta:
        dump_only = ["id"]


class PlayerId(Schema):
    player_id = fields.Integer()
