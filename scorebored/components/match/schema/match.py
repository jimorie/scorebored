from aioli.controller.schemas import fields, Schema

from scorebored.components.game.schema import GameLight

from .result import Result, ResultNew


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
