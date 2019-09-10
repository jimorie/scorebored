from aioli.controller.schemas import fields, Schema

from scorebored.components.player.schema import Player


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
