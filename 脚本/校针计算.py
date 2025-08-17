#按真实需求，判断九个点圆度，若圆度符合要求，则计算符合要求胶点质心的平均值进行校针，
#若符合圆度要求的点小于阈值，则直接校针失败，重新校针

dAcircularity_SPEC=GvVar.GetVar("#dAcircularity_SPEC")#圆度阈值
nInSpecCount=GvVar.GetVar("#nInSpecCount")#在圆度阈值个数点的阈值
dataVec=GvTool.GetToolData("信息记录数组生成_5656.输出数组")#获取blob抓取数据
#数据初始化
Needle_Display=True
Needle_Result=""
x=0
y=0
strSaveData=""
#判断有多少圆度在Spec范围内
Ok_count=0
for i in range(0,len(dataVec)):
    tempAcircularity=dataVec[i].D
    strSaveData=strSaveData+","+"{:.3f},{:.3f},{:.3f}".format(dataVec[i].X,dataVec[i].Y,dataVec[i].D)
    if tempAcircularity<=dAcircularity_SPEC and tempAcircularity>=0.9:
        Ok_count=Ok_count+1
        x=x+dataVec[i].X
        y=y+dataVec[i].Y
#平均值计算
if Ok_count>=1:
    x=x/Ok_count
    y=y/Ok_count    
#结果判断
if Ok_count>=nInSpecCount:
    Needle_Result="校针OK! 有{}个点满足圆度要求".format(Ok_count)
else:
    Needle_Display=False
    Needle_Result="校针NG!{}低于SPEC:{},胶点误差大，请重新校针!".format(Ok_count,nInSpecCount)

GvVar.SetVar("#bNeedle_Display",Needle_Display)
GvVar.SetVar("#strNeedle_Result",Needle_Result)
GvTool.SetToolData("图像坐标二维向量生成工具_5658.X分量",x)
GvTool.SetToolData("图像坐标二维向量生成工具_5658.Y分量",y)



#校针数据存储
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
path="D:\\LusterCache\\Logs\\校针数据\\"#数据路径

filename=time.strftime("%Y-%m-%d.csv",time.localtime())
time=GvTool.GetToolData("时间格式化工具_5651.格式化结果")
header="Time"
for i in range(9):
    header=header+","+"{}-X,{}-Y,{}-Acircularity".format(i+1,i+1,i+1)
header=header+"\n"

data="{:s}{:s}\n".format(time,strSaveData)    

WriteFile(path,filename,header,data)