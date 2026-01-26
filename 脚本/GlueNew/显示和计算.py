import json
import GvGluePathAOI
import time
from ScImageShow import ScImageShow
guiArray = GvVisionAssembly.GcScriptGuiArray()

if GvTool.GetToolData("Blob工具_021.执行结果"):
    polyLine = GvTool.GetToolData("Blob工具_021.Blob结果轮廓")
    try:
        num = len(polyLine)
        for i in range(num):
            print(1)
            ScImageShow.ImageShowPolyline(ScImageShow, guiArray, polyLine[i].GetVertices(), clrLineColor=[0, 255, 0], nLineWidth=1)
    except:
        pass
# Hiển thị Khu vực NG CoverageShift
if GvTool.GetToolData("Blob工具_026.执行结果") and GvTool.GetToolData("Blob工具_026.总像素数") > 0:
    polyLine = GvTool.GetToolData("Blob工具_026.Blob结果轮廓")
    try:
        num = len(polyLine)
        for i in range(num):
            ScImageShow.ImageShowPolyline(ScImageShow, guiArray, polyLine[i].GetVertices(), clrLineColor=[255, 0, 0], nLineWidth=3)
    except:
        pass

result_opr = GvGluePathAOI.result_operator()
str_out1 = json.loads(GvTool.GetToolData("主胶路_015.缺陷序列化结果"))
str_out2 = json.loads(GvTool.GetToolData("CoverageShift_024.缺陷序列化结果")) # Coverage

d_LSL_Width = GvVar.GetVar("#LSLGlueWitdth")
d_USL_Width = GvVar.GetVar("#USLGlueWitdth")
d_LSL_Coverage = GvVar.GetVar("#LSLGlueCovarageShift")
d_USL_Coverage = GvVar.GetVar("#USLGlueCovarageShift")

# Cap nhat SPEC va dua theo spec tinh toan loi width
num_region1 = str_out1["base_info"]["region_number"]
for i in range(num_region1):
    region_key = "region_{}".format(i)
    obj_width = str_out1["region_info"][region_key]["region_info_width"]
    if obj_width["enable"] == True:
        obj_width["lower_spec"] = d_LSL_Width
        obj_width["upper_spec"] = d_USL_Width
        if obj_width["min_val"] < d_LSL_Width or obj_width["max_val"] > d_USL_Width:
            obj_width["error_code"] = 1
        else:
            obj_width["error_code"] = 0
    GvGluePathAOI.check_region_errorcode(str_out1, region_key)
str_out1 = GvGluePathAOI.check_errorcode(str_out1)

## Cap nhat SPEC va dua theo spec tinh toan loi coverageShift
try:
    pixel_total = GvTool.GetToolData("Blob工具_021.总像素数")
    pixel_ng = GvTool.GetToolData("Blob工具_026.总像素数")
    coverage = 1.0 - (pixel_ng / pixel_total) if pixel_total > 0 else 0.0
except:
    coverage = 0.0

num_region2 = str_out2["base_info"]["region_number"]
for i in range(num_region2):
    region_key = "region_{}".format(i)
    obj_areashift = str_out2["region_info"][region_key]["region_info_areashift"]
    if obj_areashift["enable"] == True:
        obj_areashift["lower_spec"] = d_LSL_Coverage
        obj_areashift["upper_spec"] = d_USL_Coverage
str_out2 = result_opr.data_replace(str_out2, [coverage], [0], 5)
str_out = result_opr.merge(str_out1, str_out2)

#统计
nBrokenNG = GvVar.GetVar("#nBrokenNG")
nWidthNG = GvVar.GetVar("#nWidthNG")
nShiftNG = GvVar.GetVar("#nShiftNG")
nTotal = GvVar.GetVar("#nTotal")

nTotal = nTotal + 1

is_broken_ng = False
is_width_ng = False
is_shift_ng = False

# Check NG broken
if str_out["detection_gap_info"]["num"] > 0:
    is_broken_ng = True

# check NG Width va Coverage Shift ---
num_region_total = str_out["base_info"]["region_number"]
for i in range(num_region_total):
    region_key = "region_{}".format(i)
    region_info = str_out["region_info"][region_key]
    
    # Check Width NG
    if region_info["region_info_width"]["error_code"] == 1:
        is_width_ng = True
        
    # Check Coverage Shift NG
    if region_info["region_info_areashift"]["error_code"] == 1:
        is_shift_ng = True

# cap nhat bien
if is_broken_ng: nBrokenNG += 1
if is_width_ng: nWidthNG += 1
if is_shift_ng: nShiftNG += 1

GvVar.SetVar("#nBrokenNG", nBrokenNG)
GvVar.SetVar("#nWidthNG", nWidthNG)
GvVar.SetVar("#nShiftNG", nShiftNG)
GvVar.SetVar("#nTotal", nTotal)

#显示
gui_opr = GvGluePathAOI.glue_display()
gui_opr.set_show_mode(True)

# Check NoGlue
if GvTool.GetToolData("Blob工具_021.总像素数") > 6000:
    noGlueState = 1
else:
    noGlueState = 0
GvVar.SetVar("#nNoGlueState", noGlueState)
gui_opr.set_noglue_state(noGlueState)

guiArray = gui_opr.show_general_data_Ex(guiArray, str_out, font_size=80, offset_x=0, offset_y=0, line_space=5, line_width=3, bShowMinWidth=True, show_OK=True)
GvGuiDataAgent.SetGraphicDisplay("复检", guiArray)