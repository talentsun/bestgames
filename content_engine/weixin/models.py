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
    uid = models.CharField(u"统一id", max_length=100, db_index=True)
    integral = models.IntegerField(u"积分")
    phone = models.CharField(u"电话号码", max_length=20)
    addTime = models.DateTimeField(u"添加时间", auto_now=True)
    class Meta:
        db_table = u'weixin_user'
        verbose_name = u'微信用户'
        app_label = 'weixin'

class Gift(models.Model):
    name = models.CharField(u"名称", max_length=100)
    picture = models.ImageField(u"礼物图片", upload_to='upload/', max_length=255, blank=True)
    integral = models.IntegerField(u'所需积分')
    cost = models.IntegerField(u'花费')

    class Meta:
        db_table = u'gift'
        verbose_name = u'礼品'
        app_label = 'weixin'

class GiftItem(models.Model):
    grade = models.ForeignKey(Gift)
    type = models.SmallIntegerField(u"类型") #1 shows it's value is the reward
    state = models.SmallIntegerField(u"状态") #=1 shows it is sold out 0: it is available
    value = models.CharField(u"具体的奖品内容", max_length=1000)

    class Meta:
        db_table = u'gift_item'
        verbose_name = u'具体礼品'
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
