from aioli.controller import BaseHttpController, Method, schemas, route, takes, returns

from .schema import Player, PlayerId
from .service import PlayerService


class PlayerController(BaseHttpController):
    def __init__(self, pkg):
        super(PlayerController, self).__init__(pkg)
        self.player = PlayerService(pkg)

    async def on_request(self, request):
        self.log.debug(f"Request received: {request}")

    @route("/players", Method.GET, "List registered players")
    @takes(query=schemas.HttpParams)
    @returns(Player, many=True)
    async def players_get(self, query):
        return await self.player.get_many(**query)

    @route("/players", Method.POST, "Define new player")
    @takes(body=Player)
    @returns(Player, status=201)
    async def player_add(self, body):
        return await self.player.create(body)

    @route("/players/{player_id}", Method.GET, "Get player details")
    @takes(path=PlayerId)
    @returns(Player)
    async def player_get(self, player_id):
        return await self.player.get_one(player_id)

    @route("/players/{player_id}", Method.PUT, "Update player")
    @takes(path=PlayerId, body=Player)
    @returns(Player)
    async def player_update(self, player_id, body):
        return await self.player.update(player_id, body)

    @route("/players/{player_id}", Method.DELETE, "Delete player")
    @takes(path=PlayerId)
    @returns(status=204)
    async def player_delete(self, player_id):
        return await self.player.delete(player_id)
