#!/usr/local/bin/python2.7

import sys, time
sys.path.append("..")
import socket, subprocess

from django.core.management import setup_environ
from content_engine import settings
setup_environ(settings)

from portal.models import Game

from Utils import *
workPath = os.path.dirname(os.path.abspath(__file__))
single = workPath + "/update_index.single"
logger = logging.getLogger("build_index")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: %s cfg" % sys.argv[0]
        sys.exit()


    if not CheckSingle(single):
        logger.debug("another instance is running")
        sys.exit()

    port = int(GetConfigValue("SEARCH_PORT", sys.argv[1]))
    lastIdPath = GetConfigValue("LAST_ID_FILE", sys.argv[1])

    if not PortIsUsed(port):
        logger.error("search index not active")
        print "search index not active"
        subprocess.Popen("./SearchIndex.py Search.cfg", shell=True)

    if CheckFileExist(lastIdPath):
        lastIdFile = file(lastIdPath)
        lastId = int(lastIdFile.readline().strip())
        lastIdFile.close()
    else:
        lastId = 0
    logger.debug("%d %s %d" % (port, lastIdPath, lastId))

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    nextId = lastId
    for game in Game.objects.filter(id__gt = lastId):
        logger.debug("update index %d" % game.pk)
        content = struct.pack("!HI", 2, game.pk)
        s.sendto(content, ("127.0.0.1", port))
        time.sleep(0.1)
        if game.pk > nextId:
            nextId = game.pk

    lastIdFile = file(lastIdPath, "w")
    lastIdFile.write("%d" % nextId)
    lastIdFile.close()
    RemoveSingle(single)



     

