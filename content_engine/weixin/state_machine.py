#!/usr/local/bin/python
#coding:utf8

from django.core.cache import cache



class StateMachine(object):
    stateRoute = {}

    def __init__(self):
        self.timeout = 15 * 60
    @classmethod
    def Register(cls, stateId, smObj)
        if stateId in cls.stateRoute:
            raise Exception, "%d already registered" % stateId
        stateRoute = smObj

    @classmethod
    def matchState(cls, rule, info):
        stateInfo = cache.get('state_%s' % info.user)
        if stateInfo == None or stateInfo[0] not in cls.stateRoute:
            return False

        smObj = cls.stateRoute[stateInfo[0]]
        return smObj.match(stateInfo[1])

    @classmethod
    def dealState(cls, rule, info):
        stateInfo = cache.get('state_%s' % info.user)
        smObj = StateMachine.stateRoute[stateInfo[0]]
        return smObj.deal(stateInfo[1])


    def store(self, userId, value):
        cache.set('state_%s' % userId, value, self.timeout)

    def end(self, userId):
        cache.delete("state_%s" % userId)

    def deal(self, value):
        raise Exception, "not implemented"

    def match(self, value):
        raise Exception, "not implemented"

    def start(self):
        raise Exception, "not implemented"

Router.get_instance().set({
    'name' :u"状态机",
    'patterm' : StateMachine.matchState,
    'handler' : StateMachine.dealState
})






        
    
