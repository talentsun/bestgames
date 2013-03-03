# -*- coding: utf-8 -*-
import sys
import os

from django.template import loader,Context
from django.http import HttpResponse
from api.models import HotGamesView

def HotGamesViewFunc(request):
    hotgames = HotGamesView.objects.all()
    t = loader.get_template("hotgames.html")
    c = Context({'hotgames':hotgames})
    return HttpResponse(t.render(c))
