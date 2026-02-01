import json
import GvGluePathAOI
from GvGluePathAOI import ScImageShow

guiArray = GvVisionAssembly.GcScriptGuiArray()
# 获取结果处理操作类(合并2个异性胶工具内数据)
result_opr = GvGluePathAOI.result_operator()
str_out1=json.loads(GvTool.GetToolData("主检_6156.缺陷序列化结果"))
str_out5=json.loads(GvTool.GetToolData("断胶检测异形胶检测工具_7149.缺陷序列化结果"))
#Coverage优选
try:
    str_out2=json.loads(GvTool.GetToolData("coverage_6154.缺陷序列化结果")) 
    str_out3=json.loads(GvTool.GetToolData("基准_6155.缺陷序列化结果"))                                
    #自动
    region_num = str_out2["base_info"]["region_number"]
    list_region = [0,1,2,3,4,5,6,7,8]
    data2,errorcode2 = result_opr.data_obtain(str_out2,list_region,4)
    data3,errorcode3 = result_opr.data_obtain(str_out3,list_region,4)
    area_percent = []
    for i in range(0,len(data2)):
        if data2[i] == 0:
            area_percent.append(1)
        else:
            percent = 1-float(data2[i]/data3[i])
            area_percent.append(percent)
except:
    area_percent=[0,0,0,0,0,0,0,0,0]
    data2=[99999,99999,99999,99999,99999,99999,99999,99999,99999]
#手动
str_out4=json.loads(GvTool.GetToolData("手绘Coverage_7019.缺陷序列化结果"))                                
data4,errorcode4 = result_opr.data_obtain(str_out4,list_region,5)
CoverageMode=1
#自动存在NG或者执行失败，则判断是否启用手绘
if (sum(data2)!=0 or not GvTool.GetToolData("图像运算工具_6196.执行结果")) and sum(errorcode4)==0:
    area_percent=data4
    CoverageMode=2
else:
    pass
print(CoverageMode)
#数据写回
str_out1=result_opr.data_replace(str_out1,area_percent,list_region,5)

##----------------------------显示-----------------------------------
gui_opr = GvGluePathAOI.glue_display()
## 显示胶路面积
gui_opr.set_show_mode(True)
## NoGlue结果赋值
if GvTool.GetToolData("胶路Blob工具_5968.总像素数")>6000:
    noGlueState=1
else:
    noGlueState=0
GvVar.SetVar("#nNoGlueState",noGlueState)
gui_opr.set_noglue_state(noGlueState)

#设置镜像
mirrMode=0
# if GvVar.GetVar("@bLeftOrRight")==True:
    # mirrMode=0
# else:
    # mirrMode=1
gui_opr.set_mirror(mirrMode,5472/2,3648/2)

guiArray = gui_opr.show_general_data_Ex(guiArray,str_out1,font_size=60,offset_x=20,offset_y=20,line_space=10,line_width=2,bShowMinWidth=False,show_OK=True,dict_broken_json=str_out5)
guiArray = gui_opr.show_detetion_Region(guiArray,str_out5,show_OK=False)
#胶占比区域显示
if CoverageMode==2:
    guiArray = gui_opr.show_detetion_Region(guiArray,str_out4)
else:
    try:
        polyLine1=GvTool.GetToolData("Blob工具_6193.Blob结果轮廓")#抓点生成
        polyLine2=GvTool.GetToolData("Blob工具_6220.Blob结果轮廓")#抓点生成
        for polyline in polyLine1:
            ScImageShow.ImageShowPolyline(ScImageShow,guiArray,polyline.GetVertices(), clrLineColor=[0, 255, 0])
        for polyline in polyLine2:
            ScImageShow.ImageShowPolyline(ScImageShow,guiArray,polyline.GetVertices(), clrLineColor=[255, 0, 0])
    except:
        pass

## 检测结果赋值
bGlueCompensation=GvVar.GetVar("#bGlueCompensation")
error_code,strRes,strResMes = gui_opr.get_detect_result(str_out1)
strCompensationResult=GvVar.GetVar("#strCompensationResult")
RGBData=[0, 255, 0]
if error_code==1:
    pass
else:
    RGBData=[255, 0, 0]
## FOF显示
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
if bGlueCompensation:
    strRes="FOF"
    if len(strCompensationResult)>0:
        strDataList=GetFixedLengthData(strCompensationResult,lengthStrSpec=nLengthSpec)
        # print(strDataList)
        line_space=10
        fontSize=60
        for i in range(0,len(strDataList)):
            guiArray.Add(GvGluePathAOI.imageShowTextXY(posX=20, posY=20+fontSize*2+(7+i)*(line_space+fontSize), strmsg=strDataList[i], clrLineColor=RGBData, lFontSize=fontSize,nStyle=0)) 

GvGuiDataAgent.SetGraphicDisplay("新复检区域", guiArray)  

GvVar.SetVar("#strFlag",strRes)
GvVar.SetVar("#nErrorCode",str_out1['base_info']['error_code'])
print(strRes,error_code)
print(strResMes)
## 检测数据回传
GvTool.SetToolData("主检_6156.缺陷序列化结果",json.dumps(str_out1))
## 检测项状态返回 1开启 0关闭 
## 按 有无胶状态,胶占比,missing,断胶,溢胶,孔洞,偏移,胶长 进行排序。
strDetectionState_Spec = GvVar.GetVar("#strDetectionState_Spec")     ## "111122222"
strDetectionState = gui_opr.get_detect_state(str_out1).replace(',','')
strDetectionState_New = ""
if len(strDetectionState_Spec) == len(strDetectionState):
    for i in range(len(strDetectionState_Spec)):
        if strDetectionState_Spec[i] == "2":
            if strDetectionState[i] == "1":
                strDetectionState_New = strDetectionState_New + strDetectionState[i]
            else:
                strDetectionState_New = strDetectionState_New + strDetectionState_Spec[i]
        else:
            strDetectionState_New = strDetectionState_New + strDetectionState[i]
else:
    strDetectionState_New = strDetectionState

## 发送：实际值@下限@上限（取7位）
strDetectionState_Snd = strDetectionState_New[0:7] + "@" + strDetectionState_Spec[0:7] + "@" + strDetectionState_Spec[0:7]
GvVar.SetVar("#strDetectionStateSnd",strDetectionState_Snd)
print(strDetectionState_Snd)