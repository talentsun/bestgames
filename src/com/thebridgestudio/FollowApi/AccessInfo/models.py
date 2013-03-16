from django.db import models

# Create your models here.
class Access(models.Model):
    uid = models.BigIntegerField(db_index=True, unique=True)
    version = models.IntegerField()
    data1 = models.CharField(max_length=50, default="")
    data2 = models.CharField(max_length=50, default="")
