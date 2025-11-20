#####Lấy dữ liệu
Count_SPEC = GvVar.GetVar("#nBlobOverLapROI")
ROI = GvTool.GetToolData("Blob工具_5634.圆形ROI")
blob = GvTool.GetToolData("Blob工具_5634.Blob结果轮廓")[0]
blobResult = GvTool.GetToolData("Blob工具_5634.Blob结果")[0]
bResult = GvTool.GetToolData("Blob工具_5634.执行结果")
#Khởi tạo dữ liệu
count = 0
acircularity = 999
###Phán đoán và tính toán
#Phán đoán việc Blob bắt sai (bắt không đúng vòng tròn chuẩn)
ROICenter = ROI.GetCenter()
for i in range(blob.GetVerticesNum()):
    dis = GvVisionAssembly.DistancePoint2Point(blob.GetVertex(i), ROICenter).distance
    if abs(dis - ROI.GetRadius()) < 1.5:
        count = count + 1
#Phán đoán độ tròn
acircularity = blobResult.BlobResult.acircularity
###
#Phán đoán kết quả cuối cùng
strErrMsg = ""
Needle_Display = True
if count >= Count_SPEC or bResult == False:
    GvTool.SetToolData("Blob结果解析_5637.Acircularity", 999)
    strErrMsg = "校针NG！Blob工具抓错，请确认"  # NG hiệu chỉnh kim! Blob tool bắt sai, vui lòng kiểm tra lại
    Needle_Display = False
GvVar.SetVar("#strNeedle_Result", strErrMsg)
GvVar.SetVar("#bNeedle_Display", Needle_Display)