#coding: utf-8
from django.db import models
import time, datetime

# Create your models here.

class Operation(models.Model):
    opUid = models.BigIntegerField()
    addTime = models.DateTimeField(auto_now_add=True)
    state = models.IntegerField(default = 0) #0 not follow 1 关注了他 2 对他进行了求关注 3 已经对其撤销了关注 4 自己回粉的
    srcUid = models.BigIntegerField(default = 0)
    actionTime = models.DateTimeField(auto_now_add=True)
    followers = models.IntegerField(default = 0)
    friends = models.IntegerField(default = 0)
    statuses = models.IntegerField(default = 0)

    @classmethod
    def GetSomeDayOps(cls, someDay, state_ = -1):
        beginTime = datetime.datetime(someDay.year, someDay.month, someDay.day)
        endTime = beginTime + datetime.timedelta(days=1)
        if state_ == -1:
            return Operation.objects.filter(actionTime__gte=beginTime).filter(actionTime__lt=endTime)
        else:
            return Operation.objects.filter(actionTime__gte=beginTime).filter(actionTime__lt=endTime).filter(state=state_)
