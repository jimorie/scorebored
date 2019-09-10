from scorebored.overrides.aioli_rdbms.service import DatabaseModelService
from scorebored.components.game import GameService
from scorebored.components.side import SideService

from ..database import MatchModel

from .result import MatchResultService


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
            match = await super().update(pk, dict(game=game.model))
            await self.match_result.delete_many(query=dict(match=match.model))
            await self._create_results(match.model, payload["results"])
            return await self.get_one(pk)

    async def create(self, payload):
        """
        Register new Match entry.

        :param payload: MatchNew payload
        :return: The created Match entry
        """

        async with self.db.manager.database.transaction():
            game = await self.game.get_or_create(dict(name=payload["game"]))
            match = await self.db.create(game=game.model)
            await self._create_results(match, payload["results"])
            self.log.info(f"New match: {match}")
            return await self.get_one(match.id)

    async def expand(self, match):
        match_results = await self.match_result.get_many(query=dict(match=match.model))
        match["results"] = [
            dict(score=result["score"], side=await self.side.get_one(result["side"]["id"]))
            for result in match_results
        ]
        return match

    async def _create_results(self, match, results_payload):
        for result in results_payload:
            side = await self.side.get_or_create(result["players"])
            await self.match_result.create(
                dict(match=match, side=side.model, score=result["score"])
            )
