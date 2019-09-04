import datetime

from aioli_rdbms.model import Model, fields


class GameModel(Model):
    __tablename__ = "game"

    id = fields.Integer(primary_key=True)
    name = fields.String(max_length=64, unique=True)
    side_size_min = fields.Integer(default=1)
    side_size_max = fields.Integer(default=2)
    side_count_min = fields.Integer(default=2)
    side_count_max = fields.Integer(default=2)


class MatchModel(Model):
    __tablename__ = "match"

    id = fields.Integer(primary_key=True)
    game = fields.ForeignKey(GameModel)
    created_at = fields.DateTime(default=datetime.datetime.utcnow)
    updated_at = fields.DateTime(default=datetime.datetime.utcnow)


class SideModel(Model):
    __tablename__ = "side"

    id = fields.Integer(primary_key=True)
    name = fields.String(max_length=64)
    member_key = fields.String(unique=True, max_length=64)


class PlayerModel(Model):
    __tablename__ = "player"

    id = fields.Integer(primary_key=True)
    name = fields.String(max_length=64, unique=True)


class MatchResultModel(Model):
    __tablename__ = "match_result"

    id = fields.Integer(primary_key=True)
    match = fields.ForeignKey(MatchModel)
    side = fields.ForeignKey(SideModel)
    score = fields.Integer(default=0)


class SidePlayerModel(Model):
    __tablename__ = "side_player"

    id = fields.Integer(primary_key=True)
    side = fields.ForeignKey(SideModel)
    player = fields.ForeignKey(PlayerModel)
    # from sqlalchemy import PrimaryKeyConstraint
    # id = PrimaryKeyConstraint('side', 'player')
