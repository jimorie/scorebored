from scorebored.overrides.aioli_rdbms.service import DatabaseModelService
from .database import StatsModel


class StatsService(DatabaseModelService):
    async def on_startup(self):
        """
        Register database model.
        """
        await self.set_db_model(StatsModel)

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
            side_stats = [result["side"]["stats"]]
            side_stats.extend([player["stats"] for player in result["side"]["players"]])
            for stats in side_stats:
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
