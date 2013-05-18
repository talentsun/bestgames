# -*- coding: utf-8 -*-
from django.db import models
from django import forms
from django.forms import ModelForm

from weixin.models import BaseDialog

class DialogForm(ModelForm):
    question = forms.CharField(label=u"问题", help_text=u"20个字以内，是用户提问的问题", required=True, max_length = 100)
    answer = forms.CharField(label=u"答案", help_text=u"回答个用户的答案", required=True, max_length = 1000)
    class Meta:
        model = BaseDialog
        fields = ('question',
                  'answer',
                  'presenter')
