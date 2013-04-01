#!/usr/local/bin/python2.7
#coding: utf-8

import sys, struct, os, logging, traceback, heapq
sys.path.append("..")

from django.core.management import setup_environ
from content_engine import settings
setup_environ(settings)
import leveldb, PySeg
from BuildIndex import DBItem
from search_pb2 import Query, Response
from portal.models import Category, Game, Category
from taggit.models import Tag
from taggit.models import Tag

workPath = os.path.dirname(os.path.abspath(__file__))
NameAddr = 1
CategoryAddr = 2
TagAddr = 3
DescAddr = 4

MaxRecomGame = 3

class HitList:
    def __init__(self):
        self.hitList = []

class SearchIndex:
    def __init__(self, dataPath, segPath):
        self.dataPath = dataPath
        self.segPath = segPath
        options = {
            'create_if_missing': True,
            'error_if_exists': False,
            'paranoid_checks': False,
            'block_cache_size': 100 * (1 << 20),
            'write_buffer_size': 2 * (1 << 20),
            'block_size': 4096,
            'max_open_files': 1000,
            'block_restart_interval': 16
        }
        self.db = leveldb.LevelDB(self.dataPath, **options)
        self.logger = logging.getLogger("search")


    def GetHitList(self, term):
        self.logger.debug("get hit list for %s" % term.decode("utf8"))
        startKey = struct.pack("!H%dsI" % len(term), len(term), term, 0)
        endKey = struct.pack("!H%dsI" % len(term), len(term), term, 0xFFFFFFFF)
        hitList = HitList()
        for k, v in self.db.RangeIter(key_from = startKey, key_to = endKey):
            item = DBItem("", 0, [])
            item.Decode(k, v)
            self.logger.debug("get gameId %d addrs %s" % (item.gameId, str(item.addrs)))
            hitList.hitList.append((item.gameId, item.addrs))
        return hitList


    def Search(self, query):
        termWeightBase = 0.5
        terms = PySeg.seg(query)
        hitListList = []
        for term in terms:
            if len(term[1]) > 0 and term[1][0] == 'n':
                hitList = self.GetHitList(term[0])
                hitListList.append(hitList)

        termWeight = []
        curAddr = []
        allNum = 0
        addrWeight = {NameAddr:0.2, CategoryAddr:0.3, TagAddr:0.4, DescAddr:0.1}
        for i in range(len(hitListList)):
            allNum += len(hitListList[i].hitList)
            termWeight.append(len(hitListList[i].hitList))
            curAddr.append(0)
        if allNum == 0:
            return []
        if len(hitListList) == 1:
            termWeight[i] = 1
        else:
            for i in range(len(hitListList)):
                termWeight[i] = termWeightBase / len(hitListList) + (1 - termWeightBase) * float(allNum - termWeight[i]) / allNum / (len(hitListList) - 1)

        self.logger.debug("weight %s" % str(termWeight))


        games = []
        while True:
            curMinGameId = 0xFFFFFFFF
            for i in range(len(hitListList)):
                if curAddr[i] < len(hitListList[i].hitList) and hitListList[i].hitList[curAddr[i]][0] < curMinGameId:
                    curMinGameId = hitListList[i].hitList[curAddr[i]][0]
            if curMinGameId == 0xFFFFFFFF:
                break
            self.logger.debug("deal with gameId %d" % curMinGameId)
            curWeight = 0
            for i in range(len(hitListList)):
                if curAddr[i] < len(hitListList[i].hitList) and hitListList[i].hitList[curAddr[i]][0] == curMinGameId:
                    for addr in hitListList[i].hitList[curAddr[i]][1]:
                        curWeight += termWeight[i] * addrWeight[addr]
                    self.logger.debug("hit term %d %f" % (i, curWeight))
                    curAddr[i] += 1
            if len(games) < MaxRecomGame:
                heapq.heappush(games, [curWeight, curMinGameId])
            else:
                heapq.heappushpop(games, [curWeight, curMinGameId])


        games.sort(key=lambda g: g[0], reverse=True)

        return games

    def RespGames(self, result, gameIds, address, s):
        resp = Response()
        resp.result = result
        resp.gameIds.extend(gameIds)
        s.sendto(resp.SerializeToString(), address)
        

    def InitSeg(self):
        PySeg.init(self.segPath)
        tags = Tag.objects.all()
        for t in tags:
            try:
                PySeg.addUserWord(t.name.encode("gbk"))
                self.logger.debug("add user word tag %s success" % t.name)
            except:
                self.logger.debug("add user word %s error" % t.name)

        cats = Category.objects.all()
        for c in cats:
            try:
                PySeg.addUserWord(c.name.encode('gbk'))
                self.logger.debug("add user word category %s" % c.name)
            except:
                self.logger.debug("add user word %s error" % c.name)
    def AddOneGame(self, gameId):
        try:
            game = Game.objects.get(pk = gameId)
        except:
            self.logger.error("not find game for %d", gameId)
            return
        tags = []
        for t in game.tags.all():
            tags.append(t.name)
        categorys = [game.category.name, ]
        terms = {}
        self.logger.debug("add one game for one %d %s %s %s %s" % (gameId, game.name, game.description, str(categorys), str(tags)))
        ts = PySeg.seg(game.name.encode('utf8'))
        terms[NameAddr] = []
        for t in ts:
            if len(t[1]) > 0 and t[1][0] == 'n':
                terms[NameAddr].append(t[0])
        ts = PySeg.seg(game.description.encode('utf8'))
        terms[DescAddr] = []
        for t in ts:
            if len(t[1]) > 0 and t[1][0] == 'n':
                terms[DescAddr].append(t[0])

        terms[CategoryAddr] = []
        for c in categorys:
            terms[CategoryAddr].append(c.encode("utf8"))
        terms[TagAddr] = []
        for t in tags:
            terms[TagAddr].append(t.encode('utf8'))
        term2Addrs = {}

        for k, v in terms.items():
            for term in v:
                self.logger.debug("%d %s" % (k, term.decode('utf8')))
                if term not in term2Addrs:
                    term2Addrs[term] = []

                if k not in term2Addrs[term]:
                    term2Addrs[term].append(k)


        for term, addrs in term2Addrs.items():
            self.logger.debug("term %s addrs %s" % (term.decode('utf8'), str(addrs)))
            item = DBItem(term, gameId, addrs)
            (k, v) = item.Encode()

            self.db.Put(k, v)


    def StartServer(self):
        import socket
        host = "127.0.0.1"
        port = 8128
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))

        while True:
            try:
                message, address = s.recvfrom(8192)
                self.logger.debug("len %d" % len(message))
                query = Query()
                cmd = struct.unpack("!H", message[0:2])[0]
                message = message[2:]
                self.logger.debug("cmd %d" % cmd)
                if cmd == 1:
                    try:
                        query.ParseFromString(message)
                    except:
                        self.logger.debug("parse from string error")
                        self.logger.debug(traceback.format_exc())
                        self.RespGames(1, [], address, s)
                        return
                    self.logger.debug("get content %s" % query.query)
                    games = self.Search(query.query.encode("utf8"))
                    gameIds = []
                    for game in games:
                        self.logger.debug("game weight %f id %d" % (game[0], game[1]))
                        gameIds.append(game[1])
                    self.RespGames(0, gameIds, address, s)
                elif cmd == 2:
                    gameId = struct.unpack("!I", message[0:4])[0]
                    self.AddOneGame(gameId)
                else:
                    self.logger.error("not find cmd %d" % cmd)
            except:
                self.logger.debug(traceback.format_exc())
                

if __name__ == "__main__":
    search = SearchIndex(workPath + "/../db/", workPath + "/../")
    search.InitSeg()
    search.StartServer()


