from threading import Lock,Thread
import threading
import time
__author__ = 'renatomoitinhodias'




class User:
    def __init__(self, name=None,age=None):
        self.name = name
        self.age= age
        self.__var = None

    def __repr__(self):
        return "[name = %s , age = %s]" % ( str(self.name), str(self.age))

    def __print(self):
        print "[name = %s , age = %s]" % ( str(self.name), str(self.age))


    def getProperty(self):
        return self.__var

    def setProperty(self, n):
        self.__var =  n/2



class C(object):
    def __init__(self, x=0):
        self.__x = x

    def getx(self):
        return self.__x

    def setx(self, x):
      if x < 0: x = 0
      self.__x = x

    x = property(getx, setx)


class Sample(Thread):

    def __init__(self, condition):
        Thread.__init__(self)
        self.condition = condition

    def run(self):
        print "sleep wait ZZZZ"

        self.condition.wait()

        print "acordei"



class Cont(Thread):

    def __init__(self, condition):
        Thread.__init__(self)
        self.condition = condition

    def run(self):
        for i in range(1,5):
          time.sleep(1)
          print i

        self.condition.set()
        self.condition.clear()





condition = threading.Condition()
event = threading.Event()

#print dir(condition)
#print help(condition)

condition.acquire()

Sample(event).start()
Cont(event).start()



