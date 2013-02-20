#!/usr/bin/python

from weibo import APIClient
from AppValue import BGApp

import datetime, copy, sys, os, time, traceback
import MySQLdb

from Utils import *

from Operation import Operation
from FriendShip import FriendShip

if __name__ == "__main__":
    if len(sys.argv) == 2:
        num = int(sys.argv[1])
    else:
        num = 7
    logger = InitLogger("unfollow_competitor", logging.DEBUG, "../log/unfollow_competitor.log")
    ops = Operation.FetchSomeDayOps(Operation.FollowType, num)
    client = APIClient(BGApp.app_key, BGApp.app_secret)
    client.set_access_token(BGApp.other_token, time.time() + 90*24*3600)
    for op in ops:
        try:
            logger.debug("unfollow %d", op.uid)
            print op.uid
            if op.state == Operation.Finished:
                op.state = Operation.Removed
                op.Save()
                FriendShip.Unfollow(client, op.uid)
            time.sleep(60)
        except Exception as e:
            traceback.print_exc()
            logger.debug(traceback.format_exc())

