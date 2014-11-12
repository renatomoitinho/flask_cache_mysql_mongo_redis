__author__ = 'renatomoitinhodias'
import json, datetime
from mongokit import *

class APIEncoder(json.JSONEncoder):
    def default(self,obj):
        if isinstance(obj, datetime):
            return obj.strftime("%d/%m/%y %H:%S")
        elif isinstance(obj,ObjectId):
            return str(obj)
        return json.JSONEncoder.default(self,obj)


def ok(data):
    return json.dumps(data,cls=APIEncoder)
