'''
Created on 2013-6-23

@author: ray
'''

from django.conf.urls import patterns, url, include
from mysite import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes':True}),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes':True}),
    
    url(r'^$', 'article.views.showArticleList'),
    url(r'^article/', include('article.urls')),
    url(r'^tag/query', 'article.views.queryTags'),
    url(r'^editor/', 'article.views.editArticle'),
    
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
        
