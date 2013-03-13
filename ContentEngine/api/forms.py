# -*- coding: utf-8 -*-
from django.db import models
from django import forms
from django.forms import ModelForm
from datetimewidget.widgets import DateTimeWidget
from ajax_upload.widgets import AjaxClearableFileInput

from api.models import Redier, Game, Category

class RedierForm(ModelForm):
	class Meta:
		model = Redier

class GameForm(ModelForm):
	category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=u"选择分类", label=u"分类")

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
			'weibo_sync_timestamp',
			'presenter',
			'rating',
			'recommended_reason')
		widgets = {
			'icon' : AjaxClearableFileInput(),
			'screenshot_path_1' : AjaxClearableFileInput(),
			'screenshot_path_2' : AjaxClearableFileInput(),
			'screenshot_path_3' : AjaxClearableFileInput(),
			'screenshot_path_4' : AjaxClearableFileInput(),
			'screenshot_path_5' : AjaxClearableFileInput(),
			'weibo_sync_timestamp' : DateTimeWidget(options={
				'autoclose' : 'true',
				'showMeridian' : 'true'
				})
		}