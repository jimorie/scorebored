from aioli.controller.schemas import fields, Schema

from scorebored.components.side.schema import SideLight


class Result(Schema):
    side = fields.Nested(SideLight)
    score = fields.Integer(default=0)


class ResultNew(Schema):
    players = fields.List(fields.String())
    score = fields.Integer(default=0)
