'''
Created on 2013-6-26

@author: zhangyang
'''

from django.db import models

class BaseMgr(models.Manager):
    def query(self, pagin=None, request=None):
        kwgs = self.getDict(request)
        if pagin is not None:
            pagin.count = self.filter(id__gte=1, enabled=True, **kwgs).count()
            start = (pagin.page - 1) * pagin.size
            end = (pagin.page - 1) * pagin.size + pagin.size
            return self.filter(id__gte=1, enabled=True, **kwgs).all()[start : end]
        else:
            return self.filter(id__gte=1, enabled=True, **kwgs).all()
        
#    def remove(self, oid):
#        self.get( id=oid ).delete()
    
    def save(self, request, adkwg = None , rmlist = None):
        kwgs = self.getDict(request, rmlist)
        if adkwg is not None: 
            kwgs.update(adkwg)
        if kwgs.has_key('id'):
            mid = kwgs.pop('id')
            self.filter(id=mid).update(**kwgs)
            back = self.get(id=mid)
        else:
            back = self.create(**kwgs)
        return back
            
        
    def getDict(self, request = None, rmlist = None):
        back = {}
        if request is not None:
            back = request.GET.dict()
            back.update(request.POST.dict())
            try:
                if rmlist is not None : map(lambda s:back.pop(s), rmlist)
                if back.has_key("page.size"):
                    back.pop("page.size")
                    back.pop("page.page")
                if back.has_key("csrfmiddlewaretoken"):
                    back.pop("csrfmiddlewaretoken")
            except KeyError:
                pass    
        for k in back.keys():
            if back.get(k).encode('utf-8').strip() == '':
                back.pop(k)
        return back

class BaseModel(models.Model):
    id = models.AutoField( primary_key = True )
    name = models.CharField( max_length = 32 , null = True )
    desc = models.CharField( max_length = 256 , null = True )
    create_at = models.DateTimeField( auto_now_add = True , auto_now = False )
    last_at = models.DateTimeField( auto_now = True )
    enabled = models.BooleanField( default = True )
    
    class Meta:
        abstract = True
        
    objects = BaseMgr()