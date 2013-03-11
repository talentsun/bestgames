from django.db import models

# Create your models here.
class Access(models.Model):
    uid = models.BigIntegerField()
    version = models.IntergerField()
    data1 = models.CharField(max_length=50, default="")
    date2 = models.CharField(max_length=50, default="")
