#coding: utf-8
from django.db import models
from portal.models import Puzzle

class BaseDialog(models.Model):
    question = models.CharField(u"问题", max_length=100)
    answer = models.CharField(u"答案", max_length=1000)
    presenter = models.CharField(u"推荐人",max_length=100)

    class Meta:
        db_table = u'base_dialog'
        verbose_name = u'基本对话'
        verbose_name_plural = u'基本对话'
        app_label = 'weixin'
    

class WeixinUser(models.Model):
    uid = models.CharField(u"统一id", max_length=100)
    integral = models.IntegerField(u"积分")
    class Meta:
        db_table = u'weixin_user'
        verbose_name = u'微信用户'
        app_label = 'weixin'


class RewardItem(models.Model):
    grade = models.SmallIntegerField(u"等级")
    type = models.SmallIntegerField(u"类型") #1 shows it's value is the reward
    state = models.SmallIntegerField(u"状态") #=1 shows it is sold out 0: it is available
    value = models.CharField(u"具体的奖品内容", max_length=1000)

    class Meta:
        db_table = u'reward_item'
        verbose_name = u'奖品'
        app_label = 'weixin'

class UserAnswer(models.Model):
    questionId = models.ForeignKey(Puzzle)
    userId = models.ForeignKey(WeixinUser)
    answerTime = models.DateTimeField(auto_now=True)
    userOption = models.SmallIntegerField(u'用户提交的答案')

    class Meta:
        db_table = u"user_answer"
        verbose_name = u'用户答题历史'
        app_label = 'weixin'
