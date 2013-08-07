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

class Conversation(models.Model):
    user_content = models.CharField(u"用户消息", max_length=1000)
    content_type = models.CharField(u"用户消息类型", max_length=100)
    createtime = models.DateTimeField(u"创建时间")
    match_type = models.CharField(u"匹配类型", max_length=100, blank=True)
    reply_type = models.CharField(u"回复类型", max_length=100, blank=True)
    reply_data = models.CharField(u"回复数据", max_length=1000, blank=True)

    class Meta:
        db_table = u"conversation"
        verbose_name = u"微信对话消息"
        app_label = "weixin"
    

class WeixinUser(models.Model):
    src = models.CharField(u"来源账号", max_length=100, db_index=True)
    uid = models.CharField(u"微信id", max_length=100, db_index=True)
    integral = models.IntegerField(u"积分")
    phone = models.CharField(u"电话号码", max_length=20)
    addTime = models.DateTimeField(u"加入时间", auto_now_add=True)
    class Meta:
        db_table = u'weixin_user'
        verbose_name = u'微信用户'
        app_label = 'weixin'

    def __unicode__(self):
        return "%d" % self.id

class Gift(models.Model):
    name = models.CharField(u"名称", max_length=100)
    picture = models.ImageField(u"礼物图片", upload_to='upload/', max_length=255, blank=True)
    type_choices = (
        (1, '兑换码'),)
    type = models.SmallIntegerField(u"类型", choices=type_choices, default = 1) #1 shows it's value is the reward
    show_choices = (
        (1, '显示'),
        (0, '不显示'),
    )
    show = models.IntegerField(u'是否显示', choices=show_choices, default = 1)
    integral = models.IntegerField(u'所需积分')
    cost = models.IntegerField(u'花费')

    class Meta:
        db_table = u'gift'
        verbose_name = u'礼品'
        app_label = 'weixin'

    def __unicode__(self):
        return self.name

class GiftItem(models.Model):
    grade = models.ForeignKey(Gift, verbose_name=u'类别')
    state_choices = (
        (0, '未兑换'),
        (1, '已兑换'),)
    state = models.SmallIntegerField(u"状态", choices=state_choices, default = 0) #=1 shows it is sold out 0: it is available
    value = models.CharField(u"礼品内容", max_length=1000)

    class Meta:
        db_table = u'gift_item'
        verbose_name = u'具体礼品'
        app_label = 'weixin'

    def __unicode__(self):
        return self.grade.name

class UserGift(models.Model):
    user = models.ForeignKey(WeixinUser, verbose_name=u'用户')
    gift = models.ForeignKey(GiftItem, verbose_name=u'礼品')
    getTime = models.DateTimeField(u"兑奖时间", auto_now=True)

    class Meta:
        db_table = u"user_gift"
        verbose_name = u"兑奖记录"
        app_label = 'weixin'

class UserAnswer(models.Model):
    questionId = models.ForeignKey(Puzzle, verbose_name=u'题号')
    userId = models.ForeignKey(WeixinUser, verbose_name=u'用户')
    answerTime = models.DateTimeField(auto_now=True, verbose_name=u'答题时间')
    userOption = models.SmallIntegerField(u'答案')

    class Meta:
        db_table = u"user_answer"
        verbose_name = u'答题历史'
        app_label = 'weixin'
