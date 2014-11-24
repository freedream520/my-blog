'''
Created on 2013-6-26

@author: zhangyang
'''
from django.views.decorators.http import require_GET
from trend.models import Trend
from common.request import Pageable
from django.template.response import SimpleTemplateResponse as resp

@require_GET
def home(request):
    page = Pageable(request, size = 6)
    trends = Trend.objects.query(page, request)
    return resp('home.html', locals())