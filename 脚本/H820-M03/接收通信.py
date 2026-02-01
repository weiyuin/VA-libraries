from ScMsgReport import ScMsgReport
import time
import datetime

strCMD0=GvTool.GetToolData("数据包解析工具_003.输出数据0")
strSN=GvTool.GetToolData("数据包解析工具_003.输出数据1")
SaveImgpath=GvTool.GetToolData("数据包解析工具_003.输出数据2")
strUpLoadName=GvTool.GetToolData("数据包解析工具_003.输出数据3")

#导入key值时启用

if (strCMD0 == "V01") or (strCMD0 == "V11"):
    offset_X=float(GvTool.GetToolData("数据包解析工具_003.输出数据3"))
    offset_Y=float(GvTool.GetToolData("数据包解析工具_003.输出数据4"))
    nAngleModify=int(GvTool.GetToolData("数据包解析工具_003.输出数据5"))
    # nIndexFlow=GvTool.GetToolData("数据包解析工具_003.输出数据6")
    GvVar.SetVar("#nAngleModify",nAngleModify)
    GvVar.SetVar("#dOffsetGuiding_X",offset_X)
    GvVar.SetVar("#dOffsetGuiding_Y",offset_Y)


#生成当前系统时间
DayTime=datetime.datetime.now().strftime('%Y%m%d_')
strToday = time.strftime("%Y%m%d")
strfulltime = time.strftime("%Y%m%d%H%M%S")

try:
    strCurTime=DayTime+SaveImgpath.split('/')[-2]
    strCurTime=strCurTime[9:18]
except:
    strCurTime=datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')
    print(strCurTime,1)
print(strCurTime)

################判断是否过站
if len(strSN)>11:  #判断是否MES料 
    MES="ON"
else:
    MES="OFF"

GvVar.SetVar("#strCurTime",strCurTime.split("_")[-1])
nPic_index=GvVar.GetVar("#nPic_index")
if GvVar.GetVar("#strSN")!=strSN or GvVar.GetVar("#strCMD0")!=strCMD0:
    nPic_index=1
if GvVar.GetVar("#strSN")==strSN and GvVar.GetVar("#strCMD0")==strCMD0:
    nPic_index=nPic_index+1
if nPic_index>2:
    nPic_index=3

GvVar.SetVar("#strSN",strSN)
GvVar.SetVar("#nPic_index",nPic_index)


GvVar.SetVar("#strIsUpload",MES)
GvVar.SetVar("#strUpLoadName",strUpLoadName)
GvVar.SetVar("#strSaveImgpath",SaveImgpath)
GvVar.SetVar("@Saveimgpath",SaveImgpath)
GvVar.SetVar("#strCMD0",strCMD0)
GvVar.SetVar("#strfulltime",strfulltime)

try:
    strYearTime = SaveImgpath.split('/')[-3]
    GvVar.SetVar("#strYearTime",strYearTime)
    print(strYearTime)
except:
    GvVar.SetVar("#strYearTime",datetime.datetime.now().strftime('%Y-%m-%d'))

# 日志记录及显示
strMsg=GvTool.GetToolData("通信接收工具_001.接收字符串")
strHead=GvVar.GetVar("#strHead")
strToday = time.strftime("%Y%m%d")
# 日志记录
ScMsgReport.RecordAutoLog("E:\\LusterCache\\CCDlog\\{strToday}".format(strToday=strToday),strHead+"Reca"+strMsg)
# 日志显示
ScMsgReport.ReportMsg(strHead+"Reca"+strMsg)



#变量初始化
GvVar.SetVar("@ModelImage",1)      #实时采集

#生成NGImagePath的路径
ImagePath=GvTool.GetToolData("数据包解析工具_003.输出数据2")


try:
    if len(ImagePath)>10 :   
        ImagePath=ImagePath.split('/')
        ImagePath[4]="NG_CCD"
        print(ImagePath)
        NGImagePath=""
        for i in ImagePath[0:-1]:
             NGImagePath=NGImagePath+i+'\\'
        print(NGImagePath)
        GvVar.SetVar("#strNGimagePath",NGImagePath)
        print(1)
except:
    ScMsgReport.ReportMsg("图片路径异常！！！！")



# if len(ImagePath)>10 :   
   # ImagePath=ImagePath.split('/')
   # ImagePath[4]="NG_CCD"
   # print(ImagePath)
   # NGImagePath=""
   # for i in ImagePath[0:-1]:
       # NGImagePath=NGImagePath+i+'\\'
   # print(NGImagePath)
   # GvVar.SetVar("#strNGimagePath",NGImagePath)


#胶路分割方式防呆
nSwitch1=GvVar.GetVar("#nSwitch1")
if nSwitch1!=1 and nSwitch1!=2:
    nSwitch1=1
GvVar.SetVar("#nSwitch1",nSwitch1)

nSwitch2=GvVar.GetVar("#nSwitch2")
if nSwitch2!=1 and nSwitch2!=2:
    nSwitch2=1
GvVar.SetVar("#nSwitch2",nSwitch2)


strReceived=GvTool.GetToolData("通信接收工具_001.接收字符串")
strRcdList=strReceived.split(",")
print(len(strRcdList))
print((strRcdList))
if (GvVar.GetVar("#strCMD0")=="J0" or GvVar.GetVar("#strCMD0")=="J1") and len(strRcdList)==10 and strRcdList[1]=='0':
    calibNeedleDispenseX=float(strRcdList[4])
    calibNeedleDispenseY=float(strRcdList[5])
    calibNeedleCapX=float(strRcdList[7])
    calibNeedleCapY=float(strRcdList[8])
    print(calibNeedleDispenseX,calibNeedleDispenseY,calibNeedleCapX,calibNeedleCapY)
    if GvVar.GetVar("#strCMD0")=="J0":
        GvVar.SetVar("#dPosAixeLX",calibNeedleDispenseX)
        GvVar.SetVar("#dPosAixeLY",calibNeedleDispenseY)
        GvVar.SetVar("#dPosCCDCailLX",calibNeedleCapX)
        GvVar.SetVar("#dPosCCDCailLY",calibNeedleCapY)
    if GvVar.GetVar("#strCMD0")=="J1":
        GvVar.SetVar("#dPosAixeRX",calibNeedleDispenseX)
        GvVar.SetVar("#dPosAixeRY",calibNeedleDispenseY)
        GvVar.SetVar("#dPosCCDCailRX",calibNeedleCapX)
        GvVar.SetVar("#dPosCCDCailRY",calibNeedleCapY)
if (GvVar.GetVar("#strCMD0")=="V01" or GvVar.GetVar("#strCMD0")=="V11") and len(strRcdList)==9:
    currentCCDX=float(strRcdList[6])
    currentCCDY=float(strRcdList[7])
    print(currentCCDX,currentCCDY)
    if GvVar.GetVar("#strCMD0")=="V01":
        GvVar.SetVar("#dPosCCDCurrentLX",currentCCDX)
        GvVar.SetVar("#dPosCCDCurrentLY",currentCCDY)
    if GvVar.GetVar("#strCMD0")=="V11":
        GvVar.SetVar("#dPosCCDCurrentRX",currentCCDX)
        GvVar.SetVar("#dPosCCDCurrentRY",currentCCDY)