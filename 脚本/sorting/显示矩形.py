from ScImageShow import ScImageShow
import GvVisionAssembly

# 1. Lấy dữ liệu hiện tại
blob_Count = GvTool.GetToolData("Blob工具_012.结果个数")
Pos_Center = GvTool.GetToolData("多圆多线查找工具_005.中点_007")

# 2. Cập nhật chuỗi lưu trữ lịch sử (Gom tọa độ vào GvVar)
# Lưu hình chữ nhật nếu NG
if blob_Count != 3:
    s_rect = GvVar.GetVar("#strNG_Coords")
    s_rect += "{:.2f}|{:.2f};".format(Pos_Center.GetX(), Pos_Center.GetY())
    GvVar.SetVar("#strNG_Coords", s_rect)

# 3. Khởi tạo mảng đồ họa và Vẽ lại toàn bộ lịch sử
guiArray = GvVisionAssembly.GcScriptGuiArray()

# Vẽ lại tất cả hình chữ nhật NG
for pt in GvVar.GetVar("#strNG_Coords").strip(";").split(";"):
    if pt:
        d = pt.split("|")
        vec = GvVisionAssembly.sc2Vector(float(d[0]), float(d[1]))
        ScImageShow.ImageShowRecCenter(ScImageShow, guiArray, vec, 100, 100, [255, 0, 0], 2)

# 4. Hiển thị
GvGuiDataAgent.SetGraphicDisplay("View-1", guiArray)