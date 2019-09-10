from aioli.exceptions import NoMatchFound

from scorebored.overrides.aioli_rdbms.service import NamedDatabaseModelService
from scorebored.components.player import PlayerService
from scorebored.components.stats import StatsService

from ..database import SideModel

from .sideplayer import SidePlayerService


class SideService(NamedDatabaseModelService):
    player: PlayerService
    side_player: SidePlayerService
    stats: StatsService

    async def on_startup(self):
        """
        Integrate services.
        """
        await self.set_db_model(SideModel)
        await self.set_db_name_field("name")
        self.player = self.connect(PlayerService)
        self.side_player = self.connect(SidePlayerService)
        self.stats = self.connect(StatsService)

    async def delete(self, pk):
        """
        Delete a Side entry.

        :param pk: Primary key of the Side entry to delete
        """

        async with self.db.manager.database.transaction():
            side = await self.db.get_one(pk=pk)
            await self.side_player.delete_many(query=dict(side=side))
            await self.stats.delete(side.stats.model.id)
            return await super().delete(pk)

    async def update(self, pk, payload):
        """
        Update a Side entry.

        :param pk: Primary key of the Side entry to update
        :param payload: SideNew payload
        :return: The updated Side entry
        """

        async with self.db.manager.database.transaction():
            players = [
                await self.player.get_or_create(dict(name=name))
                for name in payload["players"]
            ]
            name = payload.get("name") or self._get_default_name(players)
            member_key = self._get_member_key(players)
            side = await super().update(pk, dict(name=name, member_key=member_key))
            await self.side_player.delete_many(query=dict(side=side.model))
            for player in players:
                await self.side_player.create(
                    dict(side=side.model, player=player.model)
                )
            return await self.get_one(pk)

    async def create(self, payload):
        """
        Register a new Side entry.

        :param payload: SideNew payload
        :return: The created Side entry
        """

        async with self.db.manager.database.transaction():
            players = [
                await self.player.get_or_create(dict(name=name))
                for name in payload["players"]
            ]
            return await self._create_side(players)

    async def get_or_create(self, names):
        """
        Get Side by players if it exists or create it

        :param names: Names of the players
        :return: The Side entry found or created
        """

        async with self.db.manager.database.transaction():
            players = [
                await self.player.get_or_create(dict(name=name)) for name in names
            ]
            member_key = self._get_member_key(players)
            try:
                return await self.find_one(member_key=member_key)
            except NoMatchFound:
                return await self._create_side(players, member_key=member_key)

    async def _create_side(self, players, member_key=None):
        if member_key is None:
            member_key = self._get_member_key(players)
        name = self._get_default_name(players)
        stats = await self.stats.create(dict())
        side = await self.db.create(name=name, member_key=member_key, stats=stats.model)
        for player in players:
            await self.side_player.create(dict(side=side, player=player.model))
        self.log.info(f"New side: {side}")
        return await self.get_one(side.id)

    async def expand(self, side):
        side_players = await self.side_player.get_many(query=dict(side=side.model))
        side["players"] = [
            await self.player.get_one(side_player["player"]["id"])
            for side_player in side_players
        ]
        side["stats"] = await self.stats.get_one(side["stats"].id)
        return side

    def _get_member_key(self, players):
        return "+".join(str(pid) for pid in sorted(player["id"] for player in players))

    def _get_default_name(self, players):
        return " + ".join(sorted(player["name"] for player in players))
