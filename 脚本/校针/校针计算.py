# Theo yêu cầu thực tế, kiểm tra độ tròn (circularity) của 9 điểm keo.
# Nếu độ tròn đạt yêu cầu thì tính giá trị trung bình tâm (centroid) của các điểm keo đạt để hiệu chỉnh kim (校针).
# Nếu số điểm đạt độ tròn nhỏ hơn ngưỡng cho phép thì hiệu chỉnh kim thất bại, cần thực hiện lại.

dAcircularity_SPEC = GvVar.GetVar("#dAcircularity_SPEC")  # Ngưỡng độ tròn (SPEC)
nInSpecCount = GvVar.GetVar("#nInSpecCount")              # Ngưỡng số lượng điểm đạt độ tròn
dataVec = GvTool.GetToolData("信息记录数组生成_5656.输出数组")  # Lấy dữ liệu các blob đã phát hiện

# Khởi tạo dữ liệu
Needle_Display = True
Needle_Result = ""
x = 0
y = 0
strSaveData = ""

# Đếm xem có bao nhiêu điểm có độ tròn nằm trong SPEC
Ok_count = 0
for i in range(0, len(dataVec)):
    tempAcircularity = dataVec[i].D
    # Lưu dữ liệu X, Y, độ tròn của từng điểm để ghi file sau
    strSaveData = strSaveData + "," + "{:.3f},{:.3f},{:.3f}".format(dataVec[i].X, dataVec[i].Y, dataVec[i].D)
    
    # Điều kiện đạt: độ tròn ≤ SPEC và ≥ 0.9 (gần tròn hoàn hảo)
    if tempAcircularity <= dAcircularity_SPEC and tempAcircularity >= 0.9:
        Ok_count = Ok_count + 1
        x = x + dataVec[i].X
        y = y + dataVec[i].Y

# Tính giá trị trung bình tọa độ tâm của các điểm đạt
if Ok_count >= 1:
    x = x / Ok_count
    y = y / Ok_count    

# Phán đoán kết quả hiệu chỉnh kim
if Ok_count >= nInSpecCount:
    Needle_Result = "校针OK! Có {} điểm đạt yêu cầu độ tròn".format(Ok_count)
else:
    Needle_Display = False
    Needle_Result = "校针NG! Chỉ có {} điểm đạt SPEC (yêu cầu ≥ {}), sai số keo lớn, vui lòng hiệu chỉnh kim lại!".format(Ok_count, nInSpecCount)

# Ghi kết quả ra biến toàn cục và đưa tọa độ trung bình vào tool vector
GvVar.SetVar("#bNeedle_Display", Needle_Display)
GvVar.SetVar("#strNeedle_Result", Needle_Result)
GvTool.SetToolData("图像坐标二维向量生成工具_5658.X分量", x)
GvTool.SetToolData("图像坐标二维向量生成工具_5658.Y分量", y)

# ============================= LƯU DỮ LIỆU HIỆU CHỈNH KIM =============================
import time
import os

def WriteFile(path, filename, header, data):
    # Nếu thư mục chưa tồn tại thì tạo mới
    if not os.path.exists(path):
        os.makedirs(path)
    # Nếu file chưa tồn tại thì tạo và ghi header, sau đó ghi data
    if not os.path.exists(path + filename):
        file = open(path + filename, "a", encoding="utf-8")
        file.write(header)
        file.write(data)
        file.close()
    else:
        # File đã tồn tại thì chỉ append data
        file = open(path + filename, "a", encoding="utf-8")
        file.write(data)
        file.close()

# Đường dẫn lưu file log dữ liệu hiệu chỉnh kim
path = "D:\\LusterCache\\Logs\\校针数据\\"

# Tên file theo ngày: 2025-11-20.csv
filename = time.strftime("%Y-%m-%d.csv", time.localtime())

# Lấy thời gian hiện tại đã được định dạng từ tool
time_str = GvTool.GetToolData("时间格式化工具_5651.格式化结果")

# Tạo header cho file CSV (chỉ ghi 1 lần khi file mới tạo)
header = "Time"
for i in range(9):
    header = header + ",{}-X,{}-Y,{}-Acircularity".format(i+1, i+1, i+1)
header = header + "\n"

# Dòng dữ liệu thực tế cần ghi (thời gian + dữ liệu 9 điểm)
data = "{:s}{:s}\n".format(time_str, strSaveData)    

# Ghi file
WriteFile(path, filename, header, data)