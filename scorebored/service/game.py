from ..database import GameModel
from .base import NamedDatabaseModelService


class GameService(NamedDatabaseModelService):
    async def on_startup(self):
        """
        Register database model.
        """
        await self.set_db_model(GameModel)
        await self.set_db_name_field("name")
