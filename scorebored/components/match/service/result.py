from scorebored.overrides.aioli_rdbms.service import DatabaseModelService

from ..database import MatchResultModel
from scorebored.components.side import SideService


class MatchResultService(DatabaseModelService):
    side: SideService

    async def on_startup(self):
        """
        Integrate services.
        """
        await self.set_db_model(MatchResultModel)
        self.side = self.connect(SideService)

    async def get_many(self, **query):
        # TODO: Joining related columns here causes duplicated rows. Report?
        query["join_related"] = False
        return await super().get_many(**query)

    async def delete_many(self, **query):
        # TODO: Joining related columns here causes duplicated rows. Report?
        query["join_related"] = False
        return await super().delete_many(**query)
