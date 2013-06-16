# Create your views here.
#coding:utf-8

from Statistic.models import Pie
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.http import HttpResponse
import json


def get_pie_data(request):
    key = request.GET['dataKey']
    datas = Pie.objects.filter(dataKey=key).order_by('dataSequence')
    pieInfos = []
    for d in datas:
        pieInfos.append({'label':d.label, 'percent':d.percent})


    return HttpResponse(json.dumps(pieInfos))

def follower_status(request):
    return render(request, "follower_status.html")

