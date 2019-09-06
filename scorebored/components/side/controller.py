from aioli.controller import BaseHttpController, Method, schemas, route, takes, returns

from .schema import Side, SideId, SideNew
from .service import SideService


class SideController(BaseHttpController):
    def __init__(self, pkg):
        super(SideController, self).__init__(pkg)
        self.side = SideService(pkg)

    @route("/sides", Method.GET, "List registered sides")
    @takes(query=schemas.HttpParams)
    @returns(Side, many=True)
    async def sides_get(self, query):
        return await self.side.get_many(**query)

    @route("/sides", Method.POST, "Define new side")
    @takes(body=SideNew)
    @returns(Side, status=201)
    async def side_add(self, body):
        return await self.side.get_or_create(body["players"])

    @route("/sides/{side_id}", Method.GET, "Get side details")
    @takes(path=SideId)
    @returns(Side)
    async def side_get(self, side_id):
        return await self.side.get_one(side_id)

    @route("/sides/{side_id}", Method.PUT, "Update side")
    @takes(path=SideId, body=SideNew)
    @returns(Side)
    async def side_update(self, side_id, body):
        return await self.side.update(side_id, body)

    @route("/sides/{side_id}", Method.DELETE, "Delete side")
    @takes(path=SideId)
    @returns(status=204)
    async def side_delete(self, side_id):
        return await self.side.delete(side_id)
