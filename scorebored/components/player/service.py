from .database import PlayerModel
from scorebored.components.stats import StatsService, StatsKeyService
from scorebored.overrides.aioli_rdbms.service import NamedDatabaseModelService


class PlayerService(NamedDatabaseModelService):
    stats: StatsService
    stats_key: StatsKeyService

    async def on_startup(self):
        """
        Register database model.
        """
        await self.set_db_model(PlayerModel)
        await self.set_db_name_field("name")
        self.stats = self.connect(StatsService)
        self.stats_key = self.connect(StatsKeyService)

    async def delete(self, pk):
        """
        Delete a Player entry.

        :param pk: Primary key of the Player to delete
        """

        async with self.db.manager.database.transaction():
            player = await self.db.get_one(pk=pk)
            await self.stats.delete_many(query=dict(stats_key=player.stats_key))
            await self.stats_key.delete(player.stats_key.pk)
            return await super().delete(pk)

    async def create(self, payload):
        """
        Create a new Player entry.

        :param payload: Player data
        :return: The created Player object
        """

        async with self.db.manager.database.transaction():
            stats_key = await self.stats_key.create(dict())
            payload["stats_key"] = stats_key.model
            return await super().create(payload)

    async def expand(self, player):
        player["stats"] = await self.stats.get_many(query=dict(stats_key=player["stats_key"]))
        return player
