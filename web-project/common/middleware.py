'''
Created on 2013-6-23

@author: ray
'''
from django.template.response import TemplateResponse
from django.template.context import RequestContext
from django.template import loader
from django.http import HttpResponse
class RequestContextMiddleware(object):
    def process_template_response(self, request, response):
        ctx = RequestContext(request, response.context_data)
        return TemplateResponse(request, response.template_name, ctx)

class CloseSiteMiddleware(object):
    def process_response(self, request, response):
        c = RequestContext(request, {})
        t = loader.get_template("temp/comming.html")
        return HttpResponse(t.render(c))

def globalVar(request):
    config = {
        "SITE_URL" : "http://lpgray.sinaapp.com"
    }
    return config;
