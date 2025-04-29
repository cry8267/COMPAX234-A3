#tuple_space.py
#This file defines a basic TupleSpace class 
#It have 3 operations:read,read and delete,insert
import threading
class TupleSpace:
    def __init__(self):
        self.data = {}
        self.lock = threading.Lock()

#read the value without deleting it
    def read(self,key):
        with self.lock:
            if key in self.data:
                return True,self.data[key]
            else:
                return False,None #not found the key

     #read and remove the key-value pair       
    def get(self,key):
        with self.lock:
            if key in self.data:
                v = self.data[key]
                del self.data[key] #delete after reading
                return True,v
            else:
                return False,None #key not there

     #input a new key-value pair       
    def put(self,key,value):
        with self.lock:
            if key not in self.data:
                self.data[key]=value
                return True
            else:
                return False #key already exists
            


