from aioli.controller.schemas import fields, Schema

from scorebored.components.game.schema import GameLight


class Stats(Schema):
    game = fields.Nested(GameLight)
    score_for = fields.Integer(default=0)
    score_against = fields.Integer(default=0)
    matches_played = fields.Integer(default=0)
    matches_won = fields.Integer(default=0)
    matches_lost = fields.Integer(default=0)

    class Meta:
        dump_only = ["id"]
