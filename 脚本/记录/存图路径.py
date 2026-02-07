import datetime

strImgPathSrc = "" #原图路径
strImgPathCap = "" #截图路径
nFlag = GvVar.GetVar("#nFlag") #是否OK/NG
print(nFlag)


strCurrentDate = datetime.datetime.now().strftime("%Y-%m-%d")
strCurrentTime = datetime.datetime.now().strftime("%H-%M-%S")

#OK====================================
if(nFlag == 1):
    strImgPathSrc = "{:s}\\原图\\OK\\{:s}.SRC".format(strCurrentDate,strCurrentTime)
    strImgPathCap = "{:s}\\截图\\OK\\{:s}.CAP".format(strCurrentDate,strCurrentTime)
#NG====================================
elif(nFlag == 0):
    strImgPathSrc = "{:s}\\原图\\NG\\{:s}.SRC".format(strCurrentDate,strCurrentTime)
    strImgPathCap = "{:s}\\截图\\NG\\{:s}.CAP".format(strCurrentDate,strCurrentTime)

print(strImgPathSrc)
print(strImgPathCap)
GvVar.SetVar("#strImgPathSrc",strImgPathSrc) 
GvVar.SetVar("#strImgPathCap",strImgPathCap)