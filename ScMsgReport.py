import sys
import time
import datetime
import threading
import GvVisionAssembly
from ScFile import ScFile
from GvAsyncLog import GvLog

class ScMsgReport:
    # Định dạng thời gian dùng để ghi log
    def GetstrCurTimeMS(self):
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')

    # Định dạng thời gian dùng để ghi log
    def GetstrCurTimeS(self):
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def GetstrCurTimeD(self):
        return datetime.datetime.now().strftime('%Y-%m-%d')

    def GetstrCurTimeM(self):
        return datetime.datetime.now().strftime('%Y-%m')

    def GetstrCurTimeY(self):
        return datetime.datetime.now().strftime('%Y')

    def __writefile(self, LocalLogPath, strCon):
        # Lưu trữ
        try:
            with open(LocalLogPath, 'a') as f:
                f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f->\t') + strCon + "\n")
        finally:
            pass

    # Ghi log # Có thể ghi log vào đường dẫn thư mục chỉ định, với tên file bên dưới
    # filePath: Tên đường dẫn, file được lưu trong thư mục ngày tháng bên dưới thư mục này (tự động tạo)
    # filename: Đường dẫn file log, nếu chưa có thì tạo mới, mặc định là Ngày_hiện_tại.txt
    # cmdWrite: Nội dung file log. Mặc định là hello
    @staticmethod
    def RecordMsgDate(filePath, filename="Null.txt", cmdWrite="Hello"):
        # Ghi nội dung nhận được vào Log
        path = ScFile.mkdirDate(filePath)

        #print(path)
        if filename=="Null.txt":
            filename = time.strftime("%m%d.txt")
            #print(filename)

        # Tạo một đối tượng luồng (thread) có tham số
        thread = threading.Thread(target=ScMsgReport.__writefile, args=(ScMsgReport, path + "\\" + filename, cmdWrite))
        thread.start()

    # Ghi log # Có thể ghi log vào đường dẫn thư mục chỉ định, với tên file bên dưới
    # filePath: Tên đường dẫn
    # filename: Đường dẫn file log, nếu chưa có thì tạo mới, mặc định là Ngày_hiện_tại.txt
    # cmdWrite: Nội dung file log. Mặc định là hello
    @staticmethod
    def RecordMsgFolder(filePath, filename="Null.txt", cmdWrite="Hello"):
        # Ghi nội dung nhận được vào Log
        path = ScFile.mkdirFolder(filePath)

        #print(path)
        if filename=="Null.txt":
            filename = time.strftime("%m%d.txt")
            #print(filename)
        thread = threading.Thread(target=ScMsgReport.__writefile, args=(ScMsgReport, path + "\\" + filename, cmdWrite))
        thread.start()

    # Ghi log # Có thể ghi log vào đường dẫn thư mục chỉ định, với tên file bên dưới, tên log tự động đặt là Ngày_hiện_tại.txt
    # filePath: Tên đường dẫn
    # cmdWrite: Nội dung file log. Mặc định là hello
    @staticmethod
    def RecordAutoLog(filePath, cmdWrite="Hello"):
        # Ghi nội dung nhận được vào Log
        path = ScFile.mkdirFolder(filePath)
        filename = time.strftime("%m%d.txt")

        thread = threading.Thread(target=ScMsgReport.__writefile, args=(ScMsgReport,path + "\\" + filename, cmdWrite))
        thread.start()

    # Ghi log # Có thể ghi log vào đường dẫn thư mục chỉ định, với tên file bên dưới, tên log tự động đặt là Ngày_hiện_tại.txt
    # filePath: Tên đường dẫn
    # cmdWrite: Nội dung file log. Mặc định là hello
    @staticmethod
    def RecordAutoPathLog(cmdWrite="Hello",filePath="D:\\LusterCache\\log",file="Null",bMessage=True,bEnable=True):
        #filePath="D:\\LusterCache\\log"
        # Ghi nội dung nhận được vào Log
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


    # Báo cáo tin nhắn thông báo
    def ReportMsg(cmdMsg="Hello",bPumpOut=True):
        # Ghi nội dung nhận được vào Log
        # Hiển thị thông tin nhận được trong thông báo
        Genote = GvVisionAssembly.GeMsgReportType
        noteType = Genote.eMRTNote
        GvVisionAssembly.ReportMessage(cmdMsg, noteType, bPumpOut)

    # Báo cáo cảnh báo (Warning)
    def ReportMsgWarn(cmdMsg="Hello",bPumpOut=True):
        # Ghi nội dung nhận được vào Log
        # Hiển thị thông tin nhận được trong thông báo
        Genote = GvVisionAssembly.GeMsgReportType
        noteType = Genote.eMRTWarning
        GvVisionAssembly.ReportMessage(cmdMsg, noteType, bPumpOut)

    # Báo cáo lỗi (Error)
    def ReportMsgError(cmdMsg="Hello",bPumpOut=True):
        # Ghi nội dung nhận được vào Log
        # Hiển thị thông tin nhận được trong thông báo
        Genote = GvVisionAssembly.GeMsgReportType
        noteType = Genote.eMRTError
        GvVisionAssembly.ReportMessage(cmdMsg, noteType, bPumpOut)

    # Báo cáo dạng cửa sổ bật lên (Popup)
    def ReportMsgPop(cmdMsg="Hello", bPumpOut=True):
        # Ghi nội dung nhận được vào Log
        # Hiển thị thông tin nhận được trong thông báo
        Genote = GvVisionAssembly.GeMsgReportType
        noteType = Genote.eMRTPopupNote
        GvVisionAssembly.ReportMessage(cmdMsg, noteType, bPumpOut)

    # Báo cáo hộp thoại tùy chỉnh, có giá trị trả về
    def ReportMsgOption(cmdMsg="Hello", bPumpOut=True):
        # Ghi nội dung nhận được vào Log
        # Hiển thị thông tin nhận được trong thông báo
        Genote = GvVisionAssembly.GeMsgReportType
        noteType = Genote.eMRTResultOption
        ans = GvVisionAssembly.ReportMessage(cmdMsg, noteType, bPumpOut)
        return ans