# coding: utf8
from router import Router
from portal.models import Game
from message_builder import MessageBuilder, BuildConfig
import logging, traceback, time, struct, socket
from service import search_pb2

def _search_games(rule, info):
    q = search_pb2.Query()
    q.query = info.text
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(struct.pack("!H", 1) + q.SerializeToString(), ("127.0.0.1", 8128))
    r = s.recv(4196)
    resp = search_pb2.Response()
    resp.ParseFromString(r)

    if resp.result == 0:
        # results is sorted by gameRel not nameRel
        for g in resp.games:
            if g.nameRel >= 0.8:
                # pattern: search download url by game name
                return BuildConfig(MessageBuilder.TYPE_DOWNLOAD_URL, None, [Game.objects.get(pk = g.gameId)])

        games = []
        for related_game in resp.games:
            if related_game.gameRel >= 0.6:
                try:
                    game = Game.objects.get(pk = related_game.gameId)
                except:
                    continue
                games.append(game)
        if len(games) > 0:
            # pattern: recommend games by tags or category
            return BuildConfig(MessageBuilder.TYPE_GAMES, None, games)

Router.get_instance().set({
    'name' : '根据游戏名获取游戏下载地址',
    'handler' : _search_games
    })
