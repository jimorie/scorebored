from aioli import Package

from .service import MatchService
from .controller import HttpController
from .config import ConfigSchema


export = Package(
    controllers=[HttpController],
    services=[MatchService],
    config=ConfigSchema,
    auto_meta=True,
)
