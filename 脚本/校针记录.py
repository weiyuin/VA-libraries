import datetime
from ScImageShow import ScImageShow
from ScMsgReport import ScMsgReport

ncalibrateindex = GvVar.GetVar("#nCaliNeedle")  # Lấy chỉ số bước hiệu chỉnh kim hiện tại
strCurTime = GvVar.GetVar("#strCurTime")       # Lấy thời gian thực hiện (đã lưu trước đó)
strCurDate = datetime.datetime.now().strftime('%Y-%m-%d')  # Lấy ngày hệ thống hiện tại (định dạng YYYY-MM-DD)

# Đường dẫn lưu file log dữ liệu hiệu chỉnh kim (theo ngày + thời gian bắt đầu quy trình)
filePath = "E:\\GVIMAGES\\Calibrate\\{date}\\{time}\\".format(date=strCurDate, time=strCurTime)  
offsetx = 0.0
offsety = 0.0

if ncalibrateindex == 0:
    strCurTime = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    GvVar.SetVar("#strCurTime", strCurTime)

elif ncalibrateindex == 9:
    # Bước 9: Khi đã hoàn thành đủ 9 vị trí → tính toán độ lệch trung bình để hiệu chỉnh kim
    centerpos = GvTool.GetToolData("数组生成工具_5636.输出数组")  # Mảng chứa kết quả 9 lần chụp (X, Y, D của từng blob)
    num = 0 
    totalx = 0.0
    totaly = 0.0

    # Lặp qua 9 bước đã thực hiện
    for i in range(0, 9):
        Eccentricity = centerpos[i].D  # Độ lệch tâm (Eccentricity) của blob ở bước i

        # Ghi log dữ liệu từng bước vào file CSV (dùng để trace và phân tích sau này)
        ScMsgReport.RecordMsgFolder(filePath, "calibrate.csv", 
            "pos{},{},{},{}".format(i+1, centerpos[i].X, centerpos[i].Y, centerpos[i].D))

        # Nếu độ lệch tâm < 100 → Vision coi là vòng tròn đủ tốt (càng gần 0 càng tròn hoàn hảo)
        if Eccentricity < 100:
            num = num + 1          # Đếm số điểm đạt yêu cầu
            totalx = totalx + centerpos[i].X
            totaly = totaly + centerpos[i].Y
                         
    # Tính toán độ lệch trung bình (offset) để bù kim
    if num == 0:               # Không có điểm nào đạt → không bù, giữ offset = 0
        offsetx = 0.0
        offsety = 0.0
    else:
        offsetx = totalx / num   # Trung bình X của các điểm đạt
        offsety = totaly / num   # Trung bình Y của các điểm đạt

    print(offsetx)
    print(offsety)

    # Lưu độ bù tương đối so với vị trí đầu tiên (vị trí tham chiếu)
    GvVar.SetVar("#doffsetx", GvVar.GetVar("#dFristPosX") - offsetx)   
    GvVar.SetVar("#doffsety", GvVar.GetVar("#dFristPosY") - offsety)          

# ====================== HIỂN THỊ LÊN ẢNH ======================
# Khởi tạo mảng GUI để vẽ đồ họa lên ảnh
guiArray = GvVisionAssembly.GcScriptGuiArray()

# Nếu Blob tool chạy thành công → vẽ contour của kim/điểm keo lên ảnh
if GvTool.GetToolData("Blob工具_5634.执行结果"):
    VecVec2 = GvTool.GetToolData("Blob结果解析_5637.轮廓边界点")  # Lấy tập hợp điểm biên của blob
    ScImageShow.ImageShowPolyline(ScImageShow, guiArray, VecVec2, clrLineColor=[0,255,0], nLineWidth=2)
    # Vẽ đường viền màu xanh lá, độ dày 2 pixel

# Cập nhật hiển thị view "校针" (hiệu chỉnh kim)
GvGuiDataAgent.SetGraphicDisplay("校针", guiArray)