import json
import GvGluePathAOI
from ScImageShow import ScImageShow 
import math

# 获取结果处理操作类
result_opr = GvGluePathAOI.result_operator()
str_out1=json.loads(GvTool.GetToolData("主检_6156.缺陷序列化结果"))
str_out2=json.loads(GvTool.GetToolData("断胶检测异形胶检测工具_7149.缺陷序列化结果"))

#获取missing的NG区域
missing_list=result_opr.get_NG_region(str_out1,1)
print(missing_list)
#获取断胶的NG区域
broken_list=result_opr.get_NG_region(str_out2,2)
print(len(broken_list))

#根据面积检测结果,进一步拆分成小片段号放入列表missingList
missingList=[]
for i in range(0,len(missing_list)):
    if missing_list[i]!=0 and i>5 and i<len(missing_list)-1:
        for j in range(0,5):
            missingList.append(i*5+j+1)
    if missing_list[i]!=0 and i==len(missing_list)-1:
        for k in range(0,len(broken_list)-5*(len(missing_list)-1)):
            missingList.append(i*5+k+1)
print(missingList)

# #将所有断胶小片段号存入列表brokenList
brokenList=[]
for i in range(30,len(broken_list)):
    if broken_list[i]!=0:
        brokenList.append(i+1)
    else:
        pass
print(brokenList)

listRegionVec=[]
#将missing和broken的片段号列表求并集存入新列表listRegionVec中并使新列表中数据listRegionVec=[]#总列表
for i in range(30,len(broken_list)):
    if i+1 in missingList or i+1 in brokenList:
        listRegionVec.append(i+1)
    else:
        pass
print(listRegionVec)#唯一且按序

#求listRegionVec中所有区域所在点集合的列表pntsListRegion，并剔除所有点可能存在的重复数据
pntsListRegion=[]#片段所在点集列表
for i in range(30,len(broken_list)):
    for j in range(0,len(listRegionVec)):
        if listRegionVec[j]==i+1:
            if i+1 in pntsListRegion:
                pass
            else:
                pntsListRegion.append(i+1)
            if listRegionVec[j]<len(broken_list):
                pntsListRegion.append(i+2)
            else:
                pntsListRegion.append(1)
print(pntsListRegion)
# print(len(pntsListRegion))               
#按小片段连续性进行分段组合,将片段点集存入列表listSectionPointsVec中
listSectionPointsVec=[]#分段列表
listSectionPoints=[]#单段点集列表
for i in range(1,len(pntsListRegion)):
    if i==1:
        listSectionPoints.append(pntsListRegion[i-1])
    if pntsListRegion[i]==pntsListRegion[i-1]+1:
        listSectionPoints.append(pntsListRegion[i])
        print(listSectionPoints)
        if i==len(pntsListRegion)-1:
            listSectionPointsVec.append(listSectionPoints)
            listSectionPoints=[]
        else:
            pass
    else:
        if i<len(pntsListRegion)-1:
            listSectionPointsVec.append(listSectionPoints)
            listSectionPoints=[]
        else:
            if i==len(pntsListRegion)-1:
                if pntsListRegion[i]==1:
                    listSectionPoints.append(pntsListRegion[i])
                    listSectionPointsVec.append(listSectionPoints)
                    listSectionPoints=[]
            else:
                pass
