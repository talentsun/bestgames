#!/usr/local/bin/python2.7
# -*- coding:utf-8 -*-

import sys, subprocess, os, os.path
workPath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(workPath + "/..")
from django.core.management import setup_environ
from content_engine import settings
setup_environ(settings)

from portal.models import Game, Category
import leveldb
from SegUtil import SegUtil
import logging, struct, os, os.path
from taggit.models import Tag

from Utils import *
NameAddr = 1
CategoryAddr = 2
TagAddr = 3
DescAddr = 4
logger = logging.getLogger("build_index")
single = workPath + "/update_index.single"


class DBItem:
    def __init__(self, term, gameId, addrs):
        self.term = term
        self.gameId = gameId
        self.addrs = addrs

    def Encode(self):
        term = self.term.encode("utf8")
        key = struct.pack("!H%dsI" % len(term), len(term), term, self.gameId)
        value = struct.pack("!B%dB" % len(self.addrs), len(self.addrs), *self.addrs)
        return (key, value)

    def EncodeKey(self):
        term = self.term.encode("utf8")
        key = struct.pack("!H%dsI" % len(term), len(term), term, self.gameId)
        return key
        
    def Decode(self, key, value):
        start = 0
        wLen = struct.unpack("!H", key[start: start + 2])[0]
        start += 2
        self.term = key[start: start + wLen].decode("utf8")
        start += wLen
        self.gameId = struct.unpack("!I", key[start: start + 4])[0]

        start = 0
        cLen = struct.unpack("!B", value[start: start + 1])[0]
        start += 1
        self.addrs = struct.unpack("!%dB" % cLen, value[start:start + cLen])
        start += cLen

class Index:
    def __init__(self, dataPath):
        self.path = dataPath

    def Show(self):
        item = DBItem("", 0, [])
        for k,v in self.db.RangeIter(include_value = True):
            item.Decode(k, v)
            self.logger.debug("term %s gameId %d addrs %s" % (item.term, item.gameId, str(item.addrs)))


    def CreateDB(self):
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
        self.db = leveldb.LevelDB(self.path, **options)
        self.logger = logging.getLogger("build_index") 
        SegUtil.Init(self.path + "/../")


    @classmethod
    def RightPos(cls, pos):
        if len(pos) > 0 and (pos[0] == 'n' or pos[0] == 'a' or pos[0] == 'v'):
            return True
        else:
            return False


    @classmethod
    def GetRightWords(cls, sentenses):
        words = []
        for s in sentenses:
            ts = SegUtil.Seg(s.encode('utf8'))
            for t in ts:
                if cls.RightPos(t[1]):
                    words.append(t[0].decode('utf8'))
        return words

        
    def BuildIndexForOne(self, gameId, name, description, categorys, tags):
        terms = {}
        self.logger.debug("build index for one %d %s %s %s %s" % (gameId, name, description, str(categorys), str(tags)))
        ts = self.GetRightWords([name,])
        terms[NameAddr] = []
        for t in ts:
            terms[NameAddr].append(t)
        ts = self.GetRightWords([description,])
        terms[DescAddr] = []
        for t in ts:
            terms[DescAddr].append(t)

        terms[CategoryAddr] = []
        ts = self.GetRightWords(categorys)
        for t in ts:
            terms[CategoryAddr].append(t)
        ts = self.GetRightWords(tags)
        terms[TagAddr] = []
        for t in ts:
            terms[TagAddr].append(t)
        term2Addrs = {}

        for k, v in terms.items():
            for term in v:
                self.logger.debug("%d %s" % (k, term))
                if term not in term2Addrs:
                    term2Addrs[term] = []

                if k not in term2Addrs[term]:
                    term2Addrs[term].append(k)


        for term, addrs in term2Addrs.items():
            self.logger.debug("term %s addrs %s" % (term, str(addrs)))
            item = DBItem(term, gameId, addrs)
            (k, v) = item.Encode()

            self.db.Put(k, v)

if __name__ == "__main__":
    os.chdir(workPath)
    if len(sys.argv) != 2:
        print "Usage: %s cfg" % sys.argv[0]
        sys.exit()

    if not CheckSingle(single):
        logger.error("another instance is running")
        sys.exit()

    dbPath = GetConfigValue("DB_PATH", sys.argv[1])
    if dbPath[-1] == '/':
        dbPath = dbPath[:-1]
    if CheckFileExist(dbPath + ".tmp"):
        DeleteFolders(dbPath + ".tmp")
    index = Index(dbPath + ".tmp")
    index.CreateDB()
    games = Game.objects.all()
    for game in games:
        tags = []
        for t in game.tags.all():
            tags.append(t.name)
        cats = [game.category.name, ]
        index.BuildIndexForOne(game.pk, game.name, game.description, cats, tags)


    pidFilePath = GetConfigValue("PID_FILE", sys.argv[1])
    port = int(GetConfigValue("SEARCH_PORT", sys.argv[1]))
    logger.debug("%s %d" % (pidFilePath, port))
    if CheckFileExist(pidFilePath) and PortIsUsed(port):
        logger.debug("search index active")
        pidFile = file(pidFilePath)
        pid = int(pidFile.readline().strip())
        KillOne(pid)
        pidFile.close()
    else:
        logger.debug("search index not active")

    if CheckFileExist(dbPath + ".bak"):
        DeleteFolders(dbPath + ".bak")
    if CheckFileExist(dbPath):
        os.rename(dbPath, dbPath + ".bak")
        DeleteFolders(dbPath)
    os.rename(dbPath + ".tmp", dbPath)

    subprocess.Popen("./SearchIndex.py Search.cfg", shell=True)
    RemoveSingle(single)



