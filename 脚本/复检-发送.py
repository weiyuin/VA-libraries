import json
import GvGluePathAOI
import time


# 获取结果处理操作类(合并2个异性胶工具内数据)
result_opr = GvGluePathAOI.result_operator()
str_out=json.loads(GvTool.GetToolData("异形胶检测工具_5500.缺陷序列化结果"))

#检测项状态返回
str_detection_state=GvVar.GetVar("#strDetectionState")
print(str_detection_state)

##----------------------------发送-----------------------------------
noGlueState=GvVar.GetVar("#nNoGlueState")
if noGlueState == 1:
    NoGlueMes = True
    ReflowMes = 0
else:
    NoGlueMes = False
    ReflowMes = 1
Path_Mes = GvVar.GetVar("@Local") + GvVar.GetVar("#strImgPathCapSnd")
mes_upload = GvGluePathAOI.mes_upload()
dtrmes = mes_upload.get_mes_info_ex(str_out,1)
dtrmes = mes_upload.get_mes_data(dtrmes,False,1,[Path_Mes,ReflowMes])
GvVar.SetVar("#strRecheck_Result",dtrmes)
print(dtrmes)

##----------------------------存储-----------------------------------
db_opr = GvGluePathAOI.database_operator()
db_opr.set_pos(1)
str_file_path = GvVar.GetVar("@filePath")
str_path_cap = GvVar.GetVar("#strImgPathCap")
str_path_src = GvVar.GetVar("#strImgPathSrc")
strToday=time.strftime("%Y%m%d")
if GvVar.GetVar("@bSaveRecheckAOIData")==True:
    db_opr.record_datas(str_out,str_file_path,strToday,str_path_cap,str_path_src,0)