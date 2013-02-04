#!/usr/bin/python

from weibo import APIClient
from AppValue import BGApp

from Operation import Operation
from FriendShip import FriendShip

import time, sys

if __name__ == '__main__':
    if len(sys.argv) == 2:
        num = int(sys.argv[1])
    else:
        num = 0
    ops = Operation.FetchSomeDayOps(Operation.FollowType, num)
    print "all number %d" % len(ops)
    followNum = 0
    client = APIClient(BGApp.app_key, BGApp.app_secret)
    client.set_access_token(BGApp.dev_token, time.time() + 90 * 24 *3600)
    for op in ops:
        if FriendShip.CheckFollow(client, op.uid, BGApp.dev_uid):
            print op.uid, op.ts
            followNum += 1
        else:
            print "not follow:", op.uid, op.ts
    print "follow num %d" % followNum
