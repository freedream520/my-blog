#coding=utf-8
'''
Created on 2013-6-26

@author: zhangyang
'''

from django.contrib.admin.models import User
from common.models import BaseModel
from django.db import models
# from mysite.settings import MEDIA_URL
# import uuid

# def sae_save_file( f , storage_name , file_name = None ):
#     from sae.storage import Bucket
#     bucket = Bucket(storage_name)
#     print bucket
#     if file_name is None:
#         file_name = f._get_name()
#     return bucket.put_object(file_name, f)

class Tag( BaseModel ):
    class Meta:
        db_table = 'mb_tags'

    articleNum = 0
    
    def setArticleNum(self, num):
        self.articleNum = num
        
    def __unicode__(self):
        return self.name
   
class Article( BaseModel ):
    class Meta:
        db_table = 'mb_articles'
        ordering = ['-created_at']
    
    user = models.ForeignKey( User, null=True )
    content = models.TextField( null = False )
    markdown = models.TextField( null = False )
    tags = models.ManyToManyField( Tag )

    thumnail = None
    displayTags = None

    @classmethod
    def saveArticle(cls, articleId, markdown, content, tags):
        if tags:
            stags = tags.strip().lstrip().rstrip().split()
            tags = [Tag.objects.get_or_create(name = tag.lower().strip().lstrip().rstrip())[0] for tag in stags]

        name = article_title(markdown)
        kwarg = {'name':name, 'markdown':markdown, 'content': content}
        if articleId:
            article = cls.objects.get(id = articleId)
            article.name = name
            article.tags = tags
            article.markdown = markdown
            article.content = content
        else:
            article = cls(**kwarg)
            article.save()
            article.tags = tags
            
        article.save()
        
        return article
    
    # def saveFile(self, img, newname):
    #     if newname is None:
    #         newname = img._get_name()
    #     sae_save_file(img, 'media', newname)
    #     self.temp_imgs.append( newname )
    #     return [img._get_name(), newname]
    
    # def changeContent(self, content, names):
    #     find = '##' + names[0] + '##'
    #     path = MEDIA_URL + '' + names[1]
    #     will = '<img src="' + path + '" />'
    #     return content.replace(find, will)

import re

titlePattern = re.compile(r'#.*')

def article_title (articleMarkdown):
    match = titlePattern.match(articleMarkdown)
    if match:
        return match.group()[1:].strip()
    return None

# class Comment( BaseModel ):
#     class Meta:
#         db_table = 'ms_comments'
#
#     content = models.TextField( null=False )
#     user = models.ForeignKey( User, null=True )
#     article = models.ForeignKey( Article, null=True )
#     komment = models.ForeignKey( 'self', null=True, related_name = 'comment_id' )
#     root_komment = models.ForeignKey( 'self', null=True, related_name = 'root_comment_id' )
#
#     def getComments(self):
#         return Comment.objects.filter(root_komment_id = self.id)

#========== Signal Definition ==========
# from trend.models import Trend
#
# @receiver(post_save, sender = Article)
# def post_save_article(sender, **kwargs):
#     if kwargs['created']:
#         aTplStringMap = util.get_config_map('trend_tpl.ini', 'article')
#         article = kwargs['instance']
#         tags = article.temp_tags
#         imgs = article.temp_imgs
#
#         desc = None
#         if tags and len(tags):
#             desc = Template(aTplStringMap['desc']).render(Context({'tags' : tags}))
#
#         path = None
#         if len(imgs):
#             path = imgs[0]
#
#         Trend.objects.create(name = 'article created'
#                              , content = Template(aTplStringMap['content']).render(Context({'article':article}))
#                              , desc = desc
#                              , path = path)
#
# ## @receiver(post_save, sender = Comment)
# def post_save_comment(sender, **kwargs):
#     comment = kwargs['instance']
#     if kwargs['created'] and comment.article:
#         tplStringMap = util.get_config_map('trend_tpl.ini', 'comment')
#         content = Template(tplStringMap['content']).render(Context({'feed' : comment}))
#         desc = Template(tplStringMap['desc']).render(Context({'feed' : comment}))
#         Trend.objects.create(name = 'feed created', content = content, desc = desc)