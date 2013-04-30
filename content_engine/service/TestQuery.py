#!/usr/local/bin/python2.7
#coding: utf8

from search_pb2 import Query, ResponseDialog
import socket
import struct



if __name__ == '__main__':
    stQuery = Query()
    stQuery.query = u"牛逼"

    query = stQuery.SerializeToString()
    print len(query)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(struct.pack("!H", 1) + query, ("127.0.0.1", 8038))

    resp = s.recv(4196)
    stResp = ResponseDialog()
    stResp.ParseFromString(resp)
    print "result %d" % stResp.result
    for d in stResp.dialogs:
        print "dialog %d weight %f" % (d.qId, d.rel)
    for term in stResp.terms:
        print "term %s weight %f" % (term.term, term.weight)



