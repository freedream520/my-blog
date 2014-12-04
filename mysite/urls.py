'''
Created on 2013-6-23

@author: ray
'''

from django.conf.urls import patterns, url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'article.views.showArticleList'),
    url(r'^article/', include('article.urls')),
    url(r'^edit/', 'article.views.editArticle'),
    url(r'^feed/', 'article.views.feed'),
    
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
