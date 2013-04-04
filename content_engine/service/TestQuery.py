#!/usr/local/bin/python2.7
#coding: utf8

from search_pb2 import Query, Response
import socket
import struct



if __name__ == '__main__':
    stQuery = Query()
    stQuery.query = u"蘑菇大战"

    query = stQuery.SerializeToString()
    print len(query)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(struct.pack("!H", 1) + query, ("127.0.0.1", 8128))

    resp = s.recv(4196)
    stResp = Response()
    stResp.ParseFromString(resp)
    print "result %d" % stResp.result
    for game in stResp.games:
        print "game %d name %f game %f" % (game.gameId, game.nameRel, game.gameRel)
    for term in stResp.terms:
        print "term %s weight %f" % (term.term, term.weight)



