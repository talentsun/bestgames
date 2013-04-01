from router import Router
from portal.models import Game
from message_builder import MessageBuilder, BuildConfig
import logging, traceback, time, struct, socket
from service import search_pb2
import socket

def _search_download_url_by_name(rule, info):
	q = search_pb2.Query()
    q.query = info.text
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(struct.pack("!H", 1) + q.SerializeToString(), ("127.0.0.1", 8128))
    r = s.recv(4196)
    response = search_pb2.Response()
    r.ParseFromString(response)
    
    games = []
    for id in r.gameIds:
        try:
            game = Game.objects.get(pk = id)
        except:
            continue
        games.append(game)
    return BuildConfig(MessageBuilder.TYPE_DOWNLOAD_URL, None, games))

Router.get_instance().set({
	'name' : '根据游戏名获取游戏下载地址',
	'handler' : _search_download_url_by_name
	})