import math
import GvVisionAssembly
from ScImageShow import ScImageShow

R_INNER = 350.0 
R_OUTER = 500.0 

guiArray = GvVisionAssembly.GcScriptGuiArray()

# Lấy kết quả Blob để tìm tâm (CX, CY)
if GvTool.GetToolData("Blob工具_003.执行结果"):
    blobs_contour = GvTool.GetToolData("Blob工具_003.Blob结果轮廓")
    if len(blobs_contour) > 0:
        main_contour = blobs_contour[0]
        sum_x = 0.0
        sum_y = 0.0
        num_pts = main_contour.GetVerticesNum()
        for k in range(num_pts):
            pt = main_contour.GetVertex(k)
            sum_x += pt.GetX()
            sum_y += pt.GetY()
        if num_pts > 0:
            cx = sum_x / num_pts
            cy = sum_y / num_pts

center_vec = GvVisionAssembly.sc2Vector(cx, cy)

# ROI CHIA 360 PHẦN
# Vẽ 2 đường tròn biên (Trong và Ngoài)
start_rad = GvVisionAssembly.scRadian(0.0)
span_rad = GvVisionAssembly.scRadian(math.pi * 2)

# Tạo vòng cung trong
arc_inner = GvVisionAssembly.scCircularArc(center_vec, R_INNER, start_rad, span_rad)
# Tạo vòng cung ngoài
arc_outer = GvVisionAssembly.scCircularArc(center_vec, R_OUTER, start_rad, span_rad)
ScImageShow.ImagechowArc(ScImageShow,guiArray, arc_inner, [0, 255, 0], nLineWidth=3)
ScImageShow.ImagechowArc(ScImageShow,guiArray, arc_outer, [0, 255, 0], nLineWidth=3)

for i in range(360):
    angle_rad = math.radians(i)
    
    p_in_x = cx + R_INNER * math.cos(angle_rad)
    p_in_y = cy + R_INNER * math.sin(angle_rad)
    
    p_out_x = cx + R_OUTER * math.cos(angle_rad)
    p_out_y = cy + R_OUTER * math.sin(angle_rad)
    
    p_in = GvVisionAssembly.sc2Vector(p_in_x, p_in_y)
    p_out = GvVisionAssembly.sc2Vector(p_out_x, p_out_y)
    
    line_seg = GvVisionAssembly.scLineSeg(p_in, p_out)
    
    ScImageShow.ImageShowLineSeg(ScImageShow,guiArray, line_seg, [0, 255, 255], nLineWidth=1)
GvGuiDataAgent.SetGraphicDisplay("360个检测框", guiArray)