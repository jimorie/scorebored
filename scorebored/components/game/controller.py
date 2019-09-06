from aioli.controller import BaseHttpController, Method, schemas, route, takes, returns

from .schema import Game, GameId
from .service import GameService


class GameController(BaseHttpController):
    def __init__(self, pkg):
        super(GameController, self).__init__(pkg)
        self.game = GameService(pkg)

    async def on_request(self, request):
        self.log.debug(f"Request received: {request}")

    @route("/games", Method.GET, "List available games")
    @takes(query=schemas.HttpParams)
    @returns(Game, many=True)
    async def games_get(self, query):
        return await self.game.get_many(**query)

    @route("/games", Method.POST, "Define new game")
    @takes(body=Game)
    @returns(Game, status=201)
    async def games_add(self, body):
        return await self.game.create(body)

    @route("/games/{game_id}", Method.GET, "Get game details")
    @takes(path=GameId)
    @returns(Game)
    async def game_get(self, game_id):
        return await self.game.get_one(game_id)

    @route("/games/{game_id}", Method.PUT, "Update game")
    @takes(path=GameId, body=Game)
    @returns(Game)
    async def game_update(self, game_id, body):
        return await self.game.update(game_id, body)

    @route("/games/{game_id}", Method.DELETE, "Delete game")
    @takes(path=GameId)
    @returns(status=204)
    async def game_delete(self, game_id):
        return await self.game.delete(game_id)
