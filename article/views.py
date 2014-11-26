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
from django.http import HttpResponse
from django.utils import simplejson

import re

## 提取文章中的图片做插图显示
thumnailPattern = re.compile(r'<img src="?(\S+(.png|.jpg|.jpeg|.gif))".+>', re.IGNORECASE)

## === Article ===
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
    return resp('article-list.html', locals())

@require_GET
def showArticle( request, aid ):
    article = Article.objects.get(id=aid)
    tags = Tag.objects.raw('SELECT at.tag_id AS id, t.name AS name, COUNT(at.tag_id) AS articleNum FROM mb_articles_tags AS at, mb_tags AS t WHERE at.tag_id = t.id GROUP BY at.tag_id')
    return resp('post.html', locals())

@login_required
@require_POST
def saveArticle( request ):
    article = Article.saveArticle(request.POST.get('articleId', None)
                              , request.POST['markdown']
                              , request.POST['content']
                              , request.POST.get('tags', None) )
    data = {
        'status' : True,
        'data' : {
            'article' : {
                'id' : article.id,
                'name' : article.name,
                'created_at' : article.created_at
            }
        }
    }
    # return HttpResponse(simplejson.dumps(data), mimetype='application/json')
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


## === Comment ===
# @require_GET
# def showFeeds( request, aId ):
#     article = Article.objects.get(id = aId)
#     return resp('article-feed.html', locals())
#
# @require_POST
# def saveComment( request ):
#     email = request.POST['email']
#     usrname = request.POST['usrname']
#     content = request.POST['content']
#     article = Article.objects.get(id = request.POST['aId'])
#
#
#     kwarg = {'user' : util.get_or_create_usr(email, usrname),'content' : content}
#
#     desc = request.POST.get('memo', None)
#     if desc : kwarg['desc'] = desc
#
#     rootId = request.POST.get('rootId', None)
#     if rootId : kwarg['root_komment'] = Comment.objects.get(id = rootId)
#
#     kommentId = request.POST.get('cId', None)
#     if content.strip().count('#-') is 1 and kommentId:
#         pattern = re.compile('(#-).*(-#\s*)')
#         content = pattern.sub('', content)
#         komment = Comment.objects.get(id = kommentId)
#
#         kwarg['content'] = content
#         kwarg['komment'] = komment
#     else:
#         kwarg['article'] = article
#
#     comment = Comment(**kwarg)
#     comment.save()
#
#     resp = HttpResponseRedirect('/article/'+str(article.id)+'/feeds#comment-'+str(comment.id))
#     ## if not request.COOKIES.has_key('email') or not request.COOKIES.has_key('usrname'):
#     resp.set_cookie('email', value = email, max_age = 31536000, httponly = True)
#     resp.set_cookie('usrname', value = usrname.encode('utf-8'), max_age = 31536000, httponly = True)
#
#     return resp
#
# @require_GET
# def deleteComment( request ):
#     comment = Comment.objects.get(id=request.GET['id'])
#     articleId = comment.article.id
#     comment.delete()
#     return redirect('/article/'+articleId)


##=== Tag ===
# @require_GET
# def queryTags( request ):
#     back = Tag.objects.query( request = request )
#     return HttpResponse( serializers.serialize('json', back) )