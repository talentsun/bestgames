#!/usr/local/bin/python2.7
#coding: utf8

import sys, subprocess, os, os.path
workPath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(workPath + "/..")
from django.core.management import setup_environ
from content_engine import settings
setup_environ(settings)

from search_pb2 import Query, Response
import socket
import struct

from portal.models import Game



if __name__ == '__main__':

    for g in Game.objects.all():
        print "test game Id %d" % g.id
        stQuery = Query()
        stQuery.query = g.name

        query = stQuery.SerializeToString()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(struct.pack("!H", 1) + query, ("127.0.0.1", 8128))

        resp = s.recv(4196)
        stResp = Response()
        stResp.ParseFromString(resp)
        if stResp.games[0].gameId != g.id:
            for game in stResp.games:
                print "game %d name %f game %f" % (game.gameId, game.nameRel, game.gameRel)
        #for term in stResp.terms:
        #    print "term %s weight %f" % (term.term, term.weight)



