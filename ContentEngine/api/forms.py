# -*- coding: utf-8 -*-
from django.db import models
from django import forms
from django.forms import ModelForm
from datetimewidget.widgets import DateTimeWidget

from api.models import Redier, Game, Category

class RedierForm(ModelForm):
	class Meta:
		model = Redier

class GameForm(ModelForm):
	category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=u"选择分类", label=u"分类")
	timestamp = forms.DateTimeField(label=u"同步时间",widget=DateTimeWidget)

	class Meta:
		model = Game
		fields = ('name', 
			'icon', 
			'description', 
			'category',
			'tags',
			'android_download_url', 
			'iOS_download_url', 
			'screenshot_path_1', 
			'screenshot_path_2', 
			'screenshot_path_3', 
			'screenshot_path_4', 
			'screenshot_path_5', 
			'sync_weibo',
			'timestamp',
			'presenter',
			'rating',
			'recommended_reason')