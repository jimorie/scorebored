from .database import PlayerModel
from scorebored.components.stats import StatsService
from scorebored.overrides.aioli_rdbms.service import NamedDatabaseModelService


class PlayerService(NamedDatabaseModelService):
    stats: StatsService

    async def on_startup(self):
        """
        Register database model.
        """
        await self.set_db_model(PlayerModel)
        await self.set_db_name_field("name")
        self.stats = self.connect(StatsService)

    async def delete(self, pk):
        """
        Delete a Player entry.

        :param pk: Primary key of the Player to delete
        """

        async with self.db.manager.database.transaction():
            player = await self.get_one(pk)
            self.stats.delete(player.stats.model.id)
            return await super().delete(pk)

    async def create(self, payload):
        """
        Create a new Player entry.

        :param payload: Player data
        :return: The created Player object
        """

        async with self.db.manager.database.transaction():
            stats = await self.stats.create(dict())
            payload["stats"] = stats.model
            return await super().create(payload)

    async def expand(self, player):
        player["stats"] = await self.stats.get_one(player["stats"])
        return player
