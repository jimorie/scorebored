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
