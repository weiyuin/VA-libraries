import datetime

strImgPathSrc = "" #原图路径
strImgPathCap = "" #截图路径
strStatus = GvVar.GetVar("#strStatus") #是否OK/NG
strCurrentDate = datetime.datetime.now().strftime("%Y-%m-%d")
strCurrentTime = datetime.datetime.now().strftime("%H-%M-%S")

#OK====================================
if(strStatus == "产品合格"):
    strImgPathSrc = "{:s}\\原图\\OK\\{:s}".format(strCurrentDate,strCurrentTime)
    strImgPathCap = "{:s}\\截图\\OK\\{:s}".format(strCurrentDate,strCurrentTime)
#NG====================================
elif(strStatus == "产品不合格"): #产品不合格
    strImgPathSrc = "{:s}\\原图\\{:s}\\{:s}".format(strCurrentDate,strStatus,strCurrentTime)
    strImgPathCap = "{:s}\\截图\\{:s}\\{:s}".format(strCurrentDate,strStatus,strCurrentTime)
elif(strStatus == "无产品"): #无产品
    strImgPathSrc = "{:s}\\原图\\{:s}\\{:s}".format(strCurrentDate,strStatus,strCurrentTime)
    strImgPathCap = "{:s}\\截图\\{:s}\\{:s}".format(strCurrentDate,strStatus,strCurrentTime)

print(strImgPathSrc)
print(strImgPathCap)
GvVar.SetVar("#strImgPathSrc",strImgPathSrc) 
GvVar.SetVar("#strImgPathCap",strImgPathCap)