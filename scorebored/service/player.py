from ..database import PlayerModel
from .base import NamedDatabaseModelService


class PlayerService(NamedDatabaseModelService):
    async def on_startup(self):
        """
        Register database model.
        """
        await self.set_db_model(PlayerModel)
        await self.set_db_name_field("name")
