import json
import GvGluePathAOI
import time


# 获取结果处理操作类(合并2个异性胶工具内数据)
result_opr = GvGluePathAOI.result_operator()
str_out1=json.loads(GvTool.GetToolData("异形胶检测工具_5347.缺陷序列化结果"))
str_out2=json.loads(GvTool.GetToolData("异形胶检测工具_5348.缺陷序列化结果"))
str_out=result_opr.merge(str_out1,str_out2)                        

##----------------------------显示-----------------------------------
guiArray = GvVisionAssembly.GcScriptGuiArray()
gui_opr = GvGluePathAOI.glue_display()
## 显示胶路面积
gui_opr.set_show_mode(True)
## NoGlue结果赋值
if GvTool.GetToolData("Blob工具_5346.总像素数")>6000:
    noGlueState=1
else:
    noGlueState=0
GvVar.SetVar("#nNoGlueState",noGlueState)
gui_opr.set_noglue_state(noGlueState)
## 显示检测结果文本
guiArray = gui_opr.show_general_data_Ex(guiArray,str_out,font_size=100,offset_x=20,offset_y=20,line_space=10,line_width=2,bShowMinWidth=False)
guiArray = gui_opr.show_detetion_Region(guiArray,str_out2)#显示胶占比ROI
GvGuiDataAgent.SetGraphicDisplay("工位3-4复检", guiArray)  
## 检测结果赋值
error_code,strRes,strResMes = gui_opr.get_detect_result(str_out)
GvVar.SetVar("#strFlag",strRes)
print(strRes)
## 检测数据回传
GvTool.SetToolData("异形胶检测工具_5347.缺陷序列化结果",json.dumps(str_out))

## 检测项状态返回（9位） 1开启 0关闭 2不检测
## 按 有无胶状态,胶占比,missing,断胶,溢胶,孔洞,偏移,胶长 进行排序。
strDetectionState_Spec = GvVar.GetVar("#strDetectionState_Spec")     ## "111122222"
strDetectionState = gui_opr.get_detect_state(str_out).replace(',','')
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