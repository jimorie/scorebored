from aioli import Package

from .components import *

export = Package(
    controllers=[GameController, MatchController, PlayerController, SideController],
    services=[
        GameService,
        MatchResultService,
        MatchService,
        PlayerService,
        SidePlayerService,
        SideService,
    ],
    auto_meta=True,
)
