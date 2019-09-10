from scorebored.overrides.aioli_rdbms.service import DatabaseModelService

from ..database import SidePlayerModel


class SidePlayerService(DatabaseModelService):
    async def on_startup(self):
        """
        Integrate services.
        """
        await self.set_db_model(SidePlayerModel)
