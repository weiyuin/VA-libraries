#####数据获取
Count_SPEC=GvVar.GetVar("#nBlobOverLapROI")
ROI = GvTool.GetToolData("Blob工具_5634.圆形ROI")
blob=GvTool.GetToolData("Blob工具_5634.Blob结果轮廓")[0]
blobResult=GvTool.GetToolData("Blob工具_5634.Blob结果")[0]
bResult=GvTool.GetToolData("Blob工具_5634.执行结果")
#数据初始化
count=0
acircularity=999
###判断计算
#抓错判断
ROICenter=ROI.GetCenter()
for i in range(blob.GetVerticesNum()):
    dis=GvVisionAssembly.DistancePoint2Point(blob.GetVertex(i),ROICenter).distance
    if abs(dis-ROI.GetRadius())<1.5:
        count=count+1
#圆形度判断
acircularity=blobResult.BlobResult.acircularity
###
#结果判断
strErrMsg=""
Needle_Display=True
if count>=Count_SPEC or bResult==False:
    GvTool.SetToolData("Blob结果解析_5637.Acircularity",999)
    strErrMsg="校针NG！Blob工具抓错，请确认"
    Needle_Display=False
GvVar.SetVar("#strNeedle_Result",strErrMsg)
GvVar.SetVar("#bNeedle_Display",Needle_Display)