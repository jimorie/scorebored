from aioli.controller.schemas import fields, Schema


class Stats(Schema):
    id = fields.Integer(primary_key=True)
    score_for = fields.Integer(default=0)
    score_against = fields.Integer(default=0)
    matches_played = fields.Integer(default=0)
    matches_won = fields.Integer(default=0)
    matches_lost = fields.Integer(default=0)

    class Meta:
        dump_only = ["id"]
