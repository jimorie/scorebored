from scorebored.overrides.aioli_rdbms.service import NamedDatabaseModelService

from .database import PlayerModel


class PlayerService(NamedDatabaseModelService):
    async def on_startup(self):
        """
        Register database model.
        """
        await self.set_db_model(PlayerModel)
        await self.set_db_name_field("name")
