__author__ = 'renatomoitinhodias'

from flask import Blueprint,_app_ctx_stack
import mysql.connector
import json


account_api = Blueprint('data_api', __name__)

CONFIG_POOL = {
    'pool_name':"simple-pool",
    'pool_size':10,
    'autocommit':True,
    'user':"root",
    'password':"",
    'host':"127.0.0.1",
    'database':'test'
}


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    top = _app_ctx_stack.top
    if not hasattr(top, 'pool'):
        top.pool = mysql.connector.pooling.MySQLConnectionPool(**CONFIG_POOL)
        top.mysql_db = top.pool.get_connection()
        print "not hash open pool"
    return top.mysql_db




@account_api.route("/dataAPI")
def accountList():
    cursor = get_db().cursor()
    cursor.execute(" select * from example ")
    try:
        return json.dumps( map(lambda a: dict(zip(['uid','name'], a)), cursor.fetchall()) )
    finally:
        cursor.close()


