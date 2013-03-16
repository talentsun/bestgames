from django.db import models
# -*- coding: utf-8 -*-

# Create your models here.
class FollowMeTask(models.Model):
    uid = models.BigIntegerField(db_index=True)
    # status 0 is not finished
    # status 1 is finished
    status = models.IntegerField()
    # type 1 is follow me and friends > followers and followers < 150 and followers > 60 and location has not "北京" and "其他"
    type = models.IntegerField()
