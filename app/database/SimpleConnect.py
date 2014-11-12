from app.database import Struct, schemas

__author__ = 'renatomoitinhodias'


'''
    pip install MySQL-python
'''

import MySQLdb


class Database:

    connection = None

    @staticmethod
    def connect():
        if Database.connection is None:
            Database.connection = MySQLdb.connect(user="root",host="127.0.0.1", port=3306)

    @staticmethod
    def session():
        if Database.connection is not None:
            return Database.connection.cursor()

    @staticmethod
    def close():
        if Database.connection is not None:
            Database.connection.close()

    @staticmethod
    def reconnect():
        Database.close()
        Database.connection = None
        Database.reconnect()



class MySQLConnect:
    def __init__(self):
        try:
            Database.connect()
            self.con = Database.connection
            print "you are connect! "
        except ValueError:
            print "error connect database"

    def close(self):
        self.con.close()

    def execute(self, query):
        cur = self.con.cursor()
        try:
            cur.execute(query)
        finally:
            cur.close()

    def query(self,scheme,query):

        list=[]
        cur = self.con.cursor()

        try:
            obj = Struct(**scheme)
            cur.execute(query)
            for line in cur.fetchall():
                list.append(Struct(**dict(zip(obj.columns, line)) ))

            return list
        except( ValueError, MySQLdb.OperationalError):
            Database.reconnect()
            return self.query(scheme,query)
        finally:
            cur.close()

class ExampleRepository(MySQLConnect):

    scheme = Struct(**schemas)

    def __init__(self):
        MySQLConnect.__init__(self)
        self.execute("use test")

    def all(self):
        return  self.query(self.scheme.example, "select * from example")
