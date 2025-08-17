from ScFile import ScFile
import time
import os

#生成当前系统日期
strCurDate=GvVar.GetVar("#strYearTime")
strCurentTime=GvVar.GetVar("#strCurTime")
struploadpath=GvVar.GetVar("#struploadpath")
strupload=GvVar.GetVar("#strIsupload")
sn=GvVar.GetVar("#strSN")
Local = GvVar.GetVar("@Local")[:2]
folderpth=Local + "\\IMG\\{}".format(strCurDate)
strStationID=GvVar.GetVar("#strStationID")
ScFile.mkdirFolder(folderpth)
# 压缩路径
struploadpath= Local + "\\GVIMAGES\\MES\\{date}\\{isupload}\\{SN}\\".format(date=strCurDate,SN=sn,isupload=strupload)
GvVar.SetVar("#struploadpath",struploadpath)
############################################################延时
LSL=1#图片数量下限
nSavenumber = GvVar.GetVar("@nSavenumber") #循环次数
dSavetime = GvVar.GetVar("@dSavetime") #单次循环时间
#检测图片数量以及延时
for a in range(0,nSavenumber):
    ImagePcs =0	
    files=os.listdir (struploadpath)	
    for i in files:	
        if i.endswith(".jpg") or i.endswith(".bmp"):	
            ImagePcs +=1	
    print(ImagePcs)	
    if ImagePcs >= int(LSL):	
        break	
    else:	
        time.sleep (dSavetime)
##############################################################
if strupload!="OFF":
    zip_file_path=Local + "\\IMG\\{}\\".format(strCurDate)
    try:
        isExists = os.path.exists(zip_file_path)
        # 判断结果
        if not isExists:
            os.makedirs(zip_file_path)
    except:
        print(12)
    # zip_name= Local + "\\IMG\\{}\\{}_{}.zip".format(strCurDate,sn,strCurentTime)
    # ScFile.Sczip_file(ScFile,struploadpath,zip_name)
    if strStationID != "":
        zip_name= Local + "\\IMG\\{}\\{}_{}_{}.zip".format(strCurDate,sn,strStationID,strCurentTime)
    else:
        zip_name= Local + "\\IMG\\{}\\{}_{}.zip".format(strCurDate,sn,strCurentTime)
    ScFile.Sczip_file(ScFile,struploadpath,zip_name)