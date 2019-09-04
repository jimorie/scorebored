from ..database import MatchModel
from .base import DatabaseModelService
from .game import GameService
from .match_result import MatchResultService
from .side import SideService


class MatchService(DatabaseModelService):
    game: GameService
    side: SideService
    match_result: MatchResultService

    async def on_startup(self):
        """
        Integrate services.
        """
        await self.set_db_model(MatchModel)
        self.game = self.connect(GameService)
        self.side = self.connect(SideService)
        self.match_result = self.connect(MatchResultService)

    async def get_one(self, pk):
        """
        Return a single Match entry or raise an exception.

        :param pk: Primary key of the Match entry to get
        :return: Single Match entry
        """

        async with self.db.manager.database.transaction():
            match = await super().get_one(pk)
            return await self._expand(match)

    async def get_many(self, **query):
        """
        Return a list of zero or more Match entries.

        :param query: Query parameters
        :return: List of Match entries
        """

        async with self.db.manager.database.transaction():
            matches = await super().get_many(**query)
            return [await self._expand(match) for match in matches]

    async def delete(self, pk):
        """
        Delete a Match entry.

        :param pk: Primary key of the Match entry to delete
        """

        async with self.db.manager.database.transaction():
            match = await self.db.get_one(pk=pk)
            await self.match_result.delete_many(query=dict(match=match))
            return await super().delete(pk)

    async def update(self, pk, payload):
        """
        Update a Match entry.

        :param pk: Primary key of the Match entry to delete
        :param payload: MatchNew payload
        :return: The updated Match entry
        """

        async with self.db.manager.database.transaction():
            game = await self.game.get_or_create(dict(name=payload["game"]))
            match = await super().update(pk, dict(game=game))
            await self.match_result.delete_many(query=dict(match=match))
            await self._create_results(match, payload["results"])
            return await self.get_one(pk)

    async def create(self, payload):
        """
        Register new Match entry.

        :param payload: MatchNew payload
        :return: The created Match entry
        """

        async with self.db.manager.database.transaction():
            game = await self.game.get_or_create(dict(name=payload["game"]))
            match = await self.db.create(game=game)
            await self._create_results(match, payload["results"])
            self.log.info(f"New match: {match}")
            return await self.get_one(match.id)

    async def _expand(self, match):
        match_data = dict(match)
        match_results = await self.match_result.get_many(query=dict(match=match))
        match_data["results"] = [
            dict(score=result.score, side=await self.side.get_one(result.side.id))
            for result in match_results
        ]
        return match_data

    async def _create_results(self, match, results_payload):
        for result in results_payload:
            side = await self.side.get_or_create(result["players"])
            await self.match_result.create(
                dict(match=match, side=side, score=result["score"])
            )
