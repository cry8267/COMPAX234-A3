import threading
class TupleSpace:
    def __init__(self):
        self.data = {}
        self.lock = threading.Lock()

    def read(self,key):
        with self.lock:
            if key in self.data:
                return True,self.data[key]
            else:
                return False,None
            
    def get(self,key):
        with self.lock:
            if key in self.data:
                v = self.data[key]
                del self.data[key]
                return True,v
            else:
                return False,None


