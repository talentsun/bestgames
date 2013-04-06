# coding: utf8

import logging, re
from router import Router
from portal.models import Game
from message_builder import MessageBuilder, BuildConfig
import logging, traceback, time, struct, socket
from service import search_pb2

logger = logging.getLogger("default")

default_sorry_wording = u'非常抱歉没有找到你要找的游戏，看来小每要加强学习了'

def __search_games(query):
    q = search_pb2.Query()
    q.query = query
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(struct.pack("!H", 1) + q.SerializeToString(), ("127.0.0.1", 8128))
    r = s.recv(4196)
    resp = search_pb2.Response()
    resp.ParseFromString(r)
    return resp

def _search_games(rule, info):
    resp = __search_games(info.text)

    if resp.result == 0:
        # results is sorted by gameRel not nameRel
        for g in resp.games:
            if g.nameRel >= 0.8:
                # pattern: search download url by game name
                return BuildConfig(MessageBuilder.TYPE_DOWNLOAD_URL, None, [Game.objects.get(pk = g.gameId)])

    return BuildConfig(MessageBuilder.TYPE_RAW_TEXT, None, default_sorry_wording)
        

def _find_tag_game(rule, info):
    pattern = u"(推荐|寻找)(.+)(的{0,1})游戏"
    m = re.match(pattern, info.text)
    if m:
        gameTags = m.group(2)
        logger.debug("game tags %s" % gameTags)
        resp = __search_games(gameTags)
        if resp.result == 0:
            res_games = []
            for g in resp.games:
                logger.debug("recom game %d weight %f" % (g.gameId, g.gameRel))
                try:
                    res_game = Game.objects.get(pk = g.gameId)
                except:
                    continue
                res_games.append(res_game)
            if len(res_games) > 0:
                return BuildConfig(MessageBuilder.TYPE_GAMES, None, res_games)

    return BuildConfig(MessageBuilder.TYPE_RAW_TEXT, None, default_sorry_wording)



def _find_similar_game(rule, info):
    pattern1 = u'(寻找|推荐)(和{0,1})(.+)(相似|类似|很像)的游戏'
    pattern2 = u'(寻找|推荐)(相似|类似|很像)(.+)的游戏'
    m = re.match(pattern1, info.text)
    gameName = None
    if m:
        gameName = m.group(3)
        logger.debug("pattern1 gameName %s" % gameName)
    else:
        m = re.match(pattern2, info.text)
        if m:
            gameName = m.group(3)
            logger.debug("pattern2 gameName %s" % gameName)
    if gameName != None:
        resp = __search_games(gameName)
        if resp.result == 0:
            max_name_rel = 0
            max_game_id = 0
            for g in resp.games:
                if g.nameRel >= max_name_rel:
                    max_name_rel = g.nameRel
                    max_game_id = g.gameId
            if max_name_rel > 0.8:
                #find game
                logger.debug("find game %d weight %f" % (max_game_id, max_name_rel))
                game = Game.objects.get(pk = max_game_id)
                similar_query = ""
                for t in game.tags.all():
                    similar_query += t.name + " "
                similar_query += game.category.name
                logger.debug("similar query %s" % similar_query)
                similar_resp = __search_games(similar_query)
                if similar_resp.result == 0:
                    res_games = []
                    for g in similar_resp.games:
                        if g.gameId != max_game_id:
                            logger.debug("recom game %d weight %f" % (g.gameId, g.gameRel))
                            try:
                                res_game = Game.objects.get(pk = g.gameId)
                            except:
                                continue
                            res_games.append(res_game)
                    if len(res_games) > 0:
                        return BuildConfig(MessageBuilder.TYPE_GAMES, None, res_games)

    return BuildConfig(MessageBuilder.TYPE_RAW_TEXT, None, default_sorry_wording)



    

Router.get_instance().set({
    'name': u'根据玩过的游戏找游戏',
    'pattern': u'((推荐|寻找)(和{0,1})(.+)(相似|类似|很像)的游戏)|((推荐|寻找)(相似|类似|很像)(.+)的游戏)',
    'handler': _find_similar_game
})


Router.get_instance().set({
    'name' : u'根据tag寻找游戏',
    'pattern': u'((推荐|寻找)(.+)(的{0,1})游戏)',
    'handler': _find_tag_game
})


Router.get_instance().set({
    'name' : u'根据游戏名获取游戏下载地址',
    'pattern': u'(下载(.+)((游戏)?))',
    'handler' : _search_games
    })
