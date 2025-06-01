import sys
import time
import datetime
import threading
import GvVisionAssembly
from ScFile import ScFile
from GvAsyncLog import GvLog

class ScMsgReport:
    #用于日志记录的时间格式
    def GetstrCurTimeMS(self):
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')

    # 用于日志记录的时间格式
    def GetstrCurTimeS(self):
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def GetstrCurTimeD(self):
        return datetime.datetime.now().strftime('%Y-%m-%d')

    def GetstrCurTimeM(self):
        return datetime.datetime.now().strftime('%Y-%m')

    def GetstrCurTimeY(self):
        return datetime.datetime.now().strftime('%Y')

    def __writefile(self, LocalLogPath, strCon):
        # 存储
        try:
            with open(LocalLogPath, 'a') as f:
                f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f->\t') + strCon + "\n")
        finally:
            pass



    #记录日志 #可以把日志记录在指定的文件夹路径下面，下面的指定文件名
    #filePath 路径名称，文件存储在这个文件夹下面的日期文件夹（自动建）
    #filename 日志文件路径，没有则新建，默认 日期当天.txt
    #cmdWrite 日志文件内容。默认 hello
    @staticmethod
    def RecordMsgDate(filePath, filename="Null.txt", cmdWrite="Hello"):
        # 将收到的内容写入Log
        path = ScFile.mkdirDate(filePath)

        #print(path)
        if filename=="Null.txt":
            filename = time.strftime("%m%d.txt")
            #print(filename)

        # 创建一个带参数的线程对象
        thread = threading.Thread(target=ScMsgReport.__writefile, args=(ScMsgReport, path + "\\" + filename, cmdWrite))
        thread.start()

    #记录日志 #可以把日志记录在指定的文件夹路径下面，下面的指定文件名
    #filePath 路径名称
    #filename 日志文件路径，没有则新建，日期当天.txt
    #cmdWrite 日志文件内容。默认 hello
    @staticmethod
    def RecordMsgFolder(filePath, filename="Null.txt", cmdWrite="Hello"):
        # 将收到的内容写入Log
        path = ScFile.mkdirFolder(filePath)

        #print(path)
        if filename=="Null.txt":
            filename = time.strftime("%m%d.txt")
            #print(filename)
        thread = threading.Thread(target=ScMsgReport.__writefile, args=(ScMsgReport, path + "\\" + filename, cmdWrite))
        thread.start()

    #记录日志 #可以把日志记录在指定的文件夹路径下面，下面的指定文件名，日志名称自动指定为 日期当天.txt
    #filePath 路径名称
    #cmdWrite 日志文件内容。默认 hello
    @staticmethod
    def RecordAutoLog(filePath, cmdWrite="Hello"):
        # 将收到的内容写入Log
        path = ScFile.mkdirFolder(filePath)
        filename = time.strftime("%m%d.txt")

        thread = threading.Thread(target=ScMsgReport.__writefile, args=(ScMsgReport,path + "\\" + filename, cmdWrite))
        thread.start()

    #记录日志 #可以把日志记录在指定的文件夹路径下面，下面的指定文件名，日志名称自动指定为 日期当天.txt
    #filePath 路径名称
    #cmdWrite 日志文件内容。默认 hello
    @staticmethod
    def RecordAutoPathLog(cmdWrite="Hello",filePath="D:\\LusterCache\\log",file="Null",bMessage=True,bEnable=True):
        #filePath="D:\\LusterCache\\log"
        # 将收到的内容写入Log
        path = ScFile.mkdirFolder(filePath)
        if file=="Null":
            filename = time.strftime("%m%d.txt")
        else:
            filename = time.strftime(file+"-%m%d.txt")

        thread = threading.Thread(target=ScMsgReport.__writefile, args=(ScMsgReport, path + "\\" + filename, cmdWrite))
        thread.start()
        if bMessage:
            Genote = GvVisionAssembly.GeMsgReportType
            GvVisionAssembly.ReportMessage(cmdWrite, Genote.eMRTNote,False)


    #报告提示消息
    def ReportMsg(cmdMsg="Hello",bPumpOut=True):
        # 将收到的内容写入Log
        # 在提示中提示收到的信息
        Genote = GvVisionAssembly.GeMsgReportType
        noteType = Genote.eMRTNote
        GvVisionAssembly.ReportMessage(cmdMsg, noteType, bPumpOut)

    #报告警告
    def ReportMsgWarn(cmdMsg="Hello",bPumpOut=True):
        # 将收到的内容写入Log
        # 在提示中提示收到的信息
        Genote = GvVisionAssembly.GeMsgReportType
        noteType = Genote.eMRTWarning
        GvVisionAssembly.ReportMessage(cmdMsg, noteType, bPumpOut)

    #报告错误提示
    def ReportMsgError(cmdMsg="Hello",bPumpOut=True):
        # 将收到的内容写入Log
        # 在提示中提示收到的信息
        Genote = GvVisionAssembly.GeMsgReportType
        noteType = Genote.eMRTError
        GvVisionAssembly.ReportMessage(cmdMsg, noteType, bPumpOut)

    #报告弹出提示
    def ReportMsgPop(cmdMsg="Hello", bPumpOut=True):
        # 将收到的内容写入Log
        # 在提示中提示收到的信息
        Genote = GvVisionAssembly.GeMsgReportType
        noteType = Genote.eMRTPopupNote
        GvVisionAssembly.ReportMessage(cmdMsg, noteType, bPumpOut)

    #报告自定义提示框，带返回值
    def ReportMsgOption(cmdMsg="Hello", bPumpOut=True):
        # 将收到的内容写入Log
        # 在提示中提示收到的信息
        Genote = GvVisionAssembly.GeMsgReportType
        noteType = Genote.eMRTResultOption
        ans = GvVisionAssembly.ReportMessage(cmdMsg, noteType, bPumpOut)
        return ans