#coding:utf-8
from django.db import models

from weixin.models import Puzzle
from django.utils import simplejson

# Create your models here.
class AllPuzzleUserByDay(models.Model):
    day = models.DateField(u"天")
    daystr = models.CharField(u"datestr", max_length=100)
    answer_num = models.IntegerField(u"使用趣味答题的用户", default = 0)
    phone_num = models.IntegerField(u"绑定手机的用户数目", default = 0)
    update_time = models.DateTimeField(u"计算时间", auto_now = True)

    class Meta:
        db_table = u"analyse_all_puzzle_user_day"
        verbose_name = u"puzzle用户按天全量分析"
        app_label = "analyse"

    def save(self, *args, **kwargs):
        self.daystr = self.day.strftime("%Y-%m-%d")
        super(AllPuzzleUserByDay, self).save(args, kwargs)


class DeltaPuzzleUserByDay(models.Model):
    day = models.DateField(u"天")
    daystr = models.CharField(u"datestr", max_length=100)
    new_user = models.IntegerField(u"新用户", default = 0)
    old_user = models.IntegerField(u"老用户", default = 0)
    update_time = models.DateTimeField(u"计算时间", auto_now = True)

    class Meta:
        db_table = u"analyse_delta_puzzle_user_day"
        verbose_name = u"puzzle用户按天增量分析"
        app_label = "analyse"

    def save(self, *args, **kwargs):
        self.daystr = self.day.strftime("%Y-%m-%d")
        super(DeltaPuzzleUserByDay, self).save(args, kwargs)

class PuzzleUserByPuzzle(models.Model):
    puzzle = models.ForeignKey(Puzzle, verbose_name=u"题目")
    new_user = models.IntegerField(u"新用户", default = 0)
    old_user = models.IntegerField(u"老用户", default = 0)
    update_time = models.DateTimeField(u"计算时间", auto_now = True)

    class Meta:
        db_table = u"analyse_puzzle_user_puzzle"
        verbose_name = u"puzzle用户按题目分析"
        app_label = "analyse"