print(listSectionPointsVec)
print(1111)
#输出补胶点位以及坐标数据，ARC表示圆弧只能由奇数构成，line为直线只能由2个点构成
outDatal=""
XList=GvTool.GetToolData("X数组生成工具_6851.输出数组")
YList=GvTool.GetToolData("Y数组生成工具_6852.输出数组")
print(XList[45])
print(YList[45])
strCompensationResult=GvVar.GetVar("#strCompensationResult")
bGluePath2Compensation=GvVar.GetVar("#bGluePath2Compensation")
strCompensationData=""
for SectionPoints in listSectionPointsVec:
    if len(SectionPoints)==2:
        strData="@LIN"
        strData=strData+';'+str(round(XList[SectionPoints[0]-1],2))+','+str(round(YList[SectionPoints[0]-1],2))+','+str(SectionPoints[0])+';'+str(round(XList[SectionPoints[0]],2))+','+str(round(YList[SectionPoints[0]],2))+','+str(SectionPoints[1])
        strCompensationData=strCompensationData+";"+str(SectionPoints[0])+','+str(SectionPoints[1])
    elif len(SectionPoints)>2:
        strData="@ARC"
        for i in range(0,len(SectionPoints)-1):
            strData=strData+';'+str(round(XList[SectionPoints[i]-1],2))+','+str(round(YList[SectionPoints[i]-1],2))+','+str(SectionPoints[i]-1)
            strCompensationData=strCompensationData+','+str(SectionPoints[i])
        if (len(SectionPoints))%2==0:
            # print(SectionPoints[i])
            # print(i)
            # print(SectionPoints[-1])
            strData=strData+"@LIN;"+str(round(XList[SectionPoints[-1]-2],2))+','+str(round(YList[SectionPoints[-1]-2],2))+','+str(SectionPoints[-1]-2)+';'+str(round(XList[SectionPoints[-1]-1],2))+','+str(round(YList[SectionPoints[-1]-1],2))+','+str(SectionPoints[-1]-1)
            strCompensationData=strCompensationData+';'+str(SectionPoints[-1]-1)+','+str(SectionPoints[-1])
        else:
            strData=strData+';'+str(round(XList[SectionPoints[-1]-1],2))+','+str(round(YList[SectionPoints[-1]-1],2))+','+str(SectionPoints[-1]-1)
            strCompensationData=strCompensationData+','+str(SectionPoints[-1])
    outDatal=outDatal+strData
print(outDatal)
if "GlueRepair:FOF" in strCompensationResult and bGluePath2Compensation==False:
    strCompensationResult=strCompensationResult[:-1]
    strCompensationResult=strCompensationResult+';'+strCompensationData[1:]
if "GlueRepair:FOF" in strCompensationResult and bGluePath2Compensation==True:
    pass
if "GlueRepair:FOF" not in strCompensationResult and bGluePath2Compensation==False:
    strCompensationResult=strCompensationResult+';'+strCompensationData[1:]
print(strCompensationResult)
if outDatal!="":
    GvVar.SetVar("#strCompensationRes","FOF")
    if not "GlueRepair:FOF" in strCompensationResult:
        strCompensationResult="GlueRepair:FOF({})".format(strCompensationResult[1:])
    elif not bGluePath2Compensation:
        strCompensationResult=strCompensationResult+")"
GvVar.SetVar("#strCompensationResult",strCompensationResult)
GvVar.SetVar("#bGluePath2Compensation",True)
GvVar.SetVar("#bGlueCompensation",True)
GvVar.SetVar("#strReflow",outDatal)    
print(strCompensationResult)
print(len(strCompensationResult))

def GetFixedLengthData(strInputData,lengthStrSpec):
    if len(strInputData)<=lengthStrSpec:
        strList.append(strInputData)
    else:
        if strInputData[lengthStrSpec-1]==";" or strInputData[lengthStrSpec-1]==",":
            strList.append(strInputData[0:lengthStrSpec])
            strInputData=strInputData[lengthStrSpec:]
            GetFixedLengthData(strInputData,lengthStrSpec)
        else:
            # print(152535)
            for i in range(2,5):
                print(i)
                if strInputData[lengthStrSpec-i]==";" or strInputData[lengthStrSpec-i]==",":
                    strList.append(strInputData[0:lengthStrSpec-i])
                    strInputData=strInputData[lengthStrSpec-i:]
                    break
            GetFixedLengthData(strInputData,lengthStrSpec)
    return strList

nLengthSpec=GvVar.GetVar("#nstrFOFLenthSpec")
strList=[]
if len(strCompensationResult)>0:
    strDataList=GetFixedLengthData(strCompensationResult,lengthStrSpec=nLengthSpec)
    print(strDataList)
    line_space=10
    fontSize=60
    guiArray = GvVisionAssembly.GcScriptGuiArray()
    for i in range(0,len(strDataList)):
        guiArray.Add(GvGluePathAOI.imageShowTextXY(posX=20, posY=20+fontSize*2+(7+i)*(line_space+fontSize), strmsg=strDataList[i], clrLineColor=[255, 0, 0], lFontSize=fontSize,nStyle=0))
    GvGuiDataAgent.SetGraphicDisplay("新复检区域", guiArray)

#补胶完初始化拍照次数
GvVar.SetVar("#nPic_index",0)