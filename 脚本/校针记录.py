import datetime
from ScImageShow import ScImageShow
from ScMsgReport import ScMsgReport

ncalibrateindex=GvVar.GetVar("#nCaliNeedle") #获取标定索引
strCurTime=GvVar.GetVar("#strCurTime")  #获取执行时间
strCurDate=datetime.datetime.now().strftime('%Y-%m-%d')  #获取系统年月日         时间            标定索引               运行时间
filePath="E:\\GVIMAGES\\Calibrate\\{date}\\{time}\\".format(date=strCurDate,time=strCurTime)  
offsetx=0.0
offsety=0.0

if ncalibrateindex==0:
    #生成当前系统时间
    strCurTime=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    GvVar.SetVar("#strCurTime",strCurTime)
elif ncalibrateindex==9:
    #分析均值
    centerpos=GvTool.GetToolData("数组生成工具_5636.输出数组")
    num=0 
    #定义基准点XY为0.0
    totalx=0.0
    totaly=0.0
    #声明for循环9次，九步标定   
    for i in range(0,9):
        #获取抓拍到blob工具里面的D值
        Eccentricity=centerpos[i].D
        #存储当前标定步数与抓取到blob的质心XY与D值
        ScMsgReport.RecordMsgFolder(filePath, "calibrate.csv", "pos{},{},{},{}".format(ncalibrateindex,centerpos[i].X,centerpos[i].Y,centerpos[i].D))
        #如果blob工具抓取到的圆度小于100，vision认为就是比较合适的圆形
        if Eccentricity<100:
           num=num+1    #num+1
           totalx=totalx+centerpos[i].X
           totaly=totaly+centerpos[i].Y
                         
    if num==0:         #如果num为0时，就设置偏移量为0.0
        offsetx=0.0
        offsety=0.0
    else:
        offsetx=totalx/num    #否则设置的偏移量除以当前num值
        offsety=totaly/num
print(offsetx)
print(offsety)

GvVar.SetVar("#doffsetx",GvVar.GetVar("#dFristPosX")-offsetx)   #设置当前的相对位置到变量       
GvVar.SetVar("#doffsety",GvVar.GetVar("#dFristPosY")-offsety)          
            
# 获取 GUI 显示数组——重要初始化显示数组
guiArray = GvVisionAssembly.GcScriptGuiArray()
#显示轮廓
if GvTool.GetToolData("Blob工具_5634.执行结果"):
    VecVec2=GvTool.GetToolData("Blob结果解析_5637.轮廓边界点")
    ScImageShow.ImageShowPolyline(ScImageShow,guiArray,VecVec2, clrLineColor=[0,255,0], nLineWidth=2)
# 将 GUI 数组设置到视图——只需要设置一次在程序末尾
GvGuiDataAgent.SetGraphicDisplay("校针", guiArray)