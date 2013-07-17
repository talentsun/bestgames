# -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import force_unicode
from taggit.managers import TaggableManager
from django.shortcuts import get_object_or_404

class Entity(models.Model):
    GAME = 1
    REDIER = 2
    COLLECTION = 3
    PROBLEM = 4
    WEIXIN = 5
    PLAYER = 6
    NEWS = 7
    PUZZLE = 8
    type = models.IntegerField(verbose_name=u'类型', default=GAME, editable=False)
    tags = TaggableManager(verbose_name=u"标签",blank=True)

    message_id3 = models.IntegerField(max_length=255, blank=True)

    sync_timestamp1 = models.DateTimeField(verbose_name=u"同步时间1",blank=True)
    sync_timestamp2 = models.DateTimeField(verbose_name=u"同步时间2",blank=True)
    sync_timestamp3 = models.DateTimeField(verbose_name=u"同步时间3",blank=True)
    STATUS_DO_NOT_SYNC =  0
    STATUS_PENDING = 1
    STATUS_COMPLETED = 2
    STATUS_FAILED = 3
    STATUS_CHOICES = (
        (STATUS_DO_NOT_SYNC, u"不同步"),
        (STATUS_PENDING, u"等待 同步"),
        (STATUS_COMPLETED, u"同步成功"),
        (STATUS_FAILED, u"同步失败"))
    status1 = models.IntegerField(u"同步状态1",max_length=20, choices=STATUS_CHOICES, default=STATUS_DO_NOT_SYNC, editable=False)
    status2 = models.IntegerField(u"同步状态2",max_length=20, choices=STATUS_CHOICES, default=STATUS_DO_NOT_SYNC, editable=False)
    status3 = models.IntegerField(u"同步状态3",max_length=20, choices=STATUS_CHOICES, default=STATUS_DO_NOT_SYNC, editable=False)
    presenter = models.CharField(u"推荐人",max_length=100)
    brief_comment = models.CharField(u"一句话点评(同步到微信)", max_length=255,blank=True)
    recommended_reason = models.TextField(u"推荐理由(同步到微博)",blank=True)
    created_time = models.DateTimeField(u"创建时间", auto_now_add=True)

    def __unicode__(self):
        if self.type == 1:
            game = get_object_or_404(Game,game_id=self.id)
            return force_unicode(game.name)
        elif self.type == 6:
            player = get_object_or_404(Player, player_id=self.id)
            return force_unicode(player.title)
        elif self.type == 7:
            gameAdvice = get_object_or_404(GameAdvices, player_id=self.id)
            return force_unicode(gameAdvice.title)
        else:
            return u"entity"

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
    RATING_1 = 1
    RATING_2 = 2
    RATING_3 = 3
    RATING_4 = 4
    RATING_5 = 5
    RATING_6 = 6
    RATING_7 = 7
    RATING_8 = 8
    RATING_9 = 9
    RATING_10 = 10
    RATING_CHOICES = (
        (RATING_10, u"5"),
        (RATING_9, u"4.5"),
        (RATING_8, u"4"),
        (RATING_7, u"3.5"),
        (RATING_6, u"3"),
        (RATING_5, u"2.5"),
        (RATING_4, u"2"),
        (RATING_3, u"1.5"),
        (RATING_1, u"1"),
        (RATING_1, u"0.5"))
    rating = models.IntegerField(u"评分", choices=RATING_CHOICES, default=RATING_6)
    size = models.CharField(u"大小", max_length=100)
    video_url = models.URLField(u"视频", max_length=255, blank=True, help_text=u"目前只支持优酷的视频地址")

    def __unicode__(self):
        return force_unicode(self.name)
    class Meta:
        db_table = u'games'
        verbose_name = u'游戏推荐'
        verbose_name_plural = u'游戏推荐'
    def save(self, *args, **kwargs):
        self.type = Entity.GAME
        if self.status1 == Entity.STATUS_DO_NOT_SYNC:
            if self.sync_timestamp1 is not None:
                self.status1 = Entity.STATUS_PENDING
        if self.status2 == Entity.STATUS_DO_NOT_SYNC:
            if self.sync_timestamp2 is not None:
                self.status2 = Entity.STATUS_PENDING
        if self.status3 == Entity.STATUS_DO_NOT_SYNC:
            if self.sync_timestamp3 is not None:
                self.status3 = Entity.STATUS_PENDING

        super(Game, self).save(args, kwargs)

class Redier(Entity):
    game_name = models.CharField(u'游戏', max_length=255)
    title = models.CharField(u"标题", max_length=100)
    image_url = models.ImageField(u"图片", upload_to='upload/', max_length=255, blank=True)
    video_url = models.URLField(u"视频", max_length=255, blank=True, help_text=u"目前只支持优酷的视频地址")

    class Meta:
        db_table = u'rediers'
        verbose_name = u'小兵变大咖'
        verbose_name_plural = u'小兵变大咖'
    def save(self, *args, **kwargs):
        self.type = Entity.REDIER
        if self.status1 == Entity.STATUS_DO_NOT_SYNC:
            if self.sync_timestamp1 is not None:
                self.status1 = Entity.STATUS_PENDING
        if self.status2 == Entity.STATUS_DO_NOT_SYNC:
            if self.sync_timestamp2 is not None:
                self.status2 = Entity.STATUS_PENDING
        if self.status3 == Entity.STATUS_DO_NOT_SYNC:
            if self.sync_timestamp3 is not None:
                self.status3 = Entity.STATUS_PENDING

        super(Redier, self).save(args, kwargs)

class Collection(Entity):
    title = models.CharField(u"标题", max_length=20)
    cover = models.ImageField(u"封面图片", upload_to='upload/', max_length=255, blank=True)
    video_url = models.URLField(u"视频", max_length=255, blank=True, help_text=u"目前只支持优酷的视频地址")
    games = models.ManyToManyField(Game, verbose_name=u"游戏")

    class Meta:
        db_table = u'collections'
        verbose_name = u'游戏合集'
        verbose_name_plural = u'游戏合集'
    def save(self, *args, **kwargs):
        self.type = Entity.COLLECTION
        if self.status1 == Entity.STATUS_DO_NOT_SYNC:
            if self.sync_timestamp1 is not None:
                self.status1 = Entity.STATUS_PENDING
        if self.status2 == Entity.STATUS_DO_NOT_SYNC:
            if self.sync_timestamp2 is not None:
                self.status2 = Entity.STATUS_PENDING
        if self.status3 == Entity.STATUS_DO_NOT_SYNC:
            if self.sync_timestamp3 is not None:
                self.status3 = Entity.STATUS_PENDING

        super(Collection, self).save(args, kwargs)


class Problem(Entity):
    title = models.CharField(u"标题", max_length=50)
    image_url = models.ImageField(u"图片", upload_to='upload/', max_length=255, blank=True)
    video_url = models.URLField(u"视频", max_length=255, blank=True, help_text=u"目前只支持优酷的视频地址")

    class Meta:
        db_table = u'problems'
        verbose_name = u'宅，必有一技'
        verbose_name_plural = u'宅，必有一技'
    def save(self, *args, **kwargs):
        self.type = Entity.PROBLEM
        if self.status1 == Entity.STATUS_DO_NOT_SYNC:
            if self.sync_timestamp1 is not None:
                self.status1 = Entity.STATUS_PENDING
        if self.status2 == Entity.STATUS_DO_NOT_SYNC:
            if self.sync_timestamp2 is not None:
                self.status2 = Entity.STATUS_PENDING
        if self.status3 == Entity.STATUS_DO_NOT_SYNC:
            if self.sync_timestamp3 is not None:
                self.status3 = Entity.STATUS_PENDING

        super(Problem, self).save(args, kwargs)

class Player(Entity):
    title = models.CharField(u"标题", max_length=50)
    image_url = models.ImageField(u"图片", upload_to='upload/', max_length=255, blank=True)
    video_url = models.URLField(u"视频", max_length=255, blank=True, help_text=u"目前只支持优酷的视频地址")

    def __unicode__(self):
        return force_unicode(self.title)
    class Meta:
        db_table = u'players'
        verbose_name = u'我是玩家'
        verbose_name_plural = u'我是玩家'
    def save(self, *args, **kwargs):
        self.type = Entity.PLAYER
        if self.status1 == Entity.STATUS_DO_NOT_SYNC:
            if self.sync_timestamp1 is not None:
                self.status1 = Entity.STATUS_PENDING
        if self.status2 == Entity.STATUS_DO_NOT_SYNC:
            if self.sync_timestamp2 is not None:
                self.status2 = Entity.STATUS_PENDING
        if self.status3 == Entity.STATUS_DO_NOT_SYNC:
            if self.sync_timestamp3 is not None:
                self.status3 = Entity.STATUS_PENDING

        super(Player, self).save(args, kwargs)

class News(Entity):
    title = models.CharField(u"标题", max_length=50)
    screenshot_path_1 = models.ImageField(u"截图1", upload_to='upload/', max_length=255, blank=True)
    screenshot_path_2 = models.ImageField(u"截图2", upload_to='upload/', max_length=255, blank=True)
    screenshot_path_3 = models.ImageField(u"截图3", upload_to='upload/', max_length=255, blank=True)
    screenshot_path_4 = models.ImageField(u"截图4", upload_to='upload/', max_length=255, blank=True)
    video_url = models.URLField(u"视频", max_length=255, blank=True, help_text=u"目前只支持优酷的视频地址")

    def __unicode__(self):
        return force_unicode(self.title)
    class Meta:
        db_table = u'news'
        verbose_name = u'游戏情报站'
        verbose_name_plural = u'游戏情报站'
    def save(self, *args, **kwargs):
        self.type = Entity.NEWS
        if self.status1 == Entity.STATUS_DO_NOT_SYNC:
            if self.sync_timestamp1 is not None:
                self.status1 = Entity.STATUS_PENDING
        if self.status2 == Entity.STATUS_DO_NOT_SYNC:
            if self.sync_timestamp2 is not None:
                self.status2 = Entity.STATUS_PENDING
        if self.status3 == Entity.STATUS_DO_NOT_SYNC:
            if self.sync_timestamp3 is not None:
                self.status3 = Entity.STATUS_PENDING

        super(News, self).save(args, kwargs)

class Puzzle(Entity):
    title = models.CharField(u"简短描述", max_length=20, blank=True)
    image_url = models.ImageField(u"问题图片", upload_to='upload/', max_length=255, blank=True)
    description = models.TextField(u'题目描述')
    option1 = models.CharField(u'选项1', max_length=200, blank=True)
    option2 = models.CharField(u'选项2', max_length=200, blank=True)
    option3 = models.CharField(u'选项3', max_length=200, blank=True)
    option4 = models.CharField(u'选项4', max_length=200, blank=True)
    right_choices = (
        (0, '1'),
        (1, '2'),
        (2, '3'),
        (3, '4'),
    )
    right = models.IntegerField(u'正确选项', choices=right_choices, default = 0)

    class Meta:
        db_table = u'puzzles'
        verbose_name = u'趣题'
        verbose_name_plural = u'趣题'
        app_label = 'portal'
    def save(self, *args, **kwargs):
        self.type = Entity.PUZZLE
        if self.status1 == Entity.STATUS_DO_NOT_SYNC:
            if self.sync_timestamp1 is not None:
                self.status1 = Entity.STATUS_PENDING
        if self.status2 == Entity.STATUS_DO_NOT_SYNC:
            if self.sync_timestamp2 is not None:
                self.status2 = Entity.STATUS_PENDING
        if self.status3 == Entity.STATUS_DO_NOT_SYNC:
            if self.sync_timestamp3 is not None:
                self.status3 = Entity.STATUS_PENDING

        super(Puzzle, self).save(args, kwargs)

class Weixin(Entity):
    title = models.CharField(u"标题", max_length=20,blank=True)
    cover = models.ImageField(u"封面图片", upload_to='upload/', max_length=255, blank=True)
    games = models.ManyToManyField(Game, verbose_name=u"游戏推荐")
    news = models.ManyToManyField(News, verbose_name=u"游戏情报站")
    players = models.ManyToManyField(Player, verbose_name=u"我是玩家")
    puzzles = models.ManyToManyField(Puzzle, verbose_name=u"趣题")

    class Meta:
        db_table = u'weixins'
        verbose_name = u'微信合集'
        verbose_name_plural = u'微信合集'
    def save(self, *args, **kwargs):
        self.type = Entity.WEIXIN
        if self.status1 == Entity.STATUS_DO_NOT_SYNC:
            if self.sync_timestamp1 is not None:
                self.status1 = Entity.STATUS_PENDING
        if self.status2 == Entity.STATUS_DO_NOT_SYNC:
            if self.sync_timestamp2 is not None:
                self.status2 = Entity.STATUS_PENDING
        if self.status3 == Entity.STATUS_DO_NOT_SYNC:
            if self.sync_timestamp3 is not None:
                self.status3 = Entity.STATUS_PENDING

        super(Weixin, self).save(args, kwargs)
