import json
import GvGluePathAOI

# Lấy đối tượng xử lý kết quả
result_opr = GvGluePathAOI.result_operator()

# 1. Gộp lỗi (nếu có)
str_1 = GvTool.GetToolData("主胶路检测_4683.缺陷序列化结果")

# Chuyển dữ liệu từ chuỗi JSON về đối tượng Python
str_1 = json.loads(str_1)

# 3. Tính toán lại lỗi
thred_miss = GvVar.GetVar("@dMissingThreshold")           # ngưỡng thiếu keo
thred_break = GvVar.GetVar("@dGlueBreakThreshold")        # ngưỡng đứt keo
thred_hole = GvVar.GetVar("@dHoleThreshold")              # ngưỡng lỗ hổng
thred_coverage = GvVar.GetVar("@dGlueCoverageThreshold")  # ngưỡng độ phủ keo


# Hiển thị
guiArray = GvVisionAssembly.GcScriptGuiArray()
gui_opr = GvGluePathAOI.glue_display()
guiArray = gui_opr.show_general_data_Ex(
    guiArray, str_out,
    font_size=70,
    offset_x=20,
    offset_y=20,
    line_space=10,
    line_width=2,
    bShowMinWidth=True
)

# Gửi dữ liệu hiển thị lên giao diện
GvGuiDataAgent.SetGraphicDisplay("new tool 复检", guiArray)