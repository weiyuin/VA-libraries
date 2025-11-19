import os

def traverse_files(fileDirPath,SN,nPos,label="Original"):
    imagefiles=[]
    listTargetPath=[]
    for root, dirs, files in os.walk(fileDirPath):
        for file in files:
            if SN in file:
                listTargetPath.append(os.path.join(root,file)) #获得文件夹下所有符合SN的文件
    if listTargetPath==[]:
        return imagefiles
    else:
        for temptempflie in listTargetPath:
            if (label in temptempflie) and (("SRC" in temptempflie) or ("Src" in temptempflie)):#判断是否为定位原图
                if len(temptempflie.split("-"))>3:
                    temdata=temptempflie.split("-")
                else:
                    temdata=temptempflie.split("_")
                for strtemp in temdata:
                    if ("Station" in strtemp) or ("Pose" in strtemp):#判断是否符合指定姿态要求
                        if str(nPos)==strtemp[-1]:
                            imagefiles.append(temptempflie)
    return imagefiles

fileDirPath=GvVar.GetVar("@strfileDirPath")
SN=GvVar.GetVar("@strReadSN")
nPos=GvVar.GetVar("@nReadPos")

strReadResult=""
if nPos!=1 and nPos!=2 and nPos!=3:
    strReadResult="输入姿态错误"
elif(GvVisionAssembly.GetSystemState()):
    strReadResult="导图失败,请先切换到离线模式"
else:
    imagefiles = traverse_files(fileDirPath,SN,nPos)
    if len(imagefiles)==0:
        strReadResult="导图失败,未找到符合条件的文件"
    else:
        strReadResult="导图成功,{}".format(imagefiles[0])
        if nPos==1: 
            GvTool.SetToolData("工位1采图_4192.文件路径",(GvVisionAssembly.GsFilePath(imagefiles[0])))
        if nPos==2:
            GvTool.SetToolData("工位1采图_5412.文件路径",(GvVisionAssembly.GsFilePath(imagefiles[0])))

GvVar.SetVar("@strReadResult",strReadResult)
