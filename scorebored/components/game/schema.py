from aioli.controller.schemas import fields, Schema


class Game(Schema):
    id = fields.Integer()
    name = fields.String()
    side_size_min = fields.Integer(default=1)
    side_size_max = fields.Integer(default=2)
    side_count_min = fields.Integer(default=2)
    side_count_max = fields.Integer(default=2)

    class Meta:
        dump_only = ["id"]


class GameLight(Game):
    class Meta:
        dump_only = ["id"]
        exclude = ["side_size_min", "side_size_max", "side_count_min", "side_count_max"]


class GameId(Schema):
    game_id = fields.Integer()
