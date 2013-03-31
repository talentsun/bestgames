#!/usr/local/bin/python2.7
#coding: utf8

from search_pb2 import Query, Response
import socket
import struct



if __name__ == '__main__':
    stQuery = Query()
    stQuery.query = u"僵尸"

    query = stQuery.SerializeToString()
    print len(query)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(struct.pack("!H", 1) + query, ("127.0.0.1", 8128))

    resp = s.recv(4196)
    stResp = Response()
    stResp.ParseFromString(resp)
    print "result %d" % stResp.result
    print "gameIds %s" % str(stResp.gameIds)



