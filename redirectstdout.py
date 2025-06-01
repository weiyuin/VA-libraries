import sys
import ctypes
import io
from threading import Lock
lock = Lock()


global dllFunprint
global myRedirect


class __redirection__(io.TextIOBase):
    def __init__(self):
        self.buff=''
        self.__console__=sys.stdout
        
    def write(self, output_stream):
        global dllFunprint
        with lock:
            self.buff = output_stream
            if type(self.buff).__name__ == 'str':
                self.buff = self.buff.encode('utf-8')
            dllFunprint(self.buff)

    def reset(self):
        sys.stdout = self.__console__
        
def redirectPrint():
    global dllFunprint
    global myRedirect
    dll = ctypes.cdll.LoadLibrary("RedirectPythonPrint.dll")
    dllFunprint = dll.pyPrint
    dllFunprint.argtypes = [ctypes.c_char_p]
    myRedirect  = __redirection__()
    sys.stdout = myRedirect

def resetPrint():
    sys.stdout = myRedirect.__console__