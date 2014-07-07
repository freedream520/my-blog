from django.contrib.auth.models import User
import json
import types
# import sae
import ConfigParser
from mysite.settings import CONFIG_PATH

def get_or_create_usr(email, usrname):
    back = []
    if email and usrname:
        back = User.objects.get_or_create( email=email
                                          , first_name = usrname
                                          , defaults = {'password':'123456'} )
    else:
        raise Exception('usrname and email can\'t be empty!')
    return back[0]

def sae_save_file( f , storage_name , file_name = None ):
    from sae.storage import Bucket
    bucket = Bucket(storage_name)
    print bucket
    if file_name is None: 
        file_name = f._get_name()
    return bucket.put_object(file_name, f)

def get_config_map(file_name, object_name):
    back = {}
    cp = ConfigParser.ConfigParser()
    with open(CONFIG_PATH + file_name,'r') as cfgFile:
        cp.readfp(cfgFile)
        items = cp.items(object_name)
        for item in items : back[item[0]] = item[1]
    return back