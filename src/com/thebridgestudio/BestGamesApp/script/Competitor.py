#!/usr/bin/python

from weibo import APIClient as APIClientV2
from AppValue import BGApp

import datetime, copy, sys, os
import MySQLdb

from Operation import Operation
from FriendShip import FriendShip

work_path = os.path.dirname(os.path.abspath(__file__))
singleFilePath = "competitor.single"

class Competitor:
    def __init__(self):
        self.uid = 0
        self.followers = 0
        self.friends = 0
        self.status = 0

    @classmethod
    def GetAllCompetitors(cls):
        conn = MySQLdb.connect(host='localhost', user='root', passwd='nameLR9969', db='bestgames', port=3306, charset='utf8')
        cursor = conn.cursor()
        cursor.execute("select uid, followers_count, friends_count, statuses_count from competitor")
        competitors = []
        for row in cursor.fetchall():
            com = Competitor()
            com.uid = row[0] 
            com.followers = row[1]
            com.friends = row[2]
            com.statuses = row[3]
            competitors.append(com)
            logger.debug("in db %d followers %d friends %d statuses %d" % (com.uid, com.followers, com.friends, com.statuses))
        cursor.close()
        conn.close()
        return competitors


    @classmethod
    def GetNumbers(cls, clientV2, coms, logger):
        uidStr = ""
        for com in coms:
            uidStr += str(com.uid) + ","

        uidStr = uidStr[0:-1]
        logger.debug("get number for %s" % uidStr)
        
        users = clientV2.get.users__counts(uids=uidStr)
        for com in coms:
            for user in users:
                if user['id'] == com.uid:
                    com.followers = user['followers_count']
                    com.friends = user['friends_count']
                    com.statuses = user['statuses_count']
                    logger.debug("%d from web followers %d friends %d statuses %d" % (com.uid, com.followers, com.friends, com.statuses))
                    break
        return

    def GetFollowers(self, clientV2, num):
        return clientV2.get.friendships__followers__ids(uid=str(self.uid), count=num)['ids']

    def Save(self):
        conn = MySQLdb.connect(host='localhost', user='root', passwd='nameLR9969', db='bestgames', port=3306, charset='utf8')
        cursor = conn.cursor()
        cursor.execute("delete from competitor where uid = %d" % self.uid)
        cursor.execute("insert into competitor (uid, followers_count, friends_count, statuses_count) values(%d, %d, %d, %d)" % (self.uid, self.followers, self.friends, self.statuses))
        cursor.close()
        conn.close()
        

def FollowUid(uid_, client, logger):
    logger.debug("try to follow %d", uid_)
    ops = Operation.FetchOps(uid_)
    meFollowing = FriendShip.CheckFollow(client, BGApp.dev_uid, uid_)
    meFollowed = FriendShip.CheckFollow(client, uid_, BGApp.dev_uid)
    logger.debug("ops num %d meFollowing %d meFollowed %d" % (len(ops), meFollowing, meFollowed))
    if len(ops) == 0 and not meFollowing and not meFollowed:
        client.post.friendships__create(uid=uid_)
        op = Operation()
        op.uid = uid_
        op.type = Operation.FollowType
        op.state = Operation.Finished
        op.Save()
        return True
    return False



if __name__ == '__main__':
    from Utils import *
    os.chdir(work_path)

    logger = InitLogger("follow_competitor", logging.DEBUG, "../log/follow_competitor.log")
    try:
        if not CheckSingle(singleFilePath):
            sys.exit("another instance running")
        comsDb = Competitor.GetAllCompetitors()
        logger.debug("competitor len %d" % len(comsDb))
        comsWeb = copy.deepcopy(comsDb)
        todayMaxNum = 30
        todayOpNum = len(Operation.FetchTodayOps(Operation.FollowType))
        client = APIClientV2(BGApp.app_key, BGApp.app_secret)
        client.set_access_token(BGApp.dev_token, time.time() + 90 * 24 *3600)
        Competitor.GetNumbers(client, comsWeb, logger)
        for comDb in comsDb:
            for comWeb in comsWeb:
                if comDb.uid == comWeb.uid:
                    if comWeb.followers > comDb.followers:
                        num = comWeb.followers - comDb.followers
                        logger.debug("%d's followers increase %d" % (comWeb.uid, num))
                        if num > 2:
                            num = 2
                        uids = comWeb.GetFollowers(client, num)
                        for uid in uids:
                            if todayOpNum < todayMaxNum:
                                ret = FollowUid(uid, client, logger)
                                if ret:
                                    logger.debug("follow success")
                                    todayOpNum += 1
                                    continue
                            else:
                                logger.debug("today's follow count reach max %d" % todayOpNum)
                                op = Operation()
                                op.uid = uid
                                op.type = Operation.AtType
                                op.state = Operation.NotFinished
                                op.Save()
                    if not comWeb.followers == comDb.followers:
                        logger.debug("%d's followers %d different from original %d" % (comWeb.uid, comWeb.followers, comDb.followers))
                        comDb.followers = comWeb.followers
                        comDb.friends = comWeb.friends
                        comDb.statuses = comWeb.statuses
                        comDb.Save()
        RemoveSingle(singleFilePath)
    except Exception as e:
        traceback.print_exc()
        logger.debug(traceback.format_exc())

