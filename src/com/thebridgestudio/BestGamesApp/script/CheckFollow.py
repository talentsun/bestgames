#!/usr/bin/python

from weibo import APIClient
from AppValue import BGApp

from Operation import Operation
from FriendShip import FriendShip

if __name__ == '__main__':
    ops = Operation.FetchSomeDayOps(Operation.FollowType, 1)
    print "all number %d" % len(ops)
    followNum = 0
    client = APIClientV2(BGApp.app_key, BGApp.app_secret)
    client.set_access_token(BGApp.dev_token, time.time() + 90 * 24 *3600)
    for op in ops:
        if FriendShip.CheckFollow(op.uid, BGApp.uid):
            followNum += 1
    print "follow num %d" % followNum
