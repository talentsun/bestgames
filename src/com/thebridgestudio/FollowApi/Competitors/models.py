from django.db import models
# -*- coding: utf-8 -*-


from weibo import APIClient
from AppValue import BGApp

# Create your models here.
class Competitor(models.Model):
    uid = models.BigIntegerField()
    followers = models.IntegerField(default=0)
    friends = models.IntegerField(default=0)
    statuses = models.IntegerField(default=0)
    isTarget = models.IntegerField(default=0)
    nickName = models.CharField(max_length=50, default="")
    screenName = models.CharField(max_length=50, default="")
    description = models.CharField(max_length=1000, default="")

    def FormatJson(self):
        res = {}
        res['uid'] = self.uid
        res['followers'] = self.followers
        res['friends'] = self.friends
        res['statuses'] = self.statuses
        res['nickName'] = self.nickName
        res['screenName'] = self.screenName
        res['description'] = self.description
        return res


    def FetchInfo(self, client):
        infos = client.get.users__show(uid=self.uid)
        self.screenName = infos["screen_name"]

    @classmethod
    def GetNumbers(cls, client, coms):
        uidStr = ""
        for com in coms:
            uidStr += str(com.uid) + ","
        uidStr = uidStr[:-1]
        users = client.get.users__counts(uids=uidStr)
        for com in coms:
            for user in users:
                if user['id'] == com.uid:
                    com.followers = user['followers_count']
                    com.friends = user['friends_count']
                    com.statuses = user['statuses_count']
                    com.save()
                    break

    def GetFollowers(self, client, num):
        return client.get.friendships__followers(uid=str(self.uid), count=num)['users']



