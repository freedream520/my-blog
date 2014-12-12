#coding=utf-8
'''
Created on 2013-6-23

@author: ray
'''

from article.models import Article, Tag
from django.core.context_processors import csrf
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from common.request import Pageable
from django.views.decorators.http import require_POST, require_GET
from django.template.response import SimpleTemplateResponse as resp
from django.template import Context, Template
from django.conf import settings
from django.http import HttpResponse

import re
import httplib
import json
import datetime

## 提取文章中的图片做插图显示
thumnailPattern = re.compile(r'<img src="?(\S+(.png|.jpg|.jpeg|.gif))".+>', re.IGNORECASE)

## 查询我的github个人信息
class GithubQuery():

    ## 上一次成功获取的时间
    lastTimeFetchedGithub = None
    ## 上一次获取的ETag
    etag = None
    ## 与github信息缓存
    myGithubInfo = None

    def queryMyGithub(self):
        conn = httplib.HTTPSConnection(host = 'api.github.com')

        if self.etag is not None:
            if self.lastTimeFetchedGithub is not None and self.myGithubInfo is not None:
                delta = datetime.timedelta(minutes = 20)
                now = datetime.datetime.now()
                if now - self.lastTimeFetchedGithub < delta:
                    return self.myGithubInfo

            conn.request(method = 'GET', url = '/users/lpgray', headers = {'User-Agent' : 'lpgray', 'If-None-Match' : self.etag})
            resp = conn.getresponse()
            self.etag = resp.getheader('ETag')
            if resp.status is 304:
                conn.close()
                return self.myGithubInfo
            else:
                self.myGithubInfo = json.loads(resp.read())
                conn.close()
                return self.myGithubInfo
        else:
            conn.request(method = 'GET', url = '/users/lpgray', headers = {'User-Agent' : 'lpgray'})
            resp = conn.getresponse()
            if resp.status is 200:
                self.etag = resp.getheader('ETag')
                self.myGithubInfo = json.loads(resp.read())
                self.lastTimeFetchedGithub = datetime.datetime.now()
                conn.close()
                return self.myGithubInfo
            else:
                file = open(settings.PROJECT_PATH + '/github_profile.json')
                self.myGithubInfo = json.loads(file.read())
                file.close()
                conn.close()
                return self.myGithubInfo

githubQuery = GithubQuery()

@require_GET
def showArticleList( request ):
    page = Pageable(request)
    articles = Article.objects.query(page, request)
    # 提取文章中的图片用于列表中的插图显示
    for article in articles:
        imgSrcs = re.findall(thumnailPattern, article.content)
        if imgSrcs and len(imgSrcs) > 0:
            article.thumnail = imgSrcs[0][0]

    tags = Tag.objects.raw('SELECT at.tag_id AS id, t.name AS name, COUNT(at.tag_id) AS articleNum FROM mb_articles_tags AS at, mb_tags AS t WHERE at.tag_id = t.id GROUP BY at.tag_id')
    githubInfo = githubQuery.queryMyGithub()
    return resp('article-list.html', locals())

@require_GET
def showArticle( request, aid ):
    article = Article.objects.get(id=aid)
    tags = Tag.objects.raw('SELECT at.tag_id AS id, t.name AS name, COUNT(at.tag_id) AS articleNum FROM mb_articles_tags AS at, mb_tags AS t WHERE at.tag_id = t.id GROUP BY at.tag_id')
    githubInfo = githubQuery.queryMyGithub()
    return resp('post.html', locals())

@require_GET
def feed( request ):
    page = Pageable(request)
    articles = Article.objects.query(page, request)
    datetime = articles[0].created_at

    file = open(settings.PROJECT_PATH + '/mysite/templates/rss.xml', 'r')
    content = file.read()
    file.close()

    template = Template(content)
    vars = Context({
        "articles" : articles,
        "datetime" : datetime
    })

    result = template.render(vars)
    response = HttpResponse(result)
    response["Content-Type"] = "application/rss+xml; charset=UTF-8"
    return response

@login_required
@require_POST
def saveArticle( request ):
    article = Article.saveArticle(request.POST.get('articleId', None)
                              , request.POST['markdown']
                              , request.POST['content']
                              , request.POST.get('tags', None) )
    return redirect('/article/' + str(article.id))

@login_required
@require_GET
def removeArticle( request ):
    Article.objects.filter(**request.GET.dict()).delete()
    return redirect('/article/query')

@login_required
@require_GET
def editArticle( request ):
    articleId = request.GET.get('id', None)
    article = None
    if articleId:
        article = Article.objects.get(id = articleId)
        article.displayTags = ''
        for tag in article.tags.all():
            article.displayTags += tag.name + '  '
    locals().update(csrf(request))
    return resp('editor.html', locals())