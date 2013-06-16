from django.db import models

# Create your models here.

class Pie(models.Model):
    dataKey = models.CharField(max_length=100)
    dataSequence = models.IntegerField()
    label = models.CharField(max_length=100)
    percent = models.FloatField()#not required to sum 1

    class Meta:
        db_table = u'pie_table'
