from aioli import Package

from .components import *

export = Package(
    controllers=[SideController, PlayerController, MatchController, GameController],
    services=[
        SideService,
        SidePlayerService,
        PlayerService,
        MatchService,
        MatchResultService,
        GameService,
    ],
    auto_meta=True,
)
