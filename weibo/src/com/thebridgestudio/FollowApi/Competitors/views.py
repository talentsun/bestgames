# Create your views here.
from Competitors.models import Competitor

from django.http import HttpResponse

from django.template import Context, loader

import json


def index(request):
    coms = Competitor.objects.all()
    comJson = []
    for com in coms:
        comJson.append(com.FormatJson())
    return HttpResponse(json.dumps(comJson))
    

