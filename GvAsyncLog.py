#from loguru import logger
from loguru._logger import Logger
import sys
import threading
import warnings
from collections import namedtuple
from inspect import isclass
from multiprocessing import current_process
from os.path import basename, splitext
from threading import current_thread

from loguru._ansimarkup import AnsiMarkup
from loguru._better_exceptions import ExceptionFormatter
from loguru._datetime import aware_now
from loguru._file_sink import FileSink
from loguru._get_frame import get_frame
from loguru._handler import Handler
from loguru._recattrs import ExceptionRecattr, FileRecattr, LevelRecattr, ProcessRecattr, ThreadRecattr
def single(cls):
    cls.instance = None
    def wrapper(*args,**kwargs):
        if not cls.instance:
            cls.instance = cls(*args,**kwargs)
        return cls.instance
    return wrapper

@single
class AsyncLog(Logger):
    def __init__(self, exception=None, depth=0, record=False, lazy=False, ansi=False, raw=False, patcher=None, extra={}):
        Logger.__init__(self, exception, depth, record, lazy, ansi, raw, patcher, extra)
        self.fileFilter = {}
    
    def _Log(self,level_id, FileID, message, args, kwargs):
        if not Logger._handlers:
            return
        (exception, depth, record, lazy, ansi, raw, patcher, extra) = self._options
        from_decorator = False
        name = None
        try:
            level_no, _, level_icon = Logger._levels[level_id]
            level_name = level_id
        except KeyError:
                raise ValueError("Level '%s' does not exist" % level_id)
                
        thread = current_thread()
        process = current_process()
        level_recattr = LevelRecattr(level_name)
        level_recattr.no, level_recattr.name, level_recattr.icon = (
            level_no,
            level_name,
            level_icon,
        )
        thread_ident = thread.ident
        thread_recattr = ThreadRecattr(thread_ident)
        thread_recattr.id, thread_recattr.name = thread_ident, thread.name

        process_ident = process.ident
        process_recattr = ProcessRecattr(process_ident)
        process_recattr.id, process_recattr.name = process_ident, process.name
        exception = None
        current_datetime = aware_now()
        log_record = {
            "exception": None,
            "extra": {**Logger._extra_class, **extra},
            "function": "",
            "level": level_recattr,
            "line": 0,
            "message": message,
            "name": name,
            "process": process_recattr,
            "thread": thread_recattr,
            "time": current_datetime,
        }
        if args or kwargs:
            log_record["message"] = message.format(*args, **kwargs)
        if None != Logger._handlers.get(FileID):
            Logger._handlers[FileID].emit(log_record, level_id, from_decorator, ansi, raw)
        else:
            raise ValueError("handler{} is not exist '%s' does not exist".format(FileID))
        
    def GetFilterID(self,file):
        FileID=0
        Logger._lock.acquire()
        bExit = False
        handlers = Logger._handlers.copy()
        for handler in handlers.values():
            if handler._name == file:
                FileID = handler._id
                bExit  = True
                break
        Logger._lock.release()
        if bExit == False:
            FileID = self.add(file,rotation="00:00",format="{time:YYYY-MM-DD HH:mm:ss:SSS} - {message}",retention="1 month",enqueue=True)
        return FileID
        
    def Log(self, file,_message, *args, **kwargs):
        FileID=0
        FileID = self.GetFilterID(file)
        self._Log("INFO", FileID, _message, args, kwargs)    
        #self._log("INFO", None, False, self._options, _message, args, kwargs)
        
GvLog = AsyncLog()