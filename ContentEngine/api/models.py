# -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import force_unicode

class Tags(models.Model):
    name = models.CharField(u"名称",max_length=100)

    def __unicode__(self):
        return force_unicode(self.name)
    class Meta:
        db_table = u'Tags'

class Entity_Types(models.Model):
    name = models.CharField(u"分类",max_length=100)

    def __unicode__(self):
        return force_unicode(self.name)

    class Meta:
        db_table = u'Entity_Types'

class Entities(models.Model):
    HOTGAME = 'HG'
    GAMEREDIER = 'GR'
    TYPE_CHOICES = (
        (HOTGAME, '热门游戏'),
        (GAMEREDIER, '游戏攻略'),
        )
    type = models.CharField(u'任务类型',max_length = 20, choices=TYPE_CHOICES,default=HOTGAME)

    SYNC = 1
    NOSYNC = 0
    SYNC_CHOICES = (
        (SYNC, '是'),
        (NOSYNC, '否'),
        )
    is_weibo_recommended = models.IntegerField(u"是否同步到微博",choices=SYNC_CHOICES,default=SYNC)
    is_qq_recommended = models.IntegerField(u"是否同步到QQ群",choices=SYNC_CHOICES,default=NOSYNC)
    is_weixin_recommended = models.IntegerField(u"是否同步到微信",choices=SYNC_CHOICES,default=NOSYNC)
    timestamp = models.DateTimeField(u"同步时间")
    rating = models.IntegerField(u"游戏评分")
    presenter = models.CharField(u"推荐人",max_length=100)
    recommended_reason = models.TextField(u"推荐理由")
    status = models.CharField(u"推荐状态",max_length = 20, default='未推荐')


    class Meta:
        db_table = u'Entities'
        verbose_name = u'热门游戏'
        verbose_name_plural = u'热门游戏'
    def __unicode__(self):
#        return str(self.is_qq_recommended) + str(self.is_weixin_recommended)
        return force_unicode(str(self.id))

class Tasks(models.Model):
    entity_id = models.ForeignKey(Entities)
    type = models.CharField(max_length=20)
    timestamp = models.TimeField()
    status = models.CharField(max_length=20)

    class Meta:
        db_table = u'Tasks'

class Entities_Tags(models.Model):
    entity_id = models.ForeignKey(Entities)
    tag_id = models.ForeignKey(Tags)

    class Meta:
        db_table = u'Entities_Tags'

class Game_Categories(models.Model):
    name = models.CharField(u"分类名称",max_length=100)

    def __unicode__(self):
        return force_unicode(self.name)

    class Meta:
        db_table = u'Game_Categories'
        verbose_name = u'游戏分类'
        verbose_name_plural = u'游戏分类'

class Hot_Games(models.Model):
    name = models.CharField(u"游戏名称",max_length=100)
    icon_path = models.ImageField(u"游戏图标",upload_to='upload/',blank=True)
    description = models.TextField(u"游戏描述")
    android_download_url = models.CharField(u"Android下载地址",max_length=255)
    iOS_download_url = models.CharField(u"IOS下载地址",max_length=255)
    entity_id = models.ForeignKey(Entities,related_name='hotgames')
    category = models.ForeignKey(Game_Categories,verbose_name='游戏分类')
    tag = models.ManyToManyField(Tags,verbose_name="标签")
    screenshot_path_1 = models.ImageField(u"游戏截图一",upload_to='upload/',blank=True)
    screenshot_path_2 = models.ImageField(u"游戏截图二",upload_to='upload/',blank=True)
    screenshot_path_3 = models.ImageField(u"游戏截图三",upload_to='upload/',blank=True)
    screenshot_path_4 = models.ImageField(u"游戏截图四",upload_to='upload/',blank=True)
    screenshot_path_5 = models.ImageField(u"游戏截图五",upload_to='upload/',blank=True)

    def __unicode__(self):
        return force_unicode(self.name)
    class Meta:
        db_table = u'Hot_Games'
        verbose_name = u'游戏'
        verbose_name_plural = u'游戏'

class GameRediers(models.Model):
    hot_game_id = models.ForeignKey(Hot_Games,verbose_name='游戏名称')
    summary = models.TextField(u"攻略简介")
    toll_gate = models.CharField(u"游戏关卡",max_length=100)
    path = models.ImageField(u"游戏攻略",upload_to='upload/',blank=True)

    class Meta:
        db_table = u'Game_Rediers'
        verbose_name = u'游戏推荐'
        verbose_name_plural = u'游戏推荐'



class HotGamesView(models.Model):
    name = models.CharField(u"游戏名称",max_length=100)
    timestamp = models.DateTimeField(u"同步时间")
    tags = models.CharField(u"标签",max_length=100)
#    status = models.CharField(u"推荐状态",max_length=100)
    presenter = models.CharField(u"推荐人",max_length=100)

    class Meta:
        managed=False
        db_table = u'hotgames'


class HotGamesRedierView(models.Model):
    name = models.CharField(u"游戏名称",max_length=100)
    timestamp = models.DateTimeField(u"同步时间")
    tags = models.CharField(u"标签",max_length=100)
    #    status = models.CharField(u"推荐状态",max_length=100)
    presenter = models.CharField(u"推荐人",max_length=100)
    toll_gate = models.CharField(u'游戏关卡',max_length=100)

    class Meta:
        managed=False
        db_table = u'hotgamesRedier'

