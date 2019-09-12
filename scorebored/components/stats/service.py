from aioli.exceptions import NoMatchFound

from scorebored.overrides.aioli_rdbms.service import DatabaseModelService
from scorebored.components.game import GameService
from .database import StatsModel, StatsKeyModel



class StatsService(DatabaseModelService):
    game: GameService

    async def on_startup(self):
        """
        Register database model.
        """
        await self.set_db_model(StatsModel)
        self.game = self.connect(GameService)

    async def get_or_create(self, game, stats_key):
        """
        Get an existing set of stats for the given game and stats_key, otherwise
        create a new one.

        :param game: The game for the stats
        :param stats_key: The stats_key for the stats
        :return: The found or created Stats object
        """

        try:
            return await self.find_one(game=game, stats_key=stats_key)
        except NoMatchFound:
            return await self.create(dict(game=game, stats_key=stats_key))

    async def expand(self, stats):
        stats["game"] = await self.game.get_one(pk=stats["game"]["id"])
        return stats

    async def add_match_stats(self, match, remove=False):
        mult = -1 if remove else 1
        results = match["results"]
        total_score = sum(result["score"] for result in results)
        best_score = max(result["score"] for result in results)
        winning_side_id = None
        for result in results:
            if result["score"] == best_score:
                if winning_side_id:
                    # It's a draw!
                    winning_side_id = None
                    break
                winning_side_id = result["side"]["id"]
        for result in results:
            side_stats_keys = [result["side"]["stats_key"]]
            side_stats_keys.extend(
                [player["stats_key"] for player in result["side"]["players"]]
            )
            for stats_key in side_stats_keys:
                stats = await self.get_or_create(match["game"].model, stats_key)
                stats["game"] = stats["game"].model
                stats["score_for"] += mult * result["score"]
                stats["score_against"] += mult * (total_score - result["score"])
                stats["matches_played"] += mult
                if result["side"]["id"] == winning_side_id:
                    stats["matches_won"] += mult
                elif winning_side_id is not None:
                    stats["matches_lost"] += mult
                payload = dict(stats)
                stats_id = payload.pop("id")
                await self.update(stats_id, payload)

    async def remove_match_stats(self, match):
        return await self.add_match_stats(match, remove=True)


class StatsKeyService(DatabaseModelService):
    async def on_startup(self):
        """
        Register database model.
        """
        await self.set_db_model(StatsKeyModel)
