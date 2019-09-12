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
        StatsKeyService,
        StatsService,
    ],
    auto_meta=True,
)
