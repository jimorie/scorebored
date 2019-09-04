from aioli.exceptions import NoMatchFound

from ..database import SideModel
from .base import NamedDatabaseModelService
from .player import PlayerService
from .side_player import SidePlayerService


class SideService(NamedDatabaseModelService):
    player: PlayerService
    side_player: SidePlayerService

    async def on_startup(self):
        """
        Integrate services.
        """
        await self.set_db_model(SideModel)
        await self.set_db_name_field("name")
        self.player = self.connect(PlayerService)
        self.side_player = self.connect(SidePlayerService)

    async def get_one(self, pk):
        """
        Return a single Side entry or raise an exception.

        :param pk: Primary key of the Side entry to get
        :return: Single Side entry
        """

        async with self.db.manager.database.transaction():
            side = await super().get_one(pk)
            return await self._expand(side)

    async def find_one(self, **query):
        """
        Return a single Side entry or raise an exception

        :param query: Query parameters
        :return: Single Side entry
        """

        async with self.db.manager.database.transaction():
            side = await super().find_one(**query)
            return await self._expand(side)

    async def get_many(self, **query):
        """
        Return a list of zero or more Side entries.

        :param query: Query parameters
        :return: List of Side entries
        """

        async with self.db.manager.database.transaction():
            sides = await super().get_many(**query)
            return [await self._expand(side) for side in sides]

    async def delete(self, pk):
        """
        Delete a Side entry.

        :param pk: Primary key of the Side entry to delete
        """

        async with self.db.manager.database.transaction():
            side = await self.db.get_one(pk=pk)
            await self.side_player.delete_many(query=dict(side=side))
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
            await self.side_player.delete_many(query=dict(side=side))
            for player in players:
                await self.side_player.create(dict(side=side, player=player))
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
                return await self.db.get_one(member_key=member_key)
            except NoMatchFound:
                return await self._create_side(players, member_key=member_key)

    async def _create_side(self, players, member_key=None):
        if member_key is None:
            member_key = self._get_member_key(players)
        name = self._get_default_name(players)
        side = await self.db.create(name=name, member_key=member_key)
        for player in players:
            await self.side_player.create(dict(side=side, player=player))
        self.log.info(f"New side: {side}")
        return side

    async def _expand(self, side):
        side_data = dict(side)
        side_players = await self.side_player.get_many(query=dict(side=side))
        side_data["players"] = [
            await self.player.get_one(side_player.player)
            for side_player in side_players
        ]
        return side_data

    def _get_member_key(self, players):
        return "+".join(str(pid) for pid in sorted(player.id for player in players))

    def _get_default_name(self, players):
        return " + ".join(sorted(player.name for player in players))
