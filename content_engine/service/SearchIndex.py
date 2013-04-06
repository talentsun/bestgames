#!/usr/local/bin/python2.7
#coding: utf-8

import sys, struct, os, logging, traceback, heapq
sys.path.append("..")

from django.core.management import setup_environ
from content_engine import settings
setup_environ(settings)
import leveldb
from SegUtil import SegUtil
from BuildIndex import DBItem, Index
from search_pb2 import Query, Response, QueryTerm, RelatedGame
from portal.models import Category, Game, Category
from taggit.models import Tag
from taggit.models import Tag

from Utils import *

workPath = os.path.dirname(os.path.abspath(__file__))
NameAddr = 1
CategoryAddr = 2
TagAddr = 3
DescAddr = 4

MaxRecomGame = 3

class HitList:
    def __init__(self):
        """
        every item is (term, addrs, nameWeight)
        """
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
        self.logger.debug("get hit list for %s" % term)
        startItem = DBItem(term, 0, [])
        endItem = DBItem(term, 0xFFFFFFFF, [])
        startKey = startItem.EncodeKey()
        endKey = endItem.EncodeKey()
        hitList = HitList()
        for k, v in self.db.RangeIter(key_from = startKey, key_to = endKey):
            item = DBItem("", 0, [])
            item.Decode(k, v)
            self.logger.debug("get gameId %d addrs %s" % (item.gameId, str(item.addrs)))
            hitList.hitList.append((item.gameId, item.addrs, item.nameWeight))
        return hitList


    def Search(self, query):
        termWeightBase = 0.7
        terms = Index.GetRightWords([query, ])
        hitListList = []
        for term in terms:
            self.logger.debug("term %s weight %f" % (term[0], term[1]))
            hitList = self.GetHitList(term[0])
            hitListList.append(hitList)

        termWeight = []
        curIndex= []
        allNum = 0
        addrWeight = {NameAddr:1, CategoryAddr:0.9, TagAddr:0.8, DescAddr:0.3}
        for i in range(len(hitListList)):
            allNum += len(hitListList[i].hitList)
            termWeight.append(len(hitListList[i].hitList))
            curIndex.append(0)
        if allNum == 0:
            return [], terms
        if len(hitListList) == 1:
            termWeight[i] = 1
        else:
            for i in range(len(hitListList)):
                termWeight[i] = termWeightBase * terms[i][1] + (1 - termWeightBase) * float(allNum - termWeight[i]) / allNum / (len(hitListList) - 1)
        self.logger.debug("weight %s" % str(termWeight))

        games = []
        while True:
            curMinGameId = 0xFFFFFFFF
            for i in range(len(hitListList)):
                if curIndex[i] < len(hitListList[i].hitList) and hitListList[i].hitList[curIndex[i]][0] < curMinGameId:
                    curMinGameId = hitListList[i].hitList[curIndex[i]][0]
            if curMinGameId == 0xFFFFFFFF:
                break
            self.logger.debug("deal with gameId %d" % curMinGameId)
            curWeight = 0
            nameWeight = 0
            for i in range(len(hitListList)):
                if curIndex[i] < len(hitListList[i].hitList) and hitListList[i].hitList[curIndex[i]][0] == curMinGameId:
                    maxAddr = 0
                    for addr in hitListList[i].hitList[curIndex[i]][1]:
                        if maxAddr< addrWeight[addr]:
                            maxAddr= addrWeight[addr]
                    curWeight += termWeight[i] * maxAddr
                    nameWeight += hitListList[i].hitList[curIndex[i]][2]
                    self.logger.debug("hit term %d %f %f" % (i, curWeight, nameWeight))
                    curIndex[i] += 1
            if len(games) < MaxRecomGame:
                heapq.heappush(games, [curWeight, curMinGameId, nameWeight])
            else:
                heapq.heappushpop(games, [curWeight, curMinGameId, nameWeight])


        games.sort(key=lambda g: g[0], reverse=True)

        return (games, terms)

    def RespGames(self, result, games, terms, address, s):
        resp = Response()
        resp.result = result
        for t in terms:
            q = resp.terms.add()
            q.term = t[0]
            q.weight = t[1]
        for g in games:
            r = resp.games.add()
            r.gameId = g[1]
            r.nameRel = g[2]
            r.gameRel = g[0]
        s.sendto(resp.SerializeToString(), address)
        

    def InitSeg(self):
        SegUtil.Init(self.segPath)
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
        self.logger.debug("add one game for one %d %s %s %s %s" % (gameId, game.name, game.description, str(categorys), str(tags)))
        Index.BuildIndexForOne(self.db, self.logger, gameId, game.name, game.description, categorys, tags)


    def StartServer(self, port):
        import socket
        host = "127.0.0.1"
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
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
                        self.RespGames(1, [], [], address, s)
                        return
                    self.logger.debug("get content %s" % query.query)
                    games, terms = self.Search(query.query)
                    for game in games:
                        self.logger.debug("game weight %f id %d" % (game[0], game[1]))
                    for term in terms:
                        self.logger.debug("term %s weight %f" % (term[0], term[1]))
                    self.RespGames(0, games, terms, address, s)
                elif cmd == 2:
                    gameId = struct.unpack("!I", message[0:4])[0]
                    self.AddOneGame(gameId)
                else:
                    self.logger.error("not find cmd %d" % cmd)
            except:
                self.logger.debug(traceback.format_exc())
                

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: %s cfg" % sys.argv[0]
        sys.exit()
    os.chdir(workPath)
    port = int(GetConfigValue("SEARCH_PORT", sys.argv[1]))
    pidFileName = GetConfigValue("PID_FILE", sys.argv[1])
    print port, pidFileName
    pidFile = file(pidFileName, "w")
    pidFile.write("%d" % os.getpid())
    pidFile.close()
    dbPath = GetConfigValue("DB_PATH", sys.argv[1])
    search = SearchIndex(dbPath, workPath + "/../")
    search.InitSeg()
    search.StartServer(port)


