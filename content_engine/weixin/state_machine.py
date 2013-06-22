#!/usr/local/bin/python
#coding:utf8

from router import Router
from django.core.cache import cache
import time

class StateMachine(object):
    stateRoute = {}
    def __init__(self):
        self.timeout = 15 * 60
    @classmethod
    def register(cls, stateId, smObj):
        if stateId in cls.stateRoute:
            raise Exception, "%d already registered" % stateId
        cls.stateRoute[stateId] = smObj

    def store(self, userId, value):
        stateInfo = (self.stateId, value)
        cache.set('state_%s' % userId, stateInfo, self.timeout)
        print userId

    @classmethod
    def end(self, userId):
        cache.delete("state_%s" % userId)

    def deal(self, value, info):
        raise Exception, "not implemented"

    def match(self, value, info):
        raise Exception, "not implemented"

    def start(self):
        raise Exception, "not implemented"
def matchState(rule, info):
    print time.time(), info.user
    stateInfo = cache.get('state_%s' % info.user)
    print stateInfo
    if stateInfo == None or stateInfo[0] not in StateMachine.stateRoute:
        return False

    smObj = StateMachine.stateRoute[stateInfo[0]]
    print time.time()
    return smObj.match(stateInfo[1], info)

def dealState(rule, info):
    stateInfo = cache.get('state_%s' % info.user)
    smObj = StateMachine.stateRoute[stateInfo[0]]
    return smObj.deal(stateInfo[1], info)

Router.get_instance().set({
    'name' :u"状态机",
    'pattern' : matchState,
    'handler' : dealState
})






        
    
