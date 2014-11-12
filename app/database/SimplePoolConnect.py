
__author__ = 'renatomoitinhodias'

import threading,random,time,mysql.connector


'''
    thread consumer test pool
'''
class Repository(threading.Thread):
    def __init__(self, threadName,connection):
        threading.Thread.__init__( self, name=threadName)
        self.connection = connection

    def __resetConnections(self):

       try:
          self.connection.reconnect()
          return True
       except Exception:pass

       return False

    def run(self):


        current_milli_time = lambda t: int(round(t * 1000))

        for i in range(20):

           start = time.time()

           cursor = None
           try:

               cursor = self.connection.cursor()
               cursor.execute(" select * from example ")
               size_result = len(cursor.fetchall())

               print "%i -> thread[%s] result query length (%i) in %i mls " % \
                     ( i, threading.Thread.getName(self) , size_result, current_milli_time(time.time()-start) )

           except Exception as e:
               print "thread[%s] result error in %s " %\
                     (  threading.Thread.getName(self) , e.message )

           if cursor is None:
               attempts =1
               while not self.__resetConnections():
                  print "thread[%s] attempts (%i) waiting... reconnect database =/ " %\
                        (threading.Thread.getName(self) ,attempts)
                  attempts+=1
                  time.sleep( 3 )

               continue
           else:
               cursor.close()

#                  self.event.wait()


           time.sleep( random.randrange(5) )




current_milli_time = (lambda t: int(round(t * 1000)))

if __name__ == '__main__':

    CONFIG_POOL = {
        'pool_name':"simple-pool",
        'pool_size':10,
        'autocommit':True,
        'user':"root",
        'password':"",
        'host':"127.0.0.1",
        'database':'test'
    }


    pool = mysql.connector.pooling.MySQLConnectionPool(**CONFIG_POOL)

    def getConnection():
        global pool
        return pool.get_connection()


    def mock_database():

      conn = getConnection()

      for i in range(10):

        start = time.time()

        try:

          cursor = conn.cursor()

          select_stmt = "SELECT * FROM example limit %(emp_no)s"
          cursor.execute(select_stmt, { 'emp_no': 2 })
#          cursor.execute(" select * from example limit %(limit)i", {'limit': 10 })
          size_result = len(cursor.fetchall())

          print "%i -> thread[%s] result query length (%i) in %i mls " %\
                ( i, threading.currentThread().getName() , size_result, current_milli_time(time.time()-start) )

        except Exception as e:
          print "thread[%s] result error in %s " %\
                (  threading.currentThread().getName() , e.message )

        time.sleep( random.randrange(5) )



    threading.Thread(target=mock_database).start()

#    conn = pool._cnx_queue.get_nowait()
#    print dir(conn)
#    print help(conn)

#    i = 0
#    while i < 11:

#       threading.Thread(target=mock_database).start()
#       i+=1
#       time.sleep( 10 )

#    print "remove connections"
#    pool._remove_connections()
#    time.sleep( 10 )
#    print "reset connections"
#    pool.add_connection()
#    time.sleep( 10 )















