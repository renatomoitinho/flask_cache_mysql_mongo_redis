# -*- coding: utf-8 -*-
import threading

__author__ = 'renatomoitinhodias'

#from app.database import Struct

from collections import deque
from bson import ObjectId
from flask import Flask, render_template, request
from flask import jsonify
from flask.ext.cache import Cache

from mongokit.connection import Connection
from app.mongo.scheme.User import User
import os,json,time
import mysql.connector




class APIEncoder(json.JSONEncoder):
    def default(self,obj):
        if isinstance(obj,ObjectId):
            return str(obj)
        return json.JSONEncoder.default(self,obj)


def toJSON(data):
     return json.dumps(data,cls=APIEncoder)

# configuration
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017

app = Flask(__name__)
app.config.from_object(__name__)

cache = Cache(app, config={
    "CACHE_TYPE" : "redis",
    "CACHE_REDIS_HOST": "127.0.0.1",
    "CACHE_REDIS_PORT": 6379,
    "CACHE_REDIS_DB": 0

})


#register others controller
#app.register_blueprint(account_api)

path = os.path.dirname(os.path.abspath(__file__))


# connect to the database
connection = Connection(app.config['MONGODB_HOST'],app.config['MONGODB_PORT'])


#registre schemes

connection.register([User])

collection = connection['test'].users


CONFIG_POOL = {
    'pool_name':"simple-pool",
    'pool_size':10,
    'autocommit':True,
    'user':"root",
    'password':"",
    'host':"127.0.0.1",
    'database':'test'
}

context = {}

current_milli_time = (lambda t: int(round(t * 1000)))


def show_log(func):
    def wrapper(*args, **kwargs):
        start = time.time()

        try:
            return func(*args,**kwargs)
        finally:
            global context,current_milli_time

            if not func.__name__ in context:
                context[func.__name__] = 0

            print "nº (%i) / time request (%i) mls" % ( context[func.__name__],current_milli_time(time.time() - start))
            context[func.__name__]+=1

    return wrapper


@app.before_request
def before_request():
    if '/static/' in request.path:
      return None


@app.route('/login')
def index():
    return render_template("auth/login.html")


@show_log
@cache.memoize()
def accountList(limit):

    try:
        query = "select * from example limit %(p_1)s",{'p_1': int(limit)}
        return json.dumps( map(lambda a: dict(zip(['uid','name'], a)), open_cursor(query) ))

    except Exception as e:
        return jsonify(error=e.message)

@show_log
@cache.cached(timeout=50)
def lists():

    return toJSON(list(collection.User.find()))

@app.route('/list')
def mock_mongodb():
    return lists()

@app.route("/dict/<limit>")
def mockMysql(limit):
    return accountList(limit)

def get_pooled():
    """Opens a new database connection if there is none yet for the
    current application context.
    """

    if not 'mysql_db' in context:
        connections = deque()
        pool = mysql.connector.pooling.MySQLConnectionPool(**CONFIG_POOL)
        for i in range(pool.pool_size):
            connections.append( pool.get_connection() )

        context['pool'] = pool
        context['mysql_db'] = connections

        print "not hash open pool"

    return context['mysql_db']

def reset_pooled():
    try:
      for conn in get_pooled(): conn.reconnect()
    except Exception : pass

def open_cursor(query=(),n=0):

    connections = get_pooled()
    current = connections.pop()

    cursor = None
    try:
        cursor = current.cursor()
        cursor.execute(query[0],query[1])

        return cursor.fetchall()

    except: pass
    finally:

        connections.appendleft(current)

        if cursor is not None:
           cursor.close()
        else:
           n+=1
           reset_pooled()
           if n == 5:
            raise Exception("database not connected, try again =[ attempts(%i)" % n )

           return open_cursor(query,n)

@app.route("/clear")
def clear():

    context['accountList'] = 0
    context['lists']=0
    return "clear ok !!"





if __name__ == '__main__':


    class Test_db(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)

        def run(self):
            while 1:
                try:
                   open_cursor("select 1")
                except Exception as e:
                    print "database is not connect try connection ... / %s" % e.message

                time.sleep(10)


#    Test_db().start()
    app.run(debug=False)
