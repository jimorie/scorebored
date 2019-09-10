from aioli.controller import BaseHttpController, Method, schemas, route, takes, returns

from .schema import Match, MatchId, MatchNew
from .service import MatchService, MatchResultService


class MatchController(BaseHttpController):
    def __init__(self, pkg):
        super(MatchController, self).__init__(pkg)
        self.match = MatchService(pkg)
        self.match_result = MatchResultService(pkg)

    async def on_request(self, request):
        self.log.debug(f"Request received: {request}")

    @route("/matches", Method.GET, "List reported matches")
    @takes(query=schemas.HttpParams)
    @returns(Match, many=True)
    async def matches_get(self, query):
        return await self.match.get_many(**query)

    @route("/matches", Method.POST, "Report new match results")
    @takes(body=MatchNew)
    @returns(Match, status=201)
    async def matches_add(self, body):
        return await self.match.create(body)

    @route("/matches/{match_id}", Method.GET, "Get match details")
    @takes(path=MatchId)
    @returns(Match)
    async def match_get(self, match_id):
        return await self.match.get_one(match_id)

    @route("/matches/{match_id}", Method.PUT, "Update match")
    @takes(path=MatchId, body=MatchNew)
    @returns(Match)
    async def match_update(self, match_id, body):
        return await self.match.update(match_id, body)

    @route("/matches/{match_id}", Method.DELETE, "Delete match")
    @takes(path=MatchId)
    @returns(status=204)
    async def match_delete(self, match_id):
        return await self.match.delete(match_id)
