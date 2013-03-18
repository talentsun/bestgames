# -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import force_unicode
from taggit.managers import TaggableManager

class Entity(models.Model):
    GAME = 1
    REDIER = 2
    type = models.IntegerField(verbose_name=u'类型', default=GAME, editable=False)
    tags = TaggableManager(verbose_name=u"标签")

    weibo_sync_timestamp = models.DateTimeField(verbose_name=u"微博同步时间",blank=True, null=True)
    STATUS_DO_NOT_SYNC =  0
    STATUS_PENDING = 1
    STATUS_COMPLETED = 2
    STATUS_FAILED = 3
    STATUS_CHOICES = (
        (STATUS_DO_NOT_SYNC, u"不同步"),
        (STATUS_PENDING, u"等待 同步"),
        (STATUS_COMPLETED, u"同步成功"),
        (STATUS_FAILED, u"同步失败"))
    status = models.IntegerField(u"同步状态",max_length=20, choices=STATUS_CHOICES, default=STATUS_DO_NOT_SYNC, editable=False)
    presenter = models.CharField(u"推荐人",max_length=100)
    RATING_1 = 1
    RATING_2 = 2
    RATING_3 = 3
    RATING_4 = 4
    RATING_5 = 5
    RATING_CHOICES = (
        (RATING_5, u"5"),
        (RATING_4, u"4"),
        (RATING_3, u"3"),
        (RATING_1, u"2"),
        (RATING_1, u"1"))
    rating = models.IntegerField(u"评分", choices=RATING_CHOICES, default=RATING_3)
    brief_comment = models.CharField(u"一句话点评(同步到微信)", max_length=255)
    recommended_reason = models.TextField(u"推荐理由(同步到微博)")

    class Meta:
        db_table = u'entities'
    def __unicode__(self):
        return force_unicode(str(self.id))

class Category(models.Model):
    name = models.CharField(u"名称",max_length=100)

    def __unicode__(self):
        return force_unicode(self.name)
    class Meta:
        db_table = u'categories'

class Game(Entity):
    name = models.CharField(u"名称", max_length=100)
    icon = models.ImageField(u"图标", upload_to='upload/', max_length=255, blank=True)
    description = models.TextField(u"描述")
    android_download_url = models.URLField(u"安卓下载地址", max_length=255, blank=True)
    iOS_download_url = models.URLField(u"苹果下载地址", max_length=255, blank=True)
    category = models.ForeignKey(Category, verbose_name='分类')
    screenshot_path_1 = models.ImageField(u"截图1", upload_to='upload/', max_length=255, blank=True)
    screenshot_path_2 = models.ImageField(u"截图2", upload_to='upload/', max_length=255, blank=True)
    screenshot_path_3 = models.ImageField(u"截图3", upload_to='upload/', max_length=255, blank=True)
    screenshot_path_4 = models.ImageField(u"截图4", upload_to='upload/', max_length=255, blank=True)

    def __unicode__(self):
        return force_unicode(self.name)
    class Meta:
        db_table = u'games'
        verbose_name = u'精品游戏推荐'
        verbose_name_plural = u'精品游戏推荐'
    def save(self, *args, **kwargs):
        self.type = Entity.GAME
        if self.weibo_sync_timestamp is not None:
            self.status = Entity.STATUS_PENDING
        super(Game, self).save(args, kwargs)

class Redier(Entity):
    game = models.ForeignKey(Game, verbose_name='游戏')
    description = models.CharField(u"描述", max_length=100)
    redier_image = models.ImageField(u"攻略", upload_to='upload/', max_length=255, blank=True)

    class Meta:
        db_table = u'rediers'
        verbose_name = u'小兵变大咖'
        verbose_name_plural = u'小兵变大咖'
    def save(self, *args, **kwargs):
        self.type = Entity.REDIER
        if self.weibo_sync_timestamp is not None:
            self.status = Entity.STATUS_PENDING
        super(Redier, self).save(args, kwargs)