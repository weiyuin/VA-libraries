from ScImageShow import ScImageShow
guiArray = GvVisionAssembly.GcScriptGuiArray()
bLeftOrRight=GvVar.GetVar("@bLeftOrRight")
imgWidth=GvVar.GetVar("@imgWidth")


point=GvTool.GetToolData("找任意曲线工具_6842.采样拟合点集GUI")
scVec=GvVisionAssembly.sc2VectorVec()
for i in range(0,len(point)):
    X=point[i].pt.GetX()
    if bLeftOrRight==False:
        X=imgWidth-X
    Y=point[i].pt.GetY()
    tempPoint=GvVisionAssembly.sc2Vector( X, Y)
    scVec.append(tempPoint)

print(len(scVec))

#起点获取
StartPoint=GvTool.GetToolData("直线到轮廓交点工具_7047.交点集合")[0]
print(StartPoint.GetY(),scVec[0].GetY())
#查找最近点
startIndex=0
minDis=9999999999
for i in range(0,len(scVec)):
    dis=GvVisionAssembly.DistancePoint2Point(point[i].pt,StartPoint).distance
    if minDis>dis:
       minDis=dis
       startIndex=i
print("Start:",startIndex)
#基于引导点重新排序
offsetNum=795
if startIndex>=offsetNum:
    startIndex=startIndex-offsetNum
else:
    startIndex=len(scVec)+startIndex-offsetNum
tempVec=scVec[startIndex:len(scVec)]
tempVec.extend(scVec[0:startIndex-1])
scVec=tempVec

#从点集中取点
count=GvVar.GetVar("#nGluePointCount")#取点个数
strSaveData=""
sc2VectorVec=GvVisionAssembly.sc2VectorVec()
print("取点间隔:",int(len(scVec)/count))
for i in range(0,count):
    strSaveData=strSaveData+","+"{:.3f},{:.3f}".format(scVec[i*int(len(scVec)/count)].GetX(),scVec[i*int(len(scVec)/count)].GetY())
    sc2VectorVec.append(scVec[i*int(len(scVec)/count)])
GvVar.SetVar("#strGulePointPose",strSaveData)
#记录点胶点位图像坐标数据
if GvVar.GetVar("#str_Flowpath")=="R":
    GvVar.SetVar("#strGluePoseImgRight",strSaveData)
else:
    GvVar.SetVar("#strGluePoseImgLeft",strSaveData)

#数据记录
import time
import os
def WriteFile(path,filename,header,data):
    if(not os.path.exists(path)):
        os.makedirs(path)
    if(not os.path.exists(path+filename)):
        file=open(path+filename,"a")
        file.write(header)
        file.write(data)
        file.close()
    else:
        file=open(path+filename,"a")
        file.write(data)
        file.close()
####
path="D:\\LusterCache\\Logs\\点位数据\\"#数据路径
filename=time.strftime("%Y-%m-%d.csv",time.localtime())
time=time.strftime("%H:%M:%S",time.localtime())
header="Time"
for i in range(len(sc2VectorVec)):
    header=header+","+"{}-X,{}-Y".format(i+1,i+1)
header=header+"\n"
data="{:s}{:s}\n".format(time,strSaveData)    
if GvVar.GetVar("#bSavePosData"):
    WriteFile(path,filename,header,data)

#距离测量
try:
    Dis3= GvTool.GetToolData("Blob工具_7037.Blob结果")[0].BlobResult.perimeter*GvVar.GetVar("#dPose1_CalibPix_X")
except:
    Dis3=999   
GvVar.SetVar("#dDistance",Dis3)

#key值后胶路显示，导入时解除注释
################################################################################################
pixScaleX=GvVar.GetVar("#dPose1_CalibPix_X")
pixScaleY=GvVar.GetVar("#dPose1_CalibPix_Y")
if GvVar.GetVar("#strCMD0")=="V01":
    pass
else:
    pixScaleX=GvVar.GetVar("#dPose2_CalibPix_X")
    pixScaleY=GvVar.GetVar("#dPose2_CalibPix_Y")
offsetX=GvVar.GetVar("#dOffsetGuiding_X")
offsetY=-GvVar.GetVar("#dOffsetGuiding_Y")
print(offsetX,offsetY)
def offsetTrans(points,deltaX,deltaY,pixelScaleX,pixelScaleY):
    newPoints=GvVisionAssembly.sc2VectorVec()
    for i in range(0,len(points)):
        newPoint=GvVisionAssembly.sc2Vector(points[i].GetX()+deltaX/pixelScaleX,points[i].GetY()+deltaY/pixelScaleY)
        newPoints.append(newPoint)
    return newPoints
if GvVar.GetVar("#enableKeyPathShow"):
    sc2VectorVec=offsetTrans(sc2VectorVec,offsetX,offsetY,pixScaleX,pixScaleY)
else:
    pass
################################################################################################

#显示
#轮廓
ScImageShow.ImageShowPolyline(ScImageShow,guiArray,scVec, clrLineColor=[0,255, 0], nLineWidth=3)
#点集
if GvTool.GetToolData("找任意曲线工具_6844.执行结果"):
    for i in range(0,len(sc2VectorVec)):
        ScImageShow.ImagechowCrossVec(ScImageShow,guiArray, sc2VectorVec[i], clrLineColor=[255,255, 0], nLineWidth=2)
        ScImageShow.ImageShowTextXY(ScImageShow,guiArray,sc2VectorVec[i].GetX(),sc2VectorVec[i].GetY(),strmsg=str(i+1),clrLineColor = [0,255, 0],lFontSize = 100,degree=0.0)
    if GvVar.GetVar("#str_Flowpath")=="L":
        GvGuiDataAgent.SetGraphicDisplay("左流道定位", guiArray)
        GvGuiDataAgent.SetGraphicDisplay("左第一道胶路", guiArray)
        GvGuiDataAgent.SetGraphicDisplay("左第二道胶路", guiArray)
    else:
        GvGuiDataAgent.SetGraphicDisplay("右流道定位", guiArray)
        GvGuiDataAgent.SetGraphicDisplay("右第一道胶路", guiArray)
        GvGuiDataAgent.SetGraphicDisplay("右第二道胶路", guiArray)


