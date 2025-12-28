import datetime
from ScImageShow import ScImageShow
from ScMsgReport import ScMsgReport

ncalibrateindex = GvVar.GetVar("#nCaliNeedle")  # Lấy chỉ số bước hiệu chỉnh kim hiện tại (0-9)
strCurTime = GvVar.GetVar("#strCurTime")       # Lấy thời gian thực hiện (đã lưu từ trước)
strCurDate = datetime.datetime.now().strftime('%Y-%m-%d')  # Lấy ngày hệ thống hiện tại (YYYY-MM-DD)

# Đường dẫn thư mục lưu log dữ liệu hiệu chỉnh kim 9 điểm (theo ngày + thời gian bắt đầu)
filePath = "E:\\GVIMAGES\\Calibrate\\{date}\\{time}\\".format(date=strCurDate, time=strCurTime)  
offsetx = 0.0
offsety = 0.0

if ncalibrateindex == 0:
    # Bước đầu tiên (index = 0): Tạo thời gian chính xác (đến microsecond) khi bắt đầu quy trình 9 bước
    strCurTime = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    GvVar.SetVar("#strCurTime", strCurTime)   # Lưu thời gian này để tất cả 9 bước cùng dùng chung thư mục

elif ncalibrateindex == 9:
    # Bước cuối (index = 9): Đã hoàn thành đủ 9 vị trí → tính toán độ lệch trung bình để bù kim
    centerpos = GvTool.GetToolData("数组生成工具_5636.输出数组")  # Mảng chứa kết quả của 9 lần chụp
    num = 0 
    totalx = 0.0
    totaly = 0.0

    # Lặp qua dữ liệu của 9 bước đã thực hiện
    for i in range(0, 9):
        Eccentricity = centerpos[i].D  # Lấy giá trị độ lệch tâm (Eccentricity) ở bước i

        # Ghi log từng bước vào file CSV (dễ dàng trace và phân tích sau này)
        ScMsgReport.RecordMsgFolder(filePath, "calibrate.csv", 
            "pos{},{:.3f},{:.3f},{:.3f}".format(i+1, centerpos[i].X, centerpos[i].Y, centerpos[i].D))

        # Nếu độ lệch tâm < 100 → Vision đánh giá là vòng tròn đủ tốt (càng gần 0 càng tròn)
        if Eccentricity < 100:
            num = num + 1               # Đếm số điểm đạt tiêu chuẩn
            totalx = totalx + centerpos[i].X
            totaly = totaly + centerpos[i].Y
                         
    # Tính độ bù trung bình
    if num == 0:                    # Không có điểm nào đạt → không bù
        offsetx = 0.0
        offsety = 0.0
    else:
        offsetx = totalx / num      # Trung bình X của các điểm đạt
        offsety = totaly / num      # Trung bình Y của các điểm đạt

    print(offsetx)
    print(offsety)

    # Lưu độ bù tương đối so với vị trí tham chiếu đầu tiên
    GvVar.SetVar("#doffsetx", GvVar.GetVar("#dFristPosX") - offsetx)   
    GvVar.SetVar("#doffsety", GvVar.GetVar("#dFristPosY") - offsety)          

# ====================== HIỂN THỊ ĐỒ HỌA LÊN ẢNH ======================
guiArray = GvVisionAssembly.GcScriptGuiArray()  # Khởi tạo mảng GUI để vẽ lên ảnh

# Nếu Blob tool chạy thành công → vẽ contour của điểm keo/kim lên ảnh
if GvTool.GetToolData("Blob工具_5634.执行结果"):
    VecVec2 = GvTool.GetToolData("Blob结果解析_5637.轮廓边界点")  # Tập hợp điểm biên của blob
    ScImageShow.ImageShowPolyline(ScImageShow, guiArray, VecVec2, clrLineColor=[0,255,0], nLineWidth=2)
GvGuiDataAgent.SetGraphicDisplay("校针", guiArray)