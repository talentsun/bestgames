from django.db import models
#coding: utf-8

class BaseDialog(models.Model):
    question = models.CharField(u"问题", max_length=1000)
    answer = models.CharField(u"答案", max_length=1000)
    


