#coding:utf-8
# Create your views here.

import logging

from django.shortcuts import render_to_response, get_object_or_404, render, redirect

from django.utils import simplejson
from chartit import DataPool, Chart
from models import *

logger = logging.getLogger('default')


def get_all_puzzle_user_day():
    data = DataPool(series=[
        {
            'options': {
                'source': AllPuzzleUserByDay.objects.filter().order_by('day')
            },
            'terms': ['daystr', 'answer_num', 'phone_num']
        }])
    cht = Chart(
        datasource = data,
        series_options = [
            {
                'options': {
                    'type': 'line',
                    'stacking': False
                },
                'terms': {
                    'daystr': ['answer_num', 'phone_num']
                }
            }],
        chart_options = {
            'title': {
                'text': u'使用过答题功能的用户'},
            'xAxis': {
                'title': {
                    'text': u'日期'}}})
    return cht

def get_delta_puzzle_user_day():
    data = DataPool(series=[
        {
            'options': {
                'source': DeltaPuzzleUserByDay.objects.filter().order_by('day')
            },
            'terms': ['daystr', 'new_user', 'old_user']
        }])
    cht = Chart(
        datasource = data,
        series_options = [
            {
                'options': {
                    'type': 'column',
                    'stacking': True
                },
                'terms': {
                    'daystr': ['new_user', 'old_user']
                }
            }],
        chart_options = {
            'title': {
                'text': u'每天答题用户'},
            'xAxis': {
                'title': {
                    'text': u'日期'}}})
    return cht
def get_puzzle_user_puzzle():
    data = DataPool(series=[
        {
            'options': {
                'source': PuzzleUserByPuzzle.objects.filter().order_by('puzzle')
            },
            'terms': ['puzzle', 'new_user', 'old_user']
        }])
    cht = Chart(
        datasource = data,
        series_options = [
            {
                'options': {
                    'type': 'column',
                    'stacking': True
                },
                'terms': {
                    'puzzle': ['new_user', 'old_user']
                }
            }],
        chart_options = {
            'title': {
                'text': u'每题的答题人数'},
            'xAxis': {
                'title': {
                    'text': u'题目'}}})
    return cht





def index(request):
    all_puzzle_chart = get_all_puzzle_user_day()    
    delta_puzzle_chart = get_delta_puzzle_user_day()
    puzzle_chart = get_puzzle_user_puzzle()
    return render_to_response('analyse.html', {'charts': [all_puzzle_chart, delta_puzzle_chart, puzzle_chart]})
        

