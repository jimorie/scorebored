from aioli.controller import BaseHttpController, Method, schemas, route, takes, returns

from .schema import (
    Game,
    GameId,
    Match,
    MatchId,
    MatchNew,
    Player,
    PlayerId,
    Side,
    SideId,
    SideNew,
)
from .service import (
    GameService,
    MatchService,
    SideService,
    PlayerService,
    MatchResultService,
    SidePlayerService,
)


class HttpController(BaseHttpController):
    def __init__(self, pkg):
        super(HttpController, self).__init__(pkg)
        self.game = GameService(pkg)
        self.match = MatchService(pkg)
        self.side = SideService(pkg)
        self.player = PlayerService(pkg)
        self.match_result = MatchResultService(pkg)
        self.side_player = SidePlayerService(pkg)

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
