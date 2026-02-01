import json
import GvGluePathAOI
import time


# 获取结果处理操作类(合并2个异性胶工具内数据)
result_opr = GvGluePathAOI.result_operator()
str_out=json.loads(GvTool.GetToolData("主检_6156.缺陷序列化结果"))

#检测项状态返回
strDetectionStateSnd=GvVar.GetVar("#strDetectionStateSnd")



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
# print(dtrmes)
dtrmes = mes_upload.get_mes_data(dtrmes,False,1,[Path_Mes,ReflowMes],b_open_recheck=True)#参数b_open_recheck为复检开关，False时关闭复检强制OK
dtrmes = dtrmes+";"+strDetectionStateSnd
# print(dtrmes)
a = dtrmes.split(';')[2].split('@')[2]

GvVar.SetVar('#strstatus',a)

# dtrmes = dtrmes[0]+';'+dtrmes.split(';')[2][0:10]+';'+dtrmes.split(';')[4]
# print(dtrmes)
#ew新增
dtrmes1=dtrmes.split(';')[0]
dtrmes2=dtrmes.split(';')[1]
dtrmes3=dtrmes.split(';')[2]
dtrmes4=dtrmes.split(';')[3]
# print(dtrmes1)
bGlueCompensation=GvVar.GetVar("#bGlueCompensation")
# if bGlueCompensation:
    # dtrmes31=dtrmes3.split(",")
    # dtrmes32=dtrmes31[0].split("@")
    # dtrmes33=dtrmes32[0]+"@"+dtrmes32[1]+"@"+"FOF@@"
    # dtrmes34=(dtrmes31[1:])
    # strxx=""
    # for i in dtrmes34:
        # i=i+","
        # strxx+=i
    # dtrmes3=dtrmes33+","+strxx
    # dtrmes3=dtrmes3[:-1]

# dtrmes5=dtrmes1+';'+dtrmes3+';'+strDetectionStateSnd
dtrmes5=dtrmes1+','+dtrmes3
print(dtrmes5,888)

GvVar.SetVar("#strRecheck_Result",dtrmes5)
#GvVar.SetVar("#strRecheck_Result",dtrmes)

##----------------------------存储-----------------------------------
db_opr = GvGluePathAOI.database_operator()
db_opr.set_pos(1)
str_file_path = GvVar.GetVar("@filePath")
str_path_cap = GvVar.GetVar("#strImgPathCap")
str_path_src = GvVar.GetVar("#strImgPathSrc")
strToday=time.strftime("%Y%m%d")
if GvVar.GetVar("@bSaveRecheckAOIData")==True:
    db_opr.record_datas(str_out,str_file_path,strToday,str_path_cap,str_path_src,0)
    