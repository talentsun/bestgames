import django_tables2 as tables
from models import UserGift, WeixinUser, UserAnswer

class PhoneColumn(tables.Column):
    def render(self, value):
        return value[:-4]+'*'*4

class UserGiftTable(tables.Table):
    class Meta:
        model = UserGift
        order_by = "-getTime"
        attrs = {'class' : 'table table-striped'}
        orderable = False
        exclude = ('id',)
class WeixinUserTable(tables.Table):
    phone = PhoneColumn(attrs={"class":"phone"})
    class Meta:
        model = WeixinUser
        attrs = {'class' : 'table table-striped'}
        orderable = False
class UserAnswerTable(tables.Table):
    class Meta:
        model = UserAnswer
        attrs = {'class' : 'table table-striped'}
        orderable = False
        exclude = ('id',)
