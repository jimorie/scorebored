from ..database import SidePlayerModel
from .base import DatabaseModelService


class SidePlayerService(DatabaseModelService):
    async def on_startup(self):
        """
        Integrate services.
        """
        await self.set_db_model(SidePlayerModel)

    async def get_many(self, **query):
        # TODO: Joining related columns here causes duplicated rows. Report?
        query["join_related"] = False
        return await super().get_many(**query)

    async def delete_many(self, **query):
        # TODO: Joining related columns here causes duplicated rows. Report?
        query["join_related"] = False
        return await super().delete_many(**query)
