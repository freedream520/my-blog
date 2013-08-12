#coding=utf-8
'''
Created on 2013-6-23

@author: ray
'''

from article.models import Article, Comment, Tag
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.core import serializers
from django.contrib.auth.decorators import login_required
from common.request import Pageable
from django.views.decorators.http import require_POST, require_GET
import util
from django.template.response import SimpleTemplateResponse as resp
import re

## === Article ===
@require_GET
def showArticleList( request ):
    page = Pageable(request)
    articles = Article.objects.query(page, request)
    map(lambda a:a.setCommentNum(a.comment_set.count()), articles)
    tags = Tag.objects.raw('SELECT at.tag_id AS id, t.name AS name, COUNT(at.tag_id) AS articleNum FROM ms_articles_tags AS at, ms_tags AS t WHERE at.tag_id = t.id GROUP BY at.tag_id')
    return resp('article-list.html', locals())

@require_GET
def showArticle( request, aid ):
    article = Article.objects.get(id=aid)
    tags = article.tags.all()
    map(lambda t:t.setArticleNum(t.article_set.count()), tags)
    return resp('article.html', locals())

@require_GET
def aboutMe( request ):
    article = Article.objects.get(id=0)
    return resp('about.html', locals())

@login_required
@require_POST
def saveArticle( request ):
    imgs = None
    if request.FILES.has_key('imgs'):
        imgs = request.FILES.getlist('imgs')
    article = Article.saveArticle(request.POST.get('id', None)
                              , request.POST['title']
                              , request.POST['desc']
                              , request.POST['tags']
                              , request.POST['content']
                              , imgs )
    if article.id == 0:
        return redirect('/about')
    return redirect('/article/' + str( article.id ))

@login_required
@require_GET
def removeArticle( request ):
    Article.objects.filter(**request.GET.dict()).delete()
    return redirect('/article/query')

@login_required
@require_GET
def editArticle( request ):
    try:
        article = Article.objects.get(id = request.GET['id'])
    except:
        article = None
    locals().update(csrf(request))
    return resp('editor.html', locals())


## === Comment ===
@require_GET
def showFeeds( request ):
    article = Article.objects.get(id = request.GET['aId'])
    return resp('article-feed.html', locals())

@require_POST
def saveComment( request ):
    email = request.POST['email']
    usrname = request.POST['usrname']
    content = request.POST['content']
    article = Article.objects.get(id = request.POST['aId'])
    
    
    kwarg = {'user' : util.get_or_create_usr(email, usrname),'content' : content}
    
    desc = request.POST.get('memo', None)
    if desc : kwarg['desc'] = desc
    
    rootId = request.POST.get('rootId', None)
    if rootId : kwarg['root_komment'] = Comment.objects.get(id = rootId)
    
    kommentId = request.POST.get('cId', None)
    if content.strip().count('#-') is 1 and kommentId:
        pattern = re.compile('(#-).*(-#\s*)')
        content = pattern.sub('', content)
        komment = Comment.objects.get(id = kommentId)
        
        kwarg['content'] = content
        kwarg['komment'] = komment         
    else:
        kwarg['article'] = article
        
    comment = Comment(**kwarg)
    comment.save()
    
    resp = HttpResponseRedirect('/article/feeds?aId='+str(article.id)+'#comment-'+str(comment.id))
    ## if not request.COOKIES.has_key('email') or not request.COOKIES.has_key('usrname'):
    resp.set_cookie('email', value = email, max_age = 31536000, httponly = True)
    resp.set_cookie('usrname', value = usrname.encode('utf-8'), max_age = 31536000, httponly = True)
    
    return resp

@require_GET
def deleteComment( request ):
    comment = Comment.objects.get(id=request.GET['id'])
    articleId = comment.article.id
    comment.delete()
    return redirect('/article/'+articleId)


##=== Tag ===
@require_GET
def queryTags( request ):
    back = Tag.objects.query( request = request )
    return HttpResponse( serializers.serialize('json', back) )