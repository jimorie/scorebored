from aioli_rdbms.model import Model, fields


class StatsModel(Model):
    __tablename__ = "stats"

    id = fields.Integer(primary_key=True)
    score_for = fields.Integer(default=0)
    score_against = fields.Integer(default=0)
    matches_played = fields.Integer(default=0)
    matches_won = fields.Integer(default=0)
    matches_lost = fields.Integer(default=0)
