from django.db import models
import time, datetime

# Create your models here.

class Operation(models.Model):
    opUid = models.BigIntegerField()
    addTime = models.DateTimeField(auto_now_add=True)
    state = models.IntegerField(default = 0)
    srcUid = models.BigIntegerField(default = 0)
    actionTime = models.DateTimeField(auto_now_add=True)
    followers = models.IntegerField(default = 0)
    friends = models.IntegerField(default = 0)
    statuses = models.IntegerField(default = 0)

    @classmethod
    def GetSomeDayOps(cls, someDay):
        beginTime = datetime.datetime(someDay.year, someDay.month, someDay.day)
        endTime = beginTime + datetime.timedelta(days=1)
        return Operation.objects.filter(actionTime__gte=beginTime).filter(actionTime__lt=endTime)
