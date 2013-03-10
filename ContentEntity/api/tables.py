#!/usr/bin/python
#coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from api.models import HotGamesView, HotGamesRedierView
import django_tables2 as tables
from django_tables2.columns import DateTimeColumn, TemplateColumn

class HotGamesTable(tables.Table):
    id = tables.Column(orderable=False, visible=False)
    name = tables.Column(orderable=False)
    presenter = tables.Column(orderable=False)
    timestamp = DateTimeColumn(orderable=True)
    status = TemplateColumn(template_name="sync_status_field.html",orderable=False,verbose_name="状态")
    tags = tables.Column(orderable=False,attrs={"class":"tags"})
    ops = TemplateColumn(template_name="hotgames_field_ops.html",verbose_name="操作",orderable=False,attrs={"class":"ops"})
    
    class Meta:
        model = HotGamesView
	order_by = "-timestamp"
	empty_text = u"暂无精品游戏推荐"
        sequence = ("name","presenter","timestamp","status","tags","ops")

class GameRediersTable(tables.Table):
    id = tables.Column(orderable=False, visible=False)
    name = tables.Column(orderable=False)
    toll_gate = tables.Column(orderable=False)
    presenter = tables.Column(orderable=False)
    timestamp = DateTimeColumn(orderable=True)
    status = TemplateColumn(template_name="sync_status_field.html",orderable=False,verbose_name="状态")
    tags = tables.Column(orderable=False,attrs={"class":"tags"})
    ops = TemplateColumn(template_name="gamerediers_field_ops.html",verbose_name="操作",orderable=False,attrs={"class":"ops"})

    class Meta:
        model = HotGamesRedierView
	order_by = "-timestamp"
	empty_text = "暂无小兵变大咖"
        sequence = ("name","toll_gate", "presenter","timestamp","status","tags","ops")
