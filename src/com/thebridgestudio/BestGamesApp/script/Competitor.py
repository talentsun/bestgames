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
        return clientV2.get.friendships__followers(uid=str(self.uid), count=num)['users']

    def Save(self):
        conn = MySQLdb.connect(host='localhost', user='root', passwd='nameLR9969', db='bestgames', port=3306, charset='utf8')
        cursor = conn.cursor()
        cursor.execute("delete from competitor where uid = %d" % self.uid)
        cursor.execute("insert into competitor (uid, followers_count, friends_count, statuses_count) values(%d, %d, %d, %d)" % (self.uid, self.followers, self.friends, self.statuses))
        cursor.close()
        conn.close()
        

def FollowUid(user, client, logger):
    logger.debug("try to follow %d", user['id'])
    ops = Operation.FetchOps(user['id'])
    meFollowing = FriendShip.CheckFollow(client, BGApp.dev_uid, user['id'])
    meFollowed = FriendShip.CheckFollow(client, user['id'], BGApp.dev_uid)
    logger.debug("ops num %d meFollowing %d meFollowed %d" % (len(ops), meFollowing, meFollowed))
    if len(ops) == 0 and not meFollowing and not meFollowed:
        client.post.friendships__create(uid=user['id'])
        op = Operation()
        op.uid = user['id'] 
        op.type = Operation.FollowType
        op.state = Operation.Finished
        op.online = user['online_status']
        op.followers = user['followers_count']
        op.friends = user['friends_count']
        op.statuses = user['statuses_count']
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
        todayOpNum = len(Operation.FetchSomeDayOps(Operation.FollowType, 0))
        logger.debug("current op number %d" % todayOpNum)
        client = APIClientV2(BGApp.app_key, BGApp.app_secret)
        client.set_access_token(BGApp.other_token, time.time() + 90 * 24 *3600)
        Competitor.GetNumbers(client, comsWeb, logger)
        for comDb in comsDb:
            for comWeb in comsWeb:
                if comDb.uid == comWeb.uid:
                    if comWeb.followers > comDb.followers:
                        num = comWeb.followers - comDb.followers
                        logger.debug("%d's followers increase %d" % (comWeb.uid, num))
                        if num > 1:
                            num = 1
                        followers = comWeb.GetFollowers(client, num)
                        for user in followers:
                            if todayOpNum < todayMaxNum:
                                ret = FollowUid(user, client, logger)
                                if ret:
                                    logger.debug("follow success")
                                    todayOpNum += 1
                                    continue
                                else:
                                    logger.debug('follow failed')
                            else:
                                logger.debug("today's follow count reach max %d" % todayOpNum)
                                op = Operation()
                                op.uid = user['id']
                                op.type = Operation.AtType
                                op.state = Operation.NotFinished
                                op.online = user['online_status']
                                op.followers = user['followers_count']
                                op.friends = user['friends_count']
                                op.statuses = user['statuses_count']
                                op.Save()
                    if not comWeb.followers == comDb.followers:
                        logger.debug("%d's followers %d different from original %d" % (comWeb.uid, comWeb.followers, comDb.followers))
                        comDb.followers = comWeb.followers
                        comDb.friends = comWeb.friends
                        comDb.statuses = comWeb.statuses
                        comDb.Save()
        RemoveSingle(singleFilePath)
    except Exception as e:
        RemoveSingle(singleFilePath)
        traceback.print_exc()
        logger.debug(traceback.format_exc())

