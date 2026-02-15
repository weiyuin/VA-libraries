from ScImageShow import ScImageShow
guiArray = GvVisionAssembly.GcScriptGuiArray()
#Kiểm tra và hiển thị kết quả hiệu chuẩn (calibration)
##########Lấy dữ liệu quá trình hiệu chuẩn
nCalibIndex = GvVar.GetVar("#nCalibIndex")
pointVec = GvTool.GetToolData("运动标定工具_5398.标定Mark点集")
PltX = GvTool.GetToolData("运动标定工具_5398.平台坐标X")
PltY = GvTool.GetToolData("运动标定工具_5398.平台坐标Y")
PltD = GvTool.GetToolData("运动标定工具_5398.平台坐标D")
bResult = GvTool.GetToolData("运动标定工具_5398.执行结果")
calibResult = GvTool.GetToolData("运动标定工具_5398.标定结果")
calib_error = GvTool.GetToolData("运动标定工具_5398.平移标定误差")
if bResult == True:
    nShowClr = 1
    calib_Msg = "标定OK"  # Hiệu chuẩn OK
else:
    nShowClr = 0
    calib_Msg = "标定NG"  # Hiệu chuẩn NG
strDirX = "X正方向：---"   # Hướng dương trục X: ---
strDirY = "Y正方向：---"   # Hướng dương trục Y: ---
ImageAngle = 0
###########
###########Hiển thị đường đi của các điểm Mark
if nCalibIndex < 1:
    point = pointVec[nCalibIndex][0]
    ScImageShow.ImagechowCrossVec(ScImageShow, guiArray, point, [0, 255, 0], 2)  # Hiển thị dấu chữ thập tại điểm
    ScImageShow.ImageShowTextXY(ScImageShow, guiArray, point.GetX(), point.GetY()+50, str(nCalibIndex+1), [0, 255, 0], 100, 0)
else:
    for i in range(len(pointVec)):
        point = pointVec[i][0]
        ScImageShow.ImagechowCrossVec(ScImageShow, guiArray, point, [0, 255, 0], 2)  # Hiển thị dấu chữ thập tại điểm
        ScImageShow.ImageShowTextXY(ScImageShow, guiArray, point.GetX(), point.GetY()+50, str(i+1), [0, 255, 0], 100, 0)
        if i > 0:
            P1 = pointVec[i-1][0]
            ScImageShow.ImageShowLineSegVec(ScImageShow, guiArray, P1, point, [255, 255, 0], 1)  # Nối hai điểm bằng đoạn thẳng
###########
###########Phán đoán sai số và hiển thị
if nCalibIndex == 8 and bResult:
    PixelX = calibResult.PixelX
    PixelY = calibResult.PixelY
    ImageAngle = calibResult.ImageAngle
    ###Xác định hướng trục
    M00 = calibResult.Matrix.GetElement(0, 0)
    if abs(M00) < 0.001:
        M00 = calibResult.Matrix.GetElement(0, 1)
    M11 = calibResult.Matrix.GetElement(1, 1)
    if abs(M11) < 0.001:
        M11 = calibResult.Matrix.GetElement(1, 1)
    if M00 < 0:
        strDirX = "X正方向：向左"    # Hướng dương trục X: sang trái
    else:
        strDirX = "X正方向：向右"    # Hướng dương trục X: sang phải
    if M11 < 0:
        strDirY = "Y正方向：向上"    # Hướng dương trục Y: lên trên
    else:
        strDirY = "Y正方向：向下"    # Hướng dương trục Y: xuống dưới
    #Phán đoán lỗi
    if calib_error > 2 * PixelX:
        nShowClr = 0
        calib_Msg = "标定NG，标定误差过大!误差:{calib_error:.5f},上限{USL}".format(calib_error=calib_error, USL=2*PixelX)
        # Hiệu chuẩn NG, sai số hiệu chuẩn quá lớn! Sai số:..., Giới hạn trên...
    if abs(PixelX - PixelY) / PixelX > 0.05:
        nShowClr = 0
        calib_Msg = "标定NG，像素误差当量过大(5%)!PixelX:{PixelX:.5f},PixelY:{PixelY:.5f}".format(PixelX=PixelX, PixelY=PixelY)
        # Hiệu chuẩn NG, sai số tương đương pixel quá lớn (>5%)!
###########
###########Hiển thị kết quả cuối cùng lên ảnh
if nShowClr == 0:
    clr = [255, 0, 0]   # Đỏ - NG
else:
    clr = [0, 255, 0]   # Xanh - OK
ScImageShow.ImageShowTextXY(ScImageShow, guiArray, 0, 0, calib_Msg, clr, 100, 0)
ScImageShow.ImageShowTextXY(ScImageShow, guiArray, 0, 100, "第{n}步".format(n=nCalibIndex+1), clr, 100, 0)  # Bước thứ n
ScImageShow.ImageShowTextXY(ScImageShow, guiArray, 0, 200, "当前机构坐标X:{X:.3f},Y:{Y:.3f},D:{D}".format(X=PltX, Y=PltY, D=PltD), clr, 100, 0)
# Tọa độ cơ cấu hiện tại X:..., Y:..., D:...
ScImageShow.ImageShowTextXY(ScImageShow, guiArray, 0, 300, strDirX, clr, 100, 0)
ScImageShow.ImageShowTextXY(ScImageShow, guiArray, 0, 400, strDirY, clr, 100, 0)
ScImageShow.ImageShowTextXY(ScImageShow, guiArray, 0, 500, "图像与轴夹角:{ImageAngle:.3f}°".format(ImageAngle=ImageAngle), clr, 100, 0)
# Góc giữa ảnh và trục: ...°
###########
GvGuiDataAgent.SetGraphicDisplay("标定", guiArray)  # Hiển thị ra view "标定"

GvVar.SetVar("#nCalibResult", nShowClr)