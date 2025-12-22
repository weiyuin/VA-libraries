from ScImageShow import ScImageShow
import GvVisionAssembly

# 1. Lấy dữ liệu hiện tại
blob_Count = GvTool.GetToolData("Blob工具_012.结果个数")
Pos_Center = GvTool.GetToolData("多圆多线查找工具_005.中点_007")
# Lấy 4 điểm để vẽ 4 đoạn thẳng (Ví dụ đoạn A từ Point5 đến Point8)
p5 = GvTool.GetToolData("多圆多线查找工具_005.交点_005")
p8 = GvTool.GetToolData("多圆多线查找工具_005.交点_008")
p9 = GvTool.GetToolData("多圆多线查找工具_005.交点_009")
p6 = GvTool.GetToolData("多圆多线查找工具_005.交点_006")

# Lưu 4 đoạn thẳng (Lưu 4 cặp tọa độ X|Y của 4 điểm p5,p8,p9,p6)
s_line = GvVar.GetVar("#strLine_Coords")
s_line += "{:.2f}|{:.2f}|{:.2f}|{:.2f}|{:.2f}|{:.2f}|{:.2f}|{:.2f};".format(
    p5.GetX(), p5.GetY(), p8.GetX(), p8.GetY(), p9.GetX(), p9.GetY(), p6.GetX(), p6.GetY())
GvVar.SetVar("#strLine_Coords", s_line)

# 3. Khởi tạo mảng đồ họa và Vẽ lại toàn bộ lịch sử
guiArray = GvVisionAssembly.GcScriptGuiArray()

# Vẽ lại tất cả các đoạn thẳng
for ln in GvVar.GetVar("#strLine_Coords").strip(";").split(";"):
    if ln:
        d = ln.split("|")
        v5 = GvVisionAssembly.sc2Vector(float(d[0]), float(d[1]))
        v8 = GvVisionAssembly.sc2Vector(float(d[2]), float(d[3]))
        v9 = GvVisionAssembly.sc2Vector(float(d[4]), float(d[5]))
        v6 = GvVisionAssembly.sc2Vector(float(d[6]), float(d[7]))
        # Vẽ 4 cạnh nối các điểm
        ScImageShow.ImageShowLineSegVec(ScImageShow, guiArray, v5, v8, [0, 255, 0], 2, 1) # Cạnh A
        ScImageShow.ImageShowLineSegVec(ScImageShow, guiArray, v5, v9, [0, 255, 0], 2, 1) # Cạnh B
        ScImageShow.ImageShowLineSegVec(ScImageShow, guiArray, v8, v6, [0, 255, 0], 2, 1) # Cạnh C
        ScImageShow.ImageShowLineSegVec(ScImageShow, guiArray, v9, v6, [0, 255, 0], 2, 1) # Cạnh D

# 4. Hiển thị
GvGuiDataAgent.SetGraphicDisplay("View-1", guiArray)