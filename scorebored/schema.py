import datetime

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


class Player(Schema):
    id = fields.Integer()
    name = fields.String()

    class Meta:
        dump_only = ["id"]


class PlayerId(Schema):
    player_id = fields.Integer()


class Side(Schema):
    id = fields.Integer()
    name = fields.String()
    players = fields.List(fields.Nested(Player))

    class Meta:
        dump_only = ["id"]


class SideLight(Side):
    class Meta:
        dump_only = ["id"]
        exclude = ["players"]


class SideNew(Schema):
    players = fields.List(fields.String())
    name = fields.String(optional=True)


class SideId(Schema):
    side_id = fields.Integer()


class Result(Schema):
    side = fields.Nested(SideLight)
    score = fields.Integer(default=0)


class ResultNew(Schema):
    players = fields.List(fields.String())
    score = fields.Integer(default=0)


class Match(Schema):
    id = fields.Integer()
    game = fields.Nested(GameLight)
    results = fields.List(fields.Nested(Result))
    created_at = fields.String()
    updated_at = fields.String()

    class Meta:
        dump_only = ["id", "created_at", "updated_at"]


class MatchNew(Schema):
    game = fields.String()
    results = fields.List(fields.Nested(ResultNew))


class MatchId(Schema):
    match_id = fields.Integer()
