import datetime
import os

def WriteFile(path, filename,data):
    if not os.path.exists(path):
        os.makedirs(path)
    if not os.path.exists(path + filename):
        file = open(path + filename, "a", encoding="utf-8")
        file.write(data)
        file.close()
    else:
        file = open(path + filename, "a", encoding="utf-8")
        file.write(data)
        file.close()
#时间
strCurrentDate = datetime.datetime.now().strftime("%Y-%m-%d")
strMilliseconds = datetime.datetime.now().strftime("%f")[:3]
strCurrentTime = datetime.datetime.now().strftime("%H:%M:%S")+ ":" + strMilliseconds

strCMD = GvTool.GetToolData("发送_017.输出文本")
path = "D:\\LOG\\{:s}\\".format(strCurrentDate)
filename = "LOG.txt"

#视觉返回：T,0/1（0：NG，1：OK）,划伤个数,黑点个数
data = "时间：{:s}    发送    指令：{:s}\n".format(strCurrentTime,strCMD)
 
print(path)
print(data)

WriteFile(path, filename, data)