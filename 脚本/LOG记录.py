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

strCMD = GvTool.GetToolData("通信接收工具_001.输出数据0")
n = GvVar.GetVar("#n")          #0：无产品，1：产品不合格，2：产品合格
dDistance = GvVar.GetVar("#dDistance") #宽度

path = "D:\\LOG\\{:s}\\".format(strCurrentDate)
filename = "LOG.txt"
#CCD返回：C,0/1/2（0：无产品，1：产品不合格，2：产品合格）,宽度（保留小数点后三位）
data = "时间：{:s}    指令：{:s}    有无产品：{:d}    宽度：{:.3f}\n".format(strCurrentTime,strCMD,n,dDistance)
 
print(path)
print(data)

WriteFile(path, filename, data)