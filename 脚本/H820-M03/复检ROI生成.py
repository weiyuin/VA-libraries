#生成一个可变折线
def GenerateTrendline(x1,y1,x2,y2,rectExID,bendangle,ylength):
    polyline = GvVisionAssembly.scPolyline()
    polyline.AddVertex(GvVisionAssembly.sc2Vector(x1,y1))
    polyline.AddVertex(GvVisionAssembly.sc2Vector(x2,y2))
    ROI_Line=GvVisionAssembly.scGuiTrendlineEx()
    ROI_Line.SetPolyline(polyline)
    ROI_Line.SetBendAngle(rectExID,bendangle)
    ROI_Line.SetYlength(rectExID,ylength)
    return ROI_Line


#获取胶路图像坐标
if GvVar.GetVar("#str_Flowpath")=="R":
    glueData=GvVar.GetVar("#strGluePoseImgRight")
else:
    glueData=GvVar.GetVar("#strGluePoseImgLeft")
#检测区域个数
count=46
startIndex=0
#取点序号31~46+1 产生16个检测区域
GvTool.SetToolData("多项Blob工具_7133.ROI总数",count)
ROI=GvVisionAssembly.scGuiTrendlineExVec()
dBend=10
if GvVar.GetVar("@bLeftOrRight"):
    pass
else:
    dBend=-dBend
print(dBend)
for i in range(0,count+startIndex):
    temp=GvVisionAssembly.scAffineRect()
    startPointX=float(glueData[1:].split(",")[i*2])/2
    startPointY=float(glueData[1:].split(",")[i*2+1])/2
    try:
        endPointX=float(glueData[1:].split(",")[(i+1)*2])/2
        endPointY=float(glueData[1:].split(",")[(i+1)*2+1])/2
    except:
        endPointX=float(glueData[1:].split(",")[0])/2
        endPointY=float(glueData[1:].split(",")[1])/2
    ROI_Line1=GenerateTrendline(startPointX,startPointY,endPointX,endPointY,0,dBend,5)
    ROI.append(ROI_Line1)
    
GvTool.SetToolData("多项Blob工具_7133.可变折线ROI", ROI)
eLightBlob=GvVisionAssembly.GeBlobPolarity()
for i in range(0,count):
    GvTool.SetToolData("多项Blob工具_7133.ROI序列号",i)
    GvTool.SetToolData("多项Blob工具_7133.Blob极性",eLightBlob.eLightBlob.values[1])
    GvTool.SetToolData("多项Blob工具_7133.是否Blob填充",True)

bendAngle=[40,40,40,40,40,40,40,30,40]
if GvVar.GetVar("@bLeftOrRight"):
    pass
else:
    for i in range(0,len(bendAngle)):
        bendAngle[i]=-bendAngle[i]
print(bendAngle)

Pix=GvVar.GetVar("#dPose1_CalibPix_X")*2
GvVar.SetVar("#dRecheckPixel",Pix)
centerPoint=GvTool.GetToolData("基准二维向量生成工具_7127.二维向量")

ROI1=GvVisionAssembly.scGuiTrendlineEx()   
ROI2=GvVisionAssembly.scGuiTrendlineEx()
ROI3=GvVisionAssembly.scGuiTrendlineEx()   
polyline1 = GvVisionAssembly.scPolyline()
polyline2 = GvVisionAssembly.scPolyline()

for i in range(startIndex,count+startIndex):
    startPointX=(float(glueData[1:].split(",")[i*2])/2-centerPoint.GetX())*Pix
    startPointY=(float(glueData[1:].split(",")[i*2+1])/2-centerPoint.GetY())*Pix
    polyline1.AddVertex(GvVisionAssembly.sc2Vector(startPointX,startPointY))
    if i==startIndex or (i%5==0 and int(i//5)<int(count//5)) or (i%5==0 and int(i//5)==int(count//5) and (i%5)>2):
        polyline2.AddVertex(GvVisionAssembly.sc2Vector(startPointX,startPointY))
    if (i%5==0 and int(i//5)==int(count//5)) and (i%5)<=2:
        pass
    if i==count+startIndex-1:
        startPointX=(float(glueData[1:].split(",")[0])/2-centerPoint.GetX())*Pix
        startPointY=(float(glueData[1:].split(",")[1])/2-centerPoint.GetY())*Pix
        polyline2.AddVertex(GvVisionAssembly.sc2Vector(startPointX,startPointY))
        polyline1.AddVertex(GvVisionAssembly.sc2Vector(startPointX,startPointY))   

ROI1.SetPolyline(polyline1)  
ROI2.SetPolyline(polyline2)
ROI3.SetPolyline(polyline2)   
for i in range(0,count+1+startIndex):
    ROI1.SetBendAngle(i,dBend)
    ROI1.SetYlength(i,12*Pix)
for i in range(0,polyline2.GetVerticesNum()-1):
    ROI2.SetBendAngle(i,bendAngle[i])
    ROI3.SetBendAngle(i,bendAngle[i])
    ROI2.SetYlength(i,300*Pix)
    ROI3.SetYlength(i,4*Pix)
tempROI=GvTool.GetToolData("断胶检测异形胶检测工具_7149.检测区域")
tempROI[0].SetScTrendlineExCaliper(ROI1.GetTrendlineExCaliper())
GvTool.SetToolData("断胶检测异形胶检测工具_7149.检测区域",tempROI)

tempROI=GvTool.GetToolData("主检_6156.检测区域")
tempROI[0].SetScTrendlineExCaliper(ROI2.GetTrendlineExCaliper())
GvTool.SetToolData("主检_6156.检测区域",tempROI)
GvTool.SetToolData("coverage_6154.检测区域",tempROI)
GvTool.SetToolData("基准_6155.检测区域",tempROI)

tempROI=GvTool.GetToolData("手绘Coverage_7019.检测区域")
tempROI[0].SetScTrendlineExCaliper(ROI3.GetTrendlineExCaliper())
GvTool.SetToolData("手绘Coverage_7019.检测区域",tempROI)