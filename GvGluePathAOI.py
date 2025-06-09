# ------------------------------------------------------------------
# Tên tệp:           GvGluePathAOI
# Tác giả:           Hao Zhao, Jun Ling, Huan Wang
# Phiên bản:         ver0_4
# Ngày tạo:          2023/11/21
# Mô tả:             Dùng cho kiểm tra tiêu chuẩn hóa AirPods, lưu trữ và hiển thị dữ liệu
#                    glue_display:        Lớp hiển thị tiêu chuẩn
#                    detection_operator： Lớp tính toán lại lỗi (dùng khi có yêu cầu tùy chỉnh từ khách hàng)
#                    database_operator：  Lớp lưu trữ dữ liệu

# History:
#       <tác giả>        <phiên bản>     <thời gian>   <mô tả>
#       Huan Wang        ver0_1         2023/10/15    Phiên bản đầu tiên
#       Jun Ling         ver0_2         2023/11/15    Sửa logic kích hoạt lưu trữ dữ liệu, thêm tính năng thống kê dữ liệu
#       Hao Zhao         ver0_3         2023/11/15    Thêm hiển thị tiêu chuẩn hóa, làm mới dữ liệu kiểm tra, thêm ví dụ và mẫu chuẩn
#       Hao Zhao         ver0_4         2023/11/21    Tương thích với vùng mở rộng chỉ kiểm tra tỷ lệ keo, bỏ qua phần khác
#       Hao Zhao         ver0_5         2023/11/22    Sửa phương pháp so sánh glue_missing
#       Huan Wang        ver0_6         2023/12/05    Thêm tính năng tải dữ liệu lên MES
#       Hao Zhao         ver0_7         2023/12/09    Chỉnh sửa nội dung hiển thị theo yêu cầu số 37; sửa hàm Add (thừa/thiếu keo, đứt keo, chiều dài keo); hỗ trợ gộp vùng lỗi với số lượng khác nhau
#       Huan Wang        ver0_8         2023/12/17    Thêm tính năng tải shiftX/shiftY lên MES
#       Hao Zhao         ver0_10        2024/1/03     Chỉnh sửa hiển thị theo yêu cầu số 37: không hiển thị COF trong lý do NG, thêm tùy chọn tắt hiển thị chiều dài keo tối thiểu/tối đa, COF hiển thị OK
#       Huan Wang        ver0_11        2024/1/03     Khi tải lên MES, sửa logic chỉ tải dữ liệu chiều rộng tương ứng NG
#       Hao Zhao         ver0_12        2024/1/22     Hợp nhất chức năng tải dữ liệu lên của dự án 36 và 37
#       Hao Zhao         ver1_13        2024/3/22     Thêm hiển thị cho dự án 37: hiển thị thông tin thường dùng như kết quả vật liệu, SN, lý do NG, chiều rộng keo ngắn nhất, thông tin chi tiết (vùng nhắc nhở)
#       Huan Wang        ver1_14        2024/4/8      Sửa số lượng chữ số thập phân khi tải dữ liệu lên
#       Hao Zhao         ver1_15        2024/4/27     Bỏ tiền tố "cof_" trong hạng mục kiểm tra COF khi tải lên; sửa glue missing thành glue area cho dự án 37; sửa lỗi không hiển thị lỗi tràn keo do thống kê vùng bị lỗi
#       Hao Zhao         ver1_16        2024/7/31     1. Bỏ cách dùng Gross SPEC cho tool 0.5 trong phần tải lên (gợi ý phần mềm tương lai truy cập)
#                                                     2. Bỏ các biến điều khiển ít dùng trong hiển thị, gộp các biến trùng chức năng
#                                                     3. Thêm hàm hiển thị mới, tương thích thông tin cơ bản, vùng kiểm tra, hiển thị NG, đơn giản hóa quá trình hiển thị
#                                                     4. Thêm hàm trả về kết quả kiểm tra, không cần hiểu cấu trúc dữ liệu keo vẫn có thể lấy kết quả, thuận tiện cho việc lấy đường dẫn lưu ảnh
#                                                     5. Thêm hàm xử lý dữ liệu tải lên, đảm bảo định dạng tải phù hợp với xử lý nội bộ của dự án, đơn giản hóa dự án
#       Hao Zhao         ver1_17        2024/11/08    1. Sửa lỗi dùng sai error_code trong hiển thị biên dạng tràn keo
#                                                     2. Bỏ logic đánh giá kết quả khi tải lại dữ liệu reflow
#                                                     3. Cập nhật ví dụ sử dụng
#       Hao Zhao         ver1_18        2024/11/18    1. Thêm hiển thị hạng mục kiểm tra NoGlue
#                                                     2. Thêm trả về kết quả kiểm tra NoGlue
#                                                     3. Thống nhất hiển thị NG khi phát hiện NG từ công cụ, thống nhất hiển thị GlueMissing
#                                                     4. Thêm chức năng ẩn hiển thị lỗi đứt keo
#       Hao Zhao         ver1_19        2024/11/30    1. Thêm hàm `get_all_detection_result` trả về kết quả tất cả hạng mục kiểm tra, hỗ trợ tùy chỉnh hiển thị về sau
#                                                     2. Thêm hàm hiển thị `show_detection_result`, phù hợp mẫu hiển thị mới của khách hàng 39
#                                                     3. Thêm hàm `ShowFeatureVec`, hỗ trợ hiển thị đặc trưng nhiều cavity
#       Hao Zhao         ver1_20        2024/12/05    1. Thêm hàm `get_mes_data_Ex`, đơn giản hóa chế độ tải dữ liệu lên cho khách hàng 39
# ------------------------------------------------------------------
# ------------------------------------------------------------------
# ví dụ
# Logic chính
"""
import json
import GvGluePathAOI

# Lấy đối tượng xử lý kết quả
result_opr = GvGluePathAOI.result_operator()

# 1. Gộp lỗi (nếu có)
str_1 = GvTool.GetToolData("主胶路检测_4683.缺陷序列化结果")  # Kết quả lỗi từ kiểm tra đường keo chính
str_2 = GvTool.GetToolData("主胶路覆盖率检测_4692.缺陷序列化结果")  # Kết quả lỗi từ kiểm tra độ phủ keo

# Chuyển dữ liệu từ chuỗi JSON về đối tượng Python
str_1 = json.loads(str_1)
str_2 = json.loads(str_2)

# Gộp dữ liệu lỗi
str_out = result_opr.merge(str_1, str_2)

# Thay đổi dữ liệu (nếu cần)
str_out = result_opr.data_replace(str_out, [0.2], [0], 4)
# Giải thích:
# Đối với các lỗi lỗ hổng/tỷ lệ keo:
#     nếu sửa dữ liệu thì OK là 0, NG là 1;
# Đối với các lỗi khác:
#     nếu sửa dữ liệu thì OK là 0, NG là 2
# (nếu chỉ sửa lỗ hổng và tỷ lệ keo thì không cần gọi lại hàm tính toán lại lỗi, còn các lỗi khác thì bắt buộc phải tính lại)

# 2. Thêm lỗi (nếu có)
# str_3 = GvTool.GetToolData("溢胶检测_4693.缺陷序列化结果")  # Kết quả lỗi từ kiểm tra tràn keo
# str_out = result_opr.add(str_out, str_3)

# Xem tạm lỗi đầu ra (ví dụ in ra mã lỗi)
# str_outtemp = json.loads(str_1)
# print(str_outtemp["base_info"]["error_code"])

# 3. Tính toán lại lỗi
thred_miss = GvVar.GetVar("@dMissingThreshold")           # ngưỡng thiếu keo
thred_break = GvVar.GetVar("@dGlueBreakThreshold")        # ngưỡng đứt keo
thred_hole = GvVar.GetVar("@dHoleThreshold")              # ngưỡng lỗ hổng
thred_coverage = GvVar.GetVar("@dGlueCoverageThreshold")  # ngưỡng độ phủ keo

# Vùng cần hiển thị và sửa lỗi
list_region = [0, 1, 2, 3, 4, 5]

# Tính toán lại kết quả lỗi theo các ngưỡng
str_out = result_opr.recalculate_result(str_out, thred_miss, thred_break, thred_hole, thred_coverage, list_region)
# ----------------------------------------------------------------

# Hiển thị
guiArray = GvVisionAssembly.GcScriptGuiArray()
gui_opr = GvGluePathAOI.glue_display()

# Cấu hình vùng cần hiển thị
################ Cách 1

# Hiển thị thông tin tổng quát
guiArray = gui_opr.show_general_data(guiArray, str_out, list_region, 40, 20, 20, 0, 2)

# Hiển thị vùng ROI kiểm tra
guiArray = gui_opr.show_detetion_Region(guiArray, str_out, list_region)

# Hiển thị thông tin lỗi NG
guiArray = gui_opr.show_NG_data(guiArray, str_out, 0, 20, -450, 50, 0)
guiArray = gui_opr.show_NG_data(guiArray, str_out, 1, 20, -450, -40, 0)
guiArray = gui_opr.show_NG_data(guiArray, str_out, 2, 20, -450, -40, 0)
guiArray = gui_opr.show_NG_data(guiArray, str_out, 3, 20, -300, -200, 0)
guiArray = gui_opr.show_NG_data(guiArray, str_out, 4, 20, -100, -200, 0)
guiArray = gui_opr.show_NG_data(guiArray, str_out, 5, 20, 100, -40, 0)

################ Cách 2

# Hiển thị toàn bộ: tiêu đề, thông tin NG, vùng kiểm tra
guiArray = gui_opr.show_general_data_Ex(
    guiArray, str_out,
    font_size=70,
    offset_x=20,
    offset_y=20,
    line_space=10,
    line_width=2,
    bShowMinWidth=True
)
# ----------------------------------------------------------------

# Lưu trữ dữ liệu
db_opr = GvGluePathAOI.database_operator()
str_file_path = GvVar.GetVar("@filePath")            # Đường dẫn lưu file dữ liệu
str_path_cap = GvVar.GetVar("#strImgPathCapSnd")     # Đường dẫn ảnh chụp kết quả
str_path_src = GvVar.GetVar("#strImgPathSrcSnd")     # Đường dẫn ảnh gốc

# Ghi dữ liệu vào tệp
db_opr.record_datas(str_out, str_file_path, str_path_cap, str_path_src, 1)

# Gửi dữ liệu hiển thị lên giao diện
GvGuiDataAgent.SetGraphicDisplay("new tool 复检", guiArray)
"""




import json
import sqlite3
import time
import datetime
import GvVisionAssembly
from ScImageShow import ScImageShow
import os
import shutil
import csv
import math
from ScMsgReport import ScMsgReport

#用于视图特征显示支持点，点集，线，线段，圆，矩形，仿射矩形，多边形，多边形集合
#featureVec 显示特征，不关心类型，按格式[[特征1,特征1工具结果],[特征2,特征2工具结果]]格式填入即可
#clr 显示颜色，0红色，1绿色
def ShowFeatureVec(guiArray,featureVec,clr,line_width=2):
    if clr==1:
        show_clr=[0,255,0]
    if clr==0:
        show_clr=[255,0,0]
    if len(featureVec)==0:
        return guiArray
    else:
        line=GvVisionAssembly.scLine()
        lineSeg=GvVisionAssembly.scLineSeg()
        circle=GvVisionAssembly.scCircle()
        point=GvVisionAssembly.sc2Vector()
        pointVec=GvVisionAssembly.sc2VectorVec()
        polyLine=GvVisionAssembly.scPolyline()
        polyLineVec=GvVisionAssembly.scPolylineVec()
        rect=GvVisionAssembly.scRect()
        AffineRect=GvVisionAssembly.scAffineRect()
        for n in range(0,len(featureVec)):
            if type(featureVec[n][0])==type(line) and featureVec[n][1]==True:#直线
                # print("line")
                ScImageShow.ImageShowLine(ScImageShow,guiArray,featureVec[n][0],show_clr,line_width)#显示直线
            if type(featureVec[n][0])==type(lineSeg)and featureVec[n][1]==True:#线段
                # print("lineSeg")
                ScImageShow.ImageShowLineSeg(ScImageShow,guiArray,featureVec[n][0],show_clr,line_width)#显示线段
            if type(featureVec[n][0])==type(circle)and featureVec[n][1]==True:#圆
                # print("circle")
                ScImageShow.ImageShowCircle(ScImageShow,guiArray,featureVec[n][0].GetCenter(), featureVec[n][0].GetRadius(), show_clr,line_width)#显示一个圆
            if type(featureVec[n][0])==type(point)and featureVec[n][1]==True:#点
                # print("point")
                ScImageShow.ImagechowCrossVec(ScImageShow,guiArray,featureVec[n][0],show_clr, line_width)#显示十字交点
            if type(featureVec[n][0])==type(pointVec)and featureVec[n][1]==True:#点集
                # print("pointVec")
                for i in range(0,len(featureVec[n][0])):
                    ScImageShow.ImagechowCrossVec(ScImageShow,guiArray,featureVec[n][0][i],show_clr, line_width)#显示十字交点
            if type(featureVec[n][0])==type(polyLine)and featureVec[n][1]==True:#多边形
                # print("polyLine")
                ScImageShow.ImageShowPolyline(ScImageShow,guiArray,featureVec[n][0].GetVertices(), show_clr, line_width)
            if type(featureVec[n][0])==type(polyLineVec)and featureVec[n][1]==True:#多边形集
                # print("polyLineVec")
                for i in range(0,len(featureVec[n][0])):
                    ScImageShow.ImageShowPolyline(ScImageShow,guiArray,featureVec[n][0][i].GetVertices(), show_clr, line_width)
            if type(featureVec[n][0])==type(rect)and featureVec[n][1]==True:#矩形
                # print("rect")
                ScImageShow.ImageShowRec(ScImageShow, guiArray, featureVec[n][0],show_clr,line_width,"")
            if type(featureVec[n][0])==type(AffineRect)and featureVec[n][1]==True:#仿射矩形
                # print("AffineRect")
                ScImageShow.ImageShowAffRec(ScImageShow, guiArray, featureVec[n][0], show_clr,line_width,"")
        return guiArray

def imageShowPolyline(VectorVec,clrLineColor = [0, 255, 0],nLineWidth = 1):
    guiStyle = GvVisionAssembly.GsScriptGuiStyle()
    guiStyle.bVisible = True
    guiStyle.nLineStyle = 1
    guiStyle.nLineWidth = nLineWidth
    guiStyle.clrLineColor = clrLineColor
    guiStyle.bLabelVisible = True
    guiStyle.strLabel = ""  # 如果不需要显示label标签，这一行代码可以删除
    guiStyle.strLabelFont = "Arial"
    guiStyle.lFontSize = 20

    guiPolyline = GvVisionAssembly.GsScriptGuiPolyline()
    guiPolyline.polyline = GvVisionAssembly.scPolyline(VectorVec, True)
    guiStyle.strLabel = ""  # 如果不需要显示label标签，这一行代码可以删除
    guiPolyline.sScriptGuiStyle = guiStyle

    #guiArray.Add(guiCircle)
    return guiPolyline

def ShowLineSeg(line,clr,nStyle=0,nWidth=3,bResult=True):
    guiStyle = GvVisionAssembly.GsScriptGuiStyle()
    guiStyle.nLineStyle = 1 ## 线型 0:实线 1:虚线 2:点线
    guiStyle.nLineWidth = nWidth ## 线宽
    guiStyle.clrLineColor = clr
    guiLineSeg = GvVisionAssembly.GsScriptGuiLineSeg()
    guiLineSeg.lineSeg = line
    guiLineSeg.sScriptGuiStyle = guiStyle
    if bResult==True:
        return guiLineSeg

def imageShowTextXY(posX=100, posY=100, strmsg="hello", clrLineColor=[0, 255, 0], lFontSize=100,nStyle=0):
    # 设置GUI格式
    guiStyle = GvVisionAssembly.GsScriptGuiStyle()
    guiStyle.bVisible = True
    guiStyle.nLineStyle = 2
    guiStyle.nLineWidth = 2
    guiStyle.clrLineColor = clrLineColor
    guiStyle.bLabelVisible = True
    guiStyle.strLabelFont = "Calibri"
    guiStyle.lFontSize = lFontSize
    ######## GUI设置 ########

    # 文本GUI显示设置
    guiText = GvVisionAssembly.GsScriptGuiText()
    guiText.sScriptGuiStyle = guiStyle
    guiText.strText = strmsg
    guiText.posX = posX
    guiText.posY = posY
    guiText.deg = 0.0
    guiText.mode=nStyle
    # guiArray.Add(guiText)
    # 将GUI数组设置到视图
    return guiText

# error_code检测
    # 用于调用add,merge重新计算整体胶路检测结果
def check_errorcode(str_info,b_show_lackglue=True):
    obj = str_info
    list_error_code=[]
    #区域errorcode
    for key in obj["region_info"].keys():
        list_error_code.append(obj["region_info"][key]["info_base"]["error_code"])
    #断胶
    if obj["detection_gap_info"]["num"]>0:
        list_error_code.append(1)
    #溢胶
    if obj["detection_overflow_info"]["num"]>0:
        list_error_code.append(2)
    #多胶
    if obj["detection_much_info"]["num"]>0:
        list_error_code.append(2)
    #少胶
    if obj["detection_less_info"]["num"]>0:
        if b_show_lackglue==True:
            list_error_code.append(1)
        else:
            list_error_code.append(2)
    #胶长
    try:
        for key in obj["glue_length_info"].keys():
            if obj["glue_length_info"][key]["enable"]==True:
                list_error_code.append(obj["glue_length_info"][key]["error_code"])
    except:
        list_error_code.append(0)#
    if sum(list_error_code)>0:
        if list_error_code.count(1)>0:
            obj["base_info"]["error_code"]=1
        else:
            obj["base_info"]["error_code"]=2
    else:
        obj["base_info"]["error_code"]=0
    return obj
    
#用于修改区域数据后判断区域errorcode
def check_region_errorcode(str_info,key):
    obj_region1=str_info
    list_error_code=[]
    error_code=0#新判断产生的errorcode
    #####获取当前区域是否启用胶长及胶长errorcode
    try:
        if obj_region1["region_info"][key]["region_info_length"]["enable"]==True:
            list_error_code.append(obj_region1["region_info"][key]["region_info_length"]["error_code"])
    except:
        list_error_code.append(0)#
    if obj_region1["region_info"][key]["region_info_width"]["enable"]==True:
        list_error_code.append(obj_region1["region_info"][key]["region_info_width"]["error_code"])
    if obj_region1["region_info"][key]["region_info_shift"]["enable"]==True:
        list_error_code.append(obj_region1["region_info"][key]["region_info_shift"]["error_code"])
    try:
        if obj_region1["region_info"][key]["region_info_shiftX"]["enable"]==True:
            list_error_code.append(obj_region1["region_info"][key]["region_info_shiftX"]["error_code"])
    except:
        list_error_code.append(0)#
    try:
        if obj_region1["region_info"][key]["region_info_shiftY"]["enable"]==True:
            list_error_code.append(obj_region1["region_info"][key]["region_info_shiftY"]["error_code"])
    except:
        list_error_code.append(0)#
    if obj_region1["region_info"][key]["region_info_hole"]["enable"]==True:
        list_error_code.append(obj_region1["region_info"][key]["region_info_hole"]["error_code"])
    if obj_region1["region_info"][key]["region_info_area"]["enable"]==True:
        list_error_code.append(obj_region1["region_info"][key]["region_info_area"]["error_code"])
    if obj_region1["region_info"][key]["region_info_areashift"]["enable"]==True: 
        list_error_code.append(obj_region1["region_info"][key]["region_info_areashift"]["error_code"])               
    if sum(list_error_code)>0:
        if list_error_code.count(1)>0:
            error_code=1
        else:
            error_code=2
    else:
        error_code=0
    return error_code

class glue_display():
    n_mirror_mode = 0
    n_image_width = 0
    n_image_height = 0
    n_format = 4#小数点保留个数
    d_noglue_spec=0.05#无胶检测的阈值百分比
    b_show_broken=True#默认显示断胶
   
     # 设置镜像(不调用则不镜像)
    # mode :
        # 0：不镜像
        # 1：水平镜像
        # 2：垂直镜像
    # width : 图像宽度
    # height : 图像高度
    def set_mirror(self,mode,width,height):
        self.n_mirror_mode = mode      
        self.n_image_width = width      
        self.n_image_height = height              
    
    # 获取个数
    def get_color(error_code,b_show_cof):
        if error_code == 0:
            return [0, 255, 0]
        if error_code == 1:
            return [255, 0, 0]
        if error_code == 2  :
            if b_show_cof==True:
                return [255, 255, 0]
            else:
                 return [0, 255, 0]

    # 设置无胶的百分比SPEC
    def set_noglue_spec(self,d_noglue_spec_manual=0.05):
        if d_noglue_spec_manual>0.3 or d_noglue_spec_manual<0:
            d_noglue_spec_manual=0.05
        self.d_noglue_spec=d_noglue_spec_manual

    # 设置显示模式
    def set_show_mode(self, b_show_broken_manual=True):
        self.b_show_broken = b_show_broken_manual

    # 获取缺陷信息
    def get_err_msg(error_code,b_show_cof):
        if error_code == 0:
            return "OK"
        if error_code == 1:
            return "NG"
        if error_code == 2:
            if b_show_cof==True:
                return "COF"
            else:
                return "OK"

    # 获取检测结果
    #str_info :异型胶输出数据
    #b_mes_choose,mes上传选择，默认False，根据结果直接返回；选择True时缺陷降级返回(Fail为COF COF为OK)
    def get_detect_result(self,obj,b_mes_choose=False):
        obj_base = obj["base_info"]
        error_code = obj_base["error_code"]
        error_code_return=0
        strRes="OK"
        strResMes="OK"
        if error_code==0:
            strRes="OK"
            strResMes="OK"
            error_code_return=1
        elif  error_code==1:
            strRes="NG"
            strResMes="Fail"
            error_code_return=0
            if b_mes_choose==True:
                strResMes="COF"
                error_code_return=1
        elif  error_code==2:
            strRes="COF"
            strResMes="COF"
            error_code_return=2
            if b_mes_choose==True:
                strResMes="OK"
                error_code_return=1
        return error_code_return,strRes,strResMes

    # 用于返回无胶检测结果，NPI阶段要求无胶上传NG，有胶上传OK（即使有其他NG项目），因此必须返回无胶状态来控制上传
    # guiArray :显示用GuiArray
    # str_info :异型胶输出数据
    # 返回0 无胶NG  1 有胶OK
    def get_noglue_result(self, str_info):
        obj = str_info
        error_return=0
        obj_region = obj["region_info"]
        # 基础信息
        region_num = obj["base_info"]["region_number"]
        glue_area_sum=0
        glue_area_SPEC_sum=0
        for i in range(region_num):
            index = "region_{index}".format(index = i)
            obj_area = obj_region[index]["region_info_area"]
            region_type = obj["region_info"][index]["info_base"]["type"]
            if obj_area["enable"]==True and region_type=="normal":
                glue_area_sum=glue_area_sum+obj_area["current_val"]
                glue_area_SPEC_sum=glue_area_SPEC_sum+obj_area["lower_spec"]
        if glue_area_sum>glue_area_SPEC_sum*self.d_noglue_spec or glue_area_SPEC_sum==0:
            error_return =1
        return error_return

    #用于返回所有检测项加胶检整体OK/NG
    #返回数组，[总结果，胶占比结果,missing结果,断胶结果,缺胶结果,有无胶结果,溢胶结果,孔洞结果,偏移结果,胶长结果]
    def get_all_detection_result(self,str_info):
        obj = str_info
        obj = check_errorcode(obj)
        region_num = obj["base_info"]["region_number"]
        obj_region = obj["region_info"]
        #先默认OK
        str_total_result="OK"
        str_broken="OK"
        str_lenght="OK"
        str_coverage="OK"
        str_no_glue="OK"
        str_missing="OK"
        str_shift="OK"
        str_hole="OK"
        str_over_flow="OK"
        str_lack_glue="OK"

        #整体结果
        obj_base = obj["base_info"]
        error_code = obj_base["error_code"]
        if error_code==1:
            str_total_result="NG"
        #有无胶水
        if self.get_noglue_result(obj)==0:
            str_broken = "NG"
            str_lenght = "NG"
            str_coverage = "NG"
            str_no_glue = "NG"
            str_missing = "NG"
            str_shift = "NG"
            str_hole = "NG"
            str_over_flow = "NG"
            str_lack_glue = "NG"
        #断胶
        if obj["detection_gap_info"]["num"]>0:
            str_broken = "NG"
        #胶长
        for key in obj["glue_length_info"].keys():
            if obj["glue_length_info"][key]["enable"]==True:
                if obj["glue_length_info"][key]["error_code"]==1:
                    str_shift = "NG"
        #胶占比
        for i in range(region_num):
            index = "region_{index}".format(index=i)
            obj_area_shift = obj_region[index]["region_info_areashift"]
            region_type = obj["region_info"][index]["info_base"]["type"]
            if obj_area_shift["enable"] == True and region_type == "normal":
                if obj_area_shift["error_code"]==1:
                    str_coverage = "NG"
                    break
        #missing
        list_error_code=[]
        for i in range(region_num):
            index = "region_{index}".format(index = i)
            obj_area = obj_region[index]["region_info_area"]
            obj_width = obj_region[index]["region_info_width"]
            region_type = obj["region_info"][index]["info_base"]["type"]
            if obj_area["enable"]==True and region_type=="normal":
                list_error_code.append(obj_area["error_code"])
            if obj_width["enable"]==True and region_type=="normal":
                list_error_code.append(obj_width["error_code"])
        if list_error_code.count(1)>0:
            str_missing = "NG"
        #偏移
        list_error_code=[]
        for i in range(region_num):
            index = "region_{index}".format(index = i)
            obj_shift = obj_region[index]["region_info_shift"]
            region_type = obj["region_info"][index]["info_base"]["type"]

            if obj_shift["enable"]==True and region_type=="normal":
                list_error_code.append(obj_shift["error_code"])

            obj_shiftX = obj_region[index]["region_info_shiftX"]
            if obj_shiftX["enable"]==True and region_type=="normal":
                list_error_code.append(obj_shiftX["error_code"])

            obj_shiftY = obj_region[index]["region_info_shiftY"]
            if obj_shiftY["enable"]==True and region_type=="normal":
                list_error_code.append(obj_shiftY["error_code"])
        if list_error_code.count(1)>0:
            str_shift = "NG"
        #孔洞
        for i in range(region_num):
            index = "region_{index}".format(index = i)
            obj_hole = obj_region[index]["region_info_hole"]
            region_type = obj["region_info"][index]["info_base"]["type"]
            if obj_hole["enable"]==True and region_type=="normal" :
                if obj_hole["error_code"]==1:
                    str_hole = "NG"
                    break
        #溢胶
        for i in range(0,region_num):
            index = "region_{index}".format(index = i)
            region_type = obj["region_info"][index]["info_base"]["type"]
            #溢胶区域判断
            if region_type!="normal" and obj_region[index]["region_info_area"]["enable"]==True:
                if obj_region[index]["region_info_area"]["error_code"]==1:
                    str_over_flow = "NG"
                    break
        #缺胶
        if obj["detection_less_info"]["num"]>0:
            str_lack_glue = "NG"
        return [str_total_result,str_coverage,str_missing,str_broken,str_lack_glue,str_no_glue,str_over_flow,str_hole,str_shift,str_lenght]

    # Dùng cho mẫu hiển thị được khách hàng số 39 chỉ định
    # guiArray : GuiArray dùng để hiển thị
    # str_info : dữ liệu đầu ra keo hình dạng đặc biệt
    # str_station : tên công đoạn (workstation)
    # font_size : cỡ chữ hiển thị
    # offset_x : độ lệch hiển thị theo trục X
    # offset_y : độ lệch hiển thị theo trục Y
    # line_space : khoảng cách giữa các dòng hiển thị
    # line_width : độ rộng đường kẻ hiển thị
    # b_show_lackglue : True hiển thị thông tin thiếu keo; False không hiển thị
    # show_OK : có hiển thị vùng OK hay không, mặc định True (hiển thị), nếu đặt False thì vùng OK không hiển thị (vùng NG bắt buộc hiển thị)
    # list_posx, list_posy : điều chỉnh vị trí hiển thị thông tin NG, nếu thiếu thì mặc định là 0, nếu số vùng không đủ thì phần còn lại được tự động thêm 0
    def show_detection_result(self, guiArray, str_info,str_station, d_CT,font_size=40, offset_x=50, offset_y=50, line_space=0,
                             line_width=3, b_show_lackglue=False,show_OK=False,list_posx=None, list_posy=None,d_img_width=5472):
        obj = str_info
        # Lấy kết quả kiểm tra từng mục
        list_detection_result=self.get_all_detection_result(obj)
        # Thông tin cơ bản
        obj_base = obj["base_info"]
        region_num = obj["base_info"]["region_number"]
        obj_region = obj["region_info"]

        # Hiển thị tên công đoạn
        clr = [255, 0, 0]
        if list_detection_result[5] == "OK":
            clr = [0, 255, 0]
        str_out = str_station
        temp_font_size = font_size
        guiArray.Add(imageShowTextXY(offset_x, offset_y, str_out, clr,font_size))
        # Hiển thị SN
        clr = [255, 0, 0]
        if list_detection_result[5] == "OK":
            clr = [0, 255, 0]
        str_out = "SN:" + obj_base["SN"]
        guiArray.Add(imageShowTextXY(offset_x, offset_y + (line_space + font_size) , str_out,clr, font_size))
        # Hiển thị thời gian
        clr = [255, 0, 0]
        if list_detection_result[5] == "OK":
            clr = [0, 255, 0]
        str_out = "SN:" + obj_base["SN"]
        now = time.localtime()
        str_out = "Time:"+time.strftime("%Y-%m-%d %H:%M:%S", now)
        guiArray.Add(imageShowTextXY(offset_x, offset_y + (line_space + font_size) * 2, str_out, clr, font_size))
        # Thông tin mục kiểm tra
        n_detection_nums=1
        # Tỷ lệ keo
        clr=[255,0,0]
        for i in range(region_num):
            index = "region_{index}".format(index=i)
            obj_area_shift = obj_region[index]["region_info_areashift"]
            region_type = obj["region_info"][index]["info_base"]["type"]
            if obj_area_shift["enable"] == True and region_type == "normal":
                str_out="Glue Coverage Shift:"+list_detection_result[1]
                if list_detection_result[1]=="OK":
                    clr=[0,255,0]
                guiArray.Add(imageShowTextXY(offset_x, offset_y + (line_space + font_size) * (n_detection_nums+2), str_out, clr, font_size))
                n_detection_nums = n_detection_nums + 1
                break

        # missing
        clr = [255, 0, 0]
        for i in range(region_num):
            index = "region_{index}".format(index=i)
            obj_area = obj_region[index]["region_info_area"]
            obj_width = obj_region[index]["region_info_width"]
            region_type = obj["region_info"][index]["info_base"]["type"]
            if (obj_area["enable"] == True or obj_width["enable"] == True) and region_type == "normal":
                str_out = "Glue Missing:" + list_detection_result[2]
                if list_detection_result[2] == "OK":
                    clr = [0, 255, 0]
                guiArray.Add(imageShowTextXY(offset_x, offset_y + (line_space + font_size) * (n_detection_nums + 2) , str_out, clr, font_size))
                n_detection_nums = n_detection_nums + 1
                break

        # broken
        if self.b_show_broken == True:
            clr = [255, 0, 0]
            str_out = "Glue Broken:" + list_detection_result[3]
            if list_detection_result[3] == "OK":
                clr = [0, 255, 0]
            guiArray.Add(imageShowTextXY(offset_x, offset_y + (line_space + font_size) * (n_detection_nums + 2), str_out,clr, font_size))
            n_detection_nums = n_detection_nums + 1

        # lack_glue
        if b_show_lackglue == True:
            clr = [255, 0, 0]
            str_out = "Less Glue:" + list_detection_result[4]
            if list_detection_result[4] == "OK":
                clr = [0, 255, 0]
            guiArray.Add(imageShowTextXY(offset_x, offset_y + (line_space + font_size) * (n_detection_nums + 2), str_out,clr, font_size))
            n_detection_nums = n_detection_nums + 1

        # no_glue
        clr = [255, 0, 0]
        str_out = "No Glue:" + list_detection_result[5]
        if list_detection_result[5] == "OK":
            clr = [0, 255, 0]
        guiArray.Add(imageShowTextXY(offset_x, offset_y + (line_space + font_size) * (n_detection_nums + 2) ,str_out, clr, font_size))
        n_detection_nums=n_detection_nums+1

        # over_flow
        clr = [255, 0, 0]
        for i in range(0,region_num):
            index = "region_{index}".format(index = i)
            region_type = obj["region_info"][index]["info_base"]["type"]
            if region_type!="normal" and obj_region[index]["region_info_area"]["enable"]==True:
                str_out="Overflow:"+list_detection_result[6]
                if list_detection_result[6] == "OK":
                    clr = [0, 255, 0]
                guiArray.Add(imageShowTextXY(offset_x, offset_y + (line_space + font_size) * (n_detection_nums + 2) , str_out, clr, font_size))
                n_detection_nums = n_detection_nums + 1
                break

        # hole
        for i in range(region_num):
            index = "region_{index}".format(index=i)
            obj_hole = obj_region[index]["region_info_hole"]
            region_type = obj["region_info"][index]["info_base"]["type"]
            if obj_hole["enable"] == True and region_type == "normal":
                str_out = "Glue Coverage Hole:" + list_detection_result[7]
                if list_detection_result[7] == "OK":
                    clr = [0, 255, 0]
                guiArray.Add(imageShowTextXY(offset_x, offset_y + (line_space + font_size) * (n_detection_nums + 2) , str_out, clr, font_size))
                n_detection_nums=n_detection_nums + 1
                break

        # 偏移
        for i in range(region_num):
            index = "region_{index}".format(index=i)
            obj_shift = obj_region[index]["region_info_shift"]
            obj_shiftX = obj_region[index]["region_info_shiftX"]
            obj_shiftY = obj_region[index]["region_info_shiftY"]
            region_type = obj["region_info"][index]["info_base"]["type"]
            if (obj_shift["enable"] == True or obj_shiftX["enable"] == True or obj_shiftY["enable"] == True) and region_type == "normal":
                str_out = "Shift:" + list_detection_result[8]
                if list_detection_result[8] == "OK":
                    clr = [0, 255, 0]
                guiArray.Add(imageShowTextXY(offset_x, offset_y + (line_space + font_size) * (n_detection_nums + 2) , str_out, clr, font_size))
                n_detection_nums=n_detection_nums + 1
                break

        # 胶长
        for key in obj["glue_length_info"].keys():
            if obj["glue_length_info"][key]["enable"] == True:
                str_out = "Glue Length:" + list_detection_result[9]
                if list_detection_result[9] == "OK":
                    clr = [0, 255, 0]
                guiArray.Add(imageShowTextXY(offset_x, offset_y + (line_space + font_size) * (n_detection_nums + 2) , str_out, clr, font_size))
                n_detection_nums=n_detection_nums + 1
                break

        # CT
        clr = [255, 0, 0]
        if list_detection_result[5] == "OK":
            clr = [0, 255, 0]
        str_out="CT:"+str(round(d_CT,3))
        guiArray.Add(imageShowTextXY(offset_x, offset_y + (line_space + font_size) * (n_detection_nums + 2) , str_out, clr, font_size))

        # Kết quả kiểm tra
        temp_show_font=font_size*2
        if temp_show_font>360:
            temp_show_font=360
        clr = [255, 0, 0]
        str_out=list_detection_result[0]
        if list_detection_result[0] == "OK":
            clr = [0, 255, 0]
        guiArray.Add(imageShowTextXY(d_img_width-offset_x-temp_show_font-100, offset_y ,str_out, clr, temp_show_font))

        # Hiển thị vùng kiểm tra
        list_region = []
        for i in range(region_num):
            list_region.append(i)
        font_size_ng = int(font_size / 2)
        if font_size_ng < 8:
            font_size_ng = 8
        guiArray = self.show_detetion_Region(guiArray, obj, list_region, show_OK, font_size_ng, line_width, False)
        # Hiển thị thông tin NG
        font_size_ng = int(font_size / 2)
        if font_size_ng < 8:
            font_size_ng = 8
        for region_index in list_region:
            if list_posx == None:
                offset_x = 0
            else:
                try:
                    offset_x = list_posx[region_index]
                except:
                    offset_x = 0
            if list_posy == None:
                offset_y = 0
            else:
                try:
                    offset_y = list_posy[region_index]
                except:
                    offset_y = 0
            guiArray = self.show_NG_data(guiArray, obj, region_index, font_size_ng, offset_x, offset_y, line_space,False)

        return guiArray

    # Dùng để hiển thị các thông tin thông thường: kết quả vật liệu, SN, lý do NG, độ rộng keo nhỏ nhất, thông tin kết quả chi tiết, vùng kiểm tra, v.v.
    # guiArray : Đối tượng GuiArray dùng để hiển thị
    # str_info : Dữ liệu đầu ra của keo dị hình
    # font_size：Kích thước font hiển thị
    # offset_x：Độ lệch hiển thị theo trục X
    # offset_y：Độ lệch hiển thị theo trục Y
    # line_space: Khoảng cách giữa các dòng
    # line_width：Độ rộng của dòng hiển thị
    # bShowMinWidth: Có hiển thị độ rộng keo nhỏ nhất hay không, true để hiển thị, false để ẩn, mặc định là hiển thị
    # b_show_cof：True hiển thị COF màu vàng và dữ liệu chi tiết; False hiển thị COF màu xanh lá và ẩn dữ liệu chi tiết
    # b_show_shifit: True hiển thị thông tin Shift; false không hiển thị
    # b_show_lenght: True hiển thị thông tin chiều dài keo; false không hiển thị
    # b_show_overflow: True hiển thị thông tin tràn keo; false không hiển thị
    # b_show_lackglue: True hiển thị thông tin thiếu keo; false không hiển thị
    # show_OK：Có hiển thị vùng OK hay không, mặc định là True (hiển thị); nếu đặt là false thì vùng OK sẽ không hiển thị (NG luôn được hiển thị)
    # list_posx, list_posy: Danh sách điều chỉnh vị trí hiển thị thông tin NG; nếu không có sẽ mặc định là 0; nếu số lượng không đủ với số vùng thì phần còn lại sẽ mặc định là 0

    def show_general_data_Ex(self,guiArray,str_info,font_size=40,offset_x=50,offset_y=50,line_space=0,line_width=3,bShowMinWidth=True,b_show_cof=False,\
                            b_show_shifit=False,b_show_lenght=False,b_show_overflow=False,b_show_lackglue=False,show_OK=False,list_posx=None,list_posy=None):
        # Hiển thị toàn bộ thông tin
        # -----------------------------
        # Gộp kết quả kiểm tra
        # error_code - Mã lỗi:
        #   eOk = 0         // OK
        #   eTruefail       // Lỗi nghiêm trọng
        #   eCOF            // Lỗi thông thường (COF)

        # obj = json.loads(str_info)  # Giải mã JSON nếu cần
        obj = str_info
        # Kiểm tra và cập nhật mã lỗi, tùy theo có hiển thị thiếu keo hay không
        obj = check_errorcode(obj, b_show_lackglue)
        # Lấy thông tin cơ bản
        obj_base = obj["base_info"]
        error_code = obj_base["error_code"]
        # Tạo chuỗi kết quả kiểm tra keo
        str_out = "Glue Check Result" + ":" + glue_display.get_err_msg(error_code, b_show_cof)

        # Hiển thị kết quả kiểm tra
        temp_font_size = font_size  # Lưu kích thước chữ tạm thời
        # Hiển thị kết quả kiểm tra chính (ví dụ: "Glue Check Result: OK/NG")
        guiArray.Add(
            imageShowTextXY(
                offset_x,
                offset_y,
                str_out,
                glue_display.get_color(error_code, b_show_cof),  # Màu theo mã lỗi và chế độ hiển thị COF
                font_size + temp_font_size
            )
        )
        # Hiển thị SN
        str_out = "SN:" + obj_base["SN"]
        guiArray.Add(
            imageShowTextXY(
                offset_x,
                offset_y + line_space + font_size + temp_font_size,
                str_out,
                glue_display.get_color(error_code, b_show_cof),
                font_size
            )
        )

        # Chuẩn bị hiển thị thông tin NG (Not Good - lỗi)
        str_out_mes = ""
        list_out_mes = []
        # Lấy số vùng kiểm tra từ thông tin cơ bản
        region_num = obj["base_info"]["region_number"]
        list_region = []
        for i in range(region_num):
            list_region.append(i)
        # Lấy thông tin chi tiết từng vùng
        obj_region = obj["region_info"]

        # Kiểm tra NoGlue: không có keo thì tất cả mục kiểm tra đều NG, có keo thì hiển thị bình thường.
        nums = 1
        str_out_noglue="NoGlue:"
        str_out_noglue_errorcode=0
        if self.get_noglue_result(obj)==1:
            str_out_noglue=str_out_noglue+"OK"
            str_out_noglue_errorcode=0
        else:
            str_out_noglue=str_out_noglue+"NG"
            str_out_noglue_errorcode=1
            list_out_mes.append("NoGlue")
        guiArray.Add(imageShowTextXY(offset_x, offset_y + (line_space + font_size) * (nums + 2) + temp_font_size,str_out_noglue, glue_display.get_color(str_out_noglue_errorcode, b_show_cof), font_size, 2))
        # Xử lý thông tin tiếp theo: nếu NoGlue thì tất cả hạng mục kiểm tra đều hiển thị NG.
        if str_out_noglue_errorcode==1:
            # Thông tin tỉ lệ/độ rộng/diện tích: không cần xử lý, vốn dĩ đã NG  
            # Thông tin lỗ hổng: cần xử lý, mặc định là NG
            for i in range(region_num):
                index = "region_{index}".format(index=i)
                obj_hole = obj_region[index]["region_info_hole"]
                region_type = obj["region_info"][index]["info_base"]["type"]
                if obj_hole["enable"] == True and region_type == "normal":
                    obj_hole["error_code"]=1
            # Thông tin đứt keo: cần xử lý, mặc định là NG
            obj["detection_gap_info"]["num"]=999
            # Thông tin thừa keo: cần xử lý, mặc định là NG
            for i in range(region_num):
                index = "region_{index}".format(index=i)
                region_type = obj["region_info"][index]["info_base"]["type"]
                if region_type != "normal" and obj_region[index]["region_info_area"]["enable"] == True:
                    obj_region[index]["region_info_area"]["error_code"]=1
            # Thông tin lệch keo: cần xử lý, mặc định là NG
            try:
                for i in range(region_num):
                    index = "region_{index}".format(index=i)
                    obj_shift = obj_region[index]["region_info_shift"]
                    obj_shiftX = obj_region[index]["region_info_shiftX"]
                    obj_shiftY = obj_region[index]["region_info_shiftY"]
                    region_type = obj["region_info"][index]["info_base"]["type"]
                    if obj_shift["enable"] == True and region_type == "normal":
                        obj_shift["error_code"]=1
                    if obj_shiftX["enable"] == True and region_type == "normal":
                        obj_shiftX["error_code"]=1
                    if obj_shiftY["enable"] == True and region_type == "normal":
                        obj_shiftY["error_code"]=1
            except:
                temp = 0  # Không có ý nghĩa
            # Thông tin chiều dài keo: cần xử lý, mặc định là NG
            try:
                for key in obj["glue_length_info"].keys():
                    if obj["glue_length_info"][key]["enable"] == True:
                        obj["glue_length_info"][key]["error_code"]=1
            except:
                temp = 0  # 

        # Xử lý thông tin "tỷ lệ phủ keo" (Coverage Shift)
        list_error_code = []     # Danh sách mã lỗi của từng vùng
        list_ng_region = []      # Danh sách vùng có lỗi
        error_codes = 0          # Mã lỗi tổng thể
        for i in range(region_num):
            index = "region_{index}".format(index = list_region[i])
            obj_area_shift = obj_region[index]["region_info_areashift"]
            region_type = obj["region_info"][index]["info_base"]["type"]
            #print(region_type)
            if obj_area_shift["enable"]==True and region_type=="normal":
                list_error_code.append(obj_area_shift["error_code"])
                list_ng_region.append(i)
        if len(list_error_code)>0:
            nums=nums+1
            str_out_area_shirt="Glue coverage shift:"
            # Nếu không có lỗi
            if sum(list_error_code)==0:
                str_out_area_shirt=str_out_area_shirt+"OK"
            else:
                if list_error_code.count(1)>0:
                    error_codes=1
                else:
                    error_codes=2
                # Hiển thị thông tin NG nếu cấu hình cho phép
                if (error_codes==2 and b_show_cof==True ) or error_codes==1:
                    list_out_mes.append("CoverageShift")
                # Tùy thuộc vào cấu hình có hiển thị COF không để xác định hiển thị NG/OK
                if error_codes==2:
                    if b_show_cof==True:
                        str_out_area_shirt = str_out_area_shirt+"NG("
                    else:
                        str_out_area_shirt = str_out_area_shirt + "OK("
                if error_codes==1:
                    str_out_area_shirt = str_out_area_shirt + "NG("
                for i in range(0,len(list_error_code)):
                    if list_error_code[i]!=0:
                        str_out_area_shirt=str_out_area_shirt+"R"+str(list_ng_region[i]+1)+","
                str_out_area_shirt=str_out_area_shirt+")"
            guiArray.Add(imageShowTextXY(offset_x,offset_y+(line_space+font_size)*(nums+2)+temp_font_size,str_out_area_shirt,glue_display.get_color(error_codes,b_show_cof),font_size,2)) 

        # 孔洞信息
        list_error_code=[]
        list_ng_region=[]
        error_codes=0
        for i in range(region_num):
            index = "region_{index}".format(index = list_region[i])
            obj_hole = obj_region[index]["region_info_hole"]
            region_type = obj["region_info"][index]["info_base"]["type"]
            if obj_hole["enable"]==True and region_type=="normal" :
                list_error_code.append(obj_hole["error_code"])
                list_ng_region.append(i)
        if len(list_error_code)>0:
            nums=nums+1
            str_out_hole="Glue coverage hole:"
            if sum(list_error_code)==0:
                str_out_hole=str_out_hole+"OK"
            else:
                if list_error_code.count(1)>0:
                    error_codes=1
                else:
                    error_codes=2
                # NG信息增加
                if (error_codes == 2 and b_show_cof == True) or error_codes == 1:
                    list_out_mes.append("Hole")
                # 根据结果及是否显示COF来显示单项NG/OK信息
                if error_codes == 2:
                    if b_show_cof == True:
                        str_out_hole = str_out_hole + "NG("
                    else:
                        str_out_hole = str_out_hole + "OK("
                if error_codes == 1:
                    str_out_hole = str_out_hole + "NG("
                for i in range(0,len(list_error_code)):
                    if list_error_code[i]!=0:
                        str_out_hole=str_out_hole+"R"+str(list_ng_region[i]+1)+","
                str_out_hole=str_out_hole+")"
            guiArray.Add(imageShowTextXY(offset_x,offset_y+(line_space+font_size)*(nums+2)+temp_font_size,str_out_hole,glue_display.get_color(error_codes,b_show_cof),font_size,2))    
        
        ####面积与宽度统一归类为GlueMissing
        # 面积信息
        list_error_code=[]
        list_ng_region=[]
        error_codes=0
        for i in range(region_num):
            index = "region_{index}".format(index = list_region[i])
            obj_area = obj_region[index]["region_info_area"]
            region_type = obj["region_info"][index]["info_base"]["type"]
            if obj_area["enable"]==True and region_type=="normal":
                list_error_code.append(obj_area["error_code"])
                list_ng_region.append(i)
        # 胶宽信息
        list_error_code1=[]
        list_ng_region1=[]
        for i in range(region_num):
            index = "region_{index}".format(index = list_region[i])
            obj_width = obj_region[index]["region_info_width"]
            region_type = obj["region_info"][index]["info_base"]["type"]
            if obj_width["enable"]==True and region_type=="normal":
                list_error_code1.append(obj_width["error_code"])
                list_ng_region1.append(i)
                # 最短胶宽及位置显示
                min_x_start=obj_width["min_start_pt"]["x"]
                min_y_start=obj_width["min_start_pt"]["y"]
                min_x_end=obj_width["min_end_pt"]["x"]
                min_y_end=obj_width["min_end_pt"]["y"]                                
                if self.n_mirror_mode == 1:
                    min_x_start = self.n_image_width - min_x_start
                    min_x_end = self.n_image_width - min_x_end                    
                elif self.n_mirror_mode == 2: 
                    min_y_start = self.n_image_height - min_y_start
                    min_y_end = self.n_image_height - min_y_end
                pt1=GvVisionAssembly.sc2Vector(min_x_start,min_y_start)
                pt2=GvVisionAssembly.sc2Vector(min_x_end,min_y_end)
                lineSeg=GvVisionAssembly.scLineSeg(pt1,pt2)
                str_min_width_out="{min_width}".format(min_width=round(obj_width["min_val"],self.n_format))
                if obj_width["min_val"]==0.0:
                    pos_x=obj_region[index]["info_base"]["position"]["x"]+30
                    pos_y=obj_region[index]["info_base"]["position"]["y"]+30
                else:
                    pos_x=(min_x_start+min_x_end)/2+5
                    pos_y=(min_y_start+min_y_end)/2
                temp=abs(font_size-10)
                if temp<8:
                    temp=8
                ###是否显示最短胶宽 
                if bShowMinWidth==True:
                    guiArray.Add(ShowLineSeg(lineSeg,glue_display.get_color(obj_width["error_code"],b_show_cof),0,2))
                    guiArray.Add(imageShowTextXY(pos_x,pos_y,str_min_width_out,glue_display.get_color(obj_width["error_code"],b_show_cof),temp,2))
        #面积与宽度信息合并，先面积后宽度
        list_error_code.extend(list_error_code1)   
        list_ng_region.extend(list_ng_region1)        
        if len(list_error_code)>0:
            nums=nums+1
            str_out_width="Glue missing:"
            if sum(list_error_code)==0:
                str_out_width=str_out_width+"OK"
            else:
                if list_error_code.count(1)>0:
                    error_codes=1
                else:
                    error_codes=2
                #NG原因新增
                if error_codes==1 or (error_codes==2 and b_show_cof==True):
                    list_out_mes.append("GlueMissing")
                #根据结果及是否显示COF来显示单项NG / OK信息
                if error_codes==2:
                    if b_show_cof==True:
                        str_out_width=str_out_width+"NG("
                    else:
                        str_out_width=str_out_width+"OK("
                if error_codes==1:
                    str_out_width = str_out_width + "NG("
                for i in range(0,len(list_error_code)):
                    if list_error_code[i]!=0:
                        str_out_width=str_out_width+"R"+str(list_ng_region[i]+1)+","
                str_out_width=str_out_width+")"
            guiArray.Add(imageShowTextXY(offset_x,offset_y+(line_space+font_size)*(nums+2)+temp_font_size,str_out_width,glue_display.get_color(error_codes,b_show_cof),font_size,2))

        # 偏移信息
        list_error_code=[]
        list_ng_region=[]
        error_codes=0
        for i in range(region_num):
            index = "region_{index}".format(index = list_region[i])
            obj_shift = obj_region[index]["region_info_shift"]
            region_type = obj["region_info"][index]["info_base"]["type"]
            #距离判断
            if obj_shift["enable"]==True and region_type=="normal":
                list_error_code.append(obj_shift["error_code"])
                if obj_shift["error_code"]>0:
                    list_ng_region.append(i)
            #X距离判断
            try:
                obj_shiftX = obj_region[index]["region_info_shiftX"]
                if obj_shiftX["enable"]==True and region_type=="normal":
                    list_error_code.append(obj_shiftX["error_code"])
                    if obj_shiftX["error_code"]>0 and list_ng_region.count(i)==0:
                        list_ng_region.append(i)
            except:
                temp=0# 
            #Y距离判断
            try:
                obj_shiftY = obj_region[index]["region_info_shiftY"]
                if obj_shiftY["enable"]==True and region_type=="normal":
                    list_error_code.append(obj_shiftY["error_code"])
                    if obj_shiftY["error_code"]>0 and list_ng_region.count(i)==0:
                        list_ng_region.append(i)
            except:
                temp=0# 
        if len(list_error_code)>0 and b_show_shifit==True:
            nums=nums+1
            str_out_shift="Glue shift:"
            if sum(list_error_code)==0:
                str_out_shift=str_out_shift+"OK"
            else:
                list_ng_region.sort()
                if list_error_code.count(1)>0:
                    error_codes=1
                    str_out_shift=str_out_shift+"NG("
                else:
                    error_codes=2
                if (error_codes!=2 and b_show_cof!=True ) or b_show_cof==True:
                    list_out_mes.append("Shift")
                if error_codes==2: 
                    if b_show_cof==True:
                        str_out_shift=str_out_shift+"NG("
                    else:
                        str_out_shift=str_out_shift+"OK("
                for i in range(0,len(list_ng_region)):
                    str_out_shift=str_out_shift+"R"+str(list_ng_region[i]+1)+","
                str_out_shift=str_out_shift+")"
            guiArray.Add(imageShowTextXY(offset_x,offset_y+(line_space+font_size)*(nums+2)+temp_font_size,str_out_shift,glue_display.get_color(error_codes,b_show_cof),font_size,2))             

        # 断胶信息及轮廓
        if self.b_show_broken==True:
            nums=nums+1
            num_brocken=obj["detection_gap_info"]["num"]
            str_out_brocken="Glue path broken:"
            error_codes=0
            if num_brocken>0:#存在断胶
                error_codes=obj_base["error_code"]
                str_out_brocken=str_out_brocken+"NG"
                list_out_mes.append("Broken")
                ###显示NG区域及长度
                try:
                    for i in range(num_brocken):
                        index = "{index}".format(index = i)
                        broken_length=obj["detection_gap_info"][index]["info"]["width"]
                        str_out_brocken_length="{broken_data}".format(broken_data=round(broken_length,self.n_format))
                        start_x=obj["detection_gap_info"][index]["info"]["start_pt"]["X"]
                        start_y=obj["detection_gap_info"][index]["info"]["start_pt"]["Y"]
                        end_x=obj["detection_gap_info"][index]["info"]["end_pt"]["X"]
                        end_y=obj["detection_gap_info"][index]["info"]["end_pt"]["Y"]
                        if self.n_mirror_mode == 1:
                            start_x = self.n_image_width - start_x
                            end_x = self.n_image_width - end_x
                        elif self.n_mirror_mode == 2:
                            start_y = self.n_image_height - start_y
                            end_y = self.n_image_height - end_y
                        scVecVec = GvVisionAssembly.sc2VectorVec()
                        for key in obj["detection_gap_info"][index]["contour"].keys():
                            temp_x=obj["detection_gap_info"][index]["contour"][key]["X"]
                            temp_y=obj["detection_gap_info"][index]["contour"][key]["Y"]
                            if self.n_mirror_mode == 1:
                                temp_x = self.n_image_width - temp_x
                            elif self.n_mirror_mode == 2:
                                temp_y = self.n_image_height - temp_y
                            pt = GvVisionAssembly.sc2Vector(temp_x,temp_y)
                            scVecVec.append(pt)
                        guiArray.Add(imageShowPolyline(scVecVec,[255,0,0],line_width))
                        guiArray.Add(imageShowTextXY((start_x+end_x)/2,(end_y+start_y)/2,str_out_brocken_length,glue_display.get_color(1,b_show_cof),font_size))
                except:
                    temp=0#
            else:#不存在断胶
                str_out_brocken=str_out_brocken+"OK"
            guiArray.Add(imageShowTextXY(offset_x,offset_y+(line_space+font_size)*(nums+2)+temp_font_size,str_out_brocken,glue_display.get_color(error_codes,b_show_cof),font_size,2))
        
        # 溢胶信息及轮廓，启用显示，不启用显示
        #判断是否有溢胶区域
        overflow_region_num=0
        error_codes_list=[]
        for i in range(0,obj["base_info"]["region_number"]):
            index = "region_{index}".format(index = i)
            region_type = obj["region_info"][index]["info_base"]["type"]
            #溢胶区域判断
            if region_type!="normal" and obj_region[index]["region_info_area"]["enable"]==True:
                overflow_region_num=overflow_region_num+1
                error_codes_list.append(obj_region[index]["region_info_area"]["error_code"])
        #有溢胶区域才进行显示
        if overflow_region_num>0 and b_show_overflow==True:
            nums=nums+1
            num_overflow=obj["detection_overflow_info"]["num"]
            str_out_overflow="Overflow:"
            error_codes=0
            if num_overflow>0:
            #error_codes状态判断
                if error_codes_list.count(1)>0:
                    error_codes=1
                else:
                    error_codes=2
                tempdatas=0
                str_out_overflow=str_out_overflow+"NG"
                if error_codes==2: 
                    if b_show_cof!=True:
                        str_out_overflow="Overflow:OK"
                if b_show_cof==True or error_codes==1:
                    list_out_mes.append("Overflow")
                ###溢胶序号排序
                startIndex=0
                for i in range(0,obj["base_info"]["region_number"]):
                    key ="region_{index}".format(index = i)   
                    region_type = obj["region_info"][key]["info_base"]["type"]
                    if region_type =="normal":
                        startIndex=startIndex+1
                ###计算溢胶面积，各区域单独输出
                str_area_overflow=[]
                list_error_code=[]
                for i in range(0,obj["base_info"]["region_number"]):
                    if i<startIndex:
                        continue
                    key ="region_{index}".format(index = i)
                    region_type = obj["region_info"][key]["info_base"]["type"]
                    if region_type=="overflow":
                        list_error_code.append(obj["region_info"][key]["info_base"]["error_code"])
                        if obj["region_info"][key]["info_base"]["error_code"]>0:
                            val=round(obj["region_info"][key]["region_info_area"]["current_val"],self.n_format)
                            lsl=round(obj["region_info"][key]["region_info_area"]["lower_spec"],2)
                            usl=round(obj["region_info"][key]["region_info_area"]["upper_spec"],2)
                            str_temp_data="OF{index}".format(index = (i+1-startIndex))+": {overflow_data}({LSL_data},{USL_data})".format(overflow_data=val,LSL_data=lsl,USL_data=usl)
                            str_area_overflow.append(str_temp_data)
                if list_error_code.count(1)>0:
                    error_codes=1
                ###显示NG区域轮廓
                try:
                    for i in range(num_overflow):
                        index = "{index}".format(index = i)               
                        scVecVec = GvVisionAssembly.sc2VectorVec()
                        for key in obj["detection_overflow_info"][index]["contour"].keys():
                            temp_x=obj["detection_overflow_info"][index]["contour"][key]["X"]
                            temp_y=obj["detection_overflow_info"][index]["contour"][key]["Y"]
                            if self.n_mirror_mode == 1:
                                temp_x = self.n_image_width - temp_x          
                            elif self.n_mirror_mode == 2: 
                                temp_y = self.n_image_height - temp_y
                            pt = GvVisionAssembly.sc2Vector(temp_x,temp_y)
                            scVecVec.append(pt)
                        #if b_show_cof==True:
                        guiArray.Add(imageShowPolyline(scVecVec,glue_display.get_color(error_codes,b_show_cof),line_width))
                except:
                    print("No Counter")
                #并入溢胶面积
                #if len(str_area_overflow)>0 and b_show_cof==True:
                if len(str_area_overflow)>0:
                    str_out_overflow=str_out_overflow+"("
                    for str_data in str_area_overflow:
                        str_out_overflow=str_out_overflow+str_data+","
                    str_out_overflow=str_out_overflow+")"
            else:
                str_out_overflow=str_out_overflow+"OK"
            guiArray.Add(imageShowTextXY(offset_x,offset_y+(line_space+font_size)*(nums+2)+temp_font_size,str_out_overflow,glue_display.get_color(error_codes,b_show_cof),font_size,2))

        # 胶长信息
        list_error_code=[]
        str_length=[]
        enable_flage=False
        error_codes=0
        str_out_length="Gluelength:"
        lenght_index=0
        for key in obj["glue_length_info"].keys():
            lenght_index=lenght_index+1
            if obj["glue_length_info"][key]["enable"]==True:
                enable_flage=True
                if obj["glue_length_info"][key]["error_code"]>0:
                    list_error_code.append(obj["glue_length_info"][key]["error_code"])
                    lengh_dat=round(obj["glue_length_info"][key]["current_val"],self.n_format)
                    lsl=round(obj["glue_length_info"][key]["lower_spec"],2)
                    usl=round(obj["glue_length_info"][key]["upper_spec"],2)
                    str_temp_data="Length"+str(lenght_index)+":{lenght}({LSL_data},{USL_data})".format(lenght=lengh_dat,LSL_data=lsl,USL_data=usl)
                    str_length.append(str_temp_data)  
        #启用显示，不启用显示
        if enable_flage==True and b_show_lenght==True:
            if len(list_error_code)>0:
                if list_error_code.count(1)>0:
                    error_codes=1
                else:
                    error_codes=2
                str_out_length=str_out_length+"NG"
                if error_codes==2: 
                    if b_show_cof!=True:
                        str_out_length="Gluelength:OK"
                if (error_codes!=2 and b_show_cof!=True ) or b_show_cof==True:
                    list_out_mes.append("Gluelength")
                #if error_codes>0 and b_show_cof==True:
                if error_codes>0:
                    str_out_length=str_out_length+"("
                    for str_data in str_length:
                        str_out_length=str_out_length+str_data+","
                    str_out_length=str_out_length+")"
            else:
                str_out_length=str_out_length+"OK"
            nums=nums+1
            guiArray.Add(imageShowTextXY(offset_x,offset_y+(line_space+font_size)*(nums+2)+temp_font_size,str_out_length,glue_display.get_color(error_codes,b_show_cof),font_size,2))
        
        #缺胶信息
        if b_show_lackglue==True:
            show_errorcode=0
            nums=nums+1
            num_LackGlue=obj["detection_less_info"]["num"]
            str_out_LackGlue="LessGlue:"
            if num_LackGlue>0:
                list_out_mes.append("LessGlue")
                str_out_LackGlue=str_out_LackGlue+"NG"
                show_errorcode=1
            else:
                str_out_LackGlue=str_out_LackGlue+"OK"
            guiArray.Add(imageShowTextXY(offset_x,offset_y+(line_space+font_size)*(nums+2)+temp_font_size,str_out_LackGlue,glue_display.get_color(show_errorcode,b_show_cof),font_size,2))
        
        #NG信息  
        if len(list_out_mes)>0:
            str_out_mes="NG reason:"
            for i in list_out_mes:
                str_out_mes=str_out_mes+i+"/"
        guiArray.Add(imageShowTextXY(offset_x,offset_y+(line_space+font_size)*2+temp_font_size,str_out_mes,glue_display.get_color(error_code = obj_base["error_code"],b_show_cof=b_show_cof),font_size))       
        #显示检测区域
        font_size_ng=int(font_size/2)
        if font_size_ng<8:
            font_size_ng=8
        guiArray=self.show_detetion_Region(guiArray,obj,list_region,show_OK,font_size_ng,line_width,b_show_cof)
        #显示NG信息
        font_size_ng=int(font_size/2)
        if font_size_ng<8:
            font_size_ng=8
        for region_index in list_region:
            if list_posx==None:
                offset_x=0
            else:
                try:
                    offset_x=list_posx[region_index]
                except:
                    offset_x=0
            if list_posy==None:
                offset_y=0
            else:
                try:
                    offset_y=list_posy[region_index]
                except:
                    offset_y=0
            guiArray=self.show_NG_data(guiArray,obj,region_index,font_size_ng,offset_x,offset_y,line_space,b_show_cof)
        #显示处理
        
        return guiArray 

    #用于显示常规信息：物料结果,SN,NG原因，最短胶宽，详细结果信息
    #guiArray :显示用GuiArray
    #str_info :异型胶输出数据
    #font_size：显示字体
    #offset_x：显示偏移量X
    #offset_y：显示偏移量Y
    #line_space: 显示行间距
    #line_width：显示线宽

    #bShowMinWidth:是否显示最小胶宽,true 显示 ，false 不显示,默认显示
    #b_show_cof：True COF显示黄色与详细数据  False COF显示绿色及屏蔽详细数据
    #b_show_shifit:True 显示Shift信息；false 不显示
    #b_show_lenght:True 显示胶长信息；false 不显示
    #b_show_overflow:True 显示溢胶信息；false 不显示
    #b_show_lackglue:True 显示缺胶信息；false 不显示
    def show_general_data(self,guiArray,str_info,font_size=40,offset_x=50,offset_y=50,line_space=0,line_width=3,bShowMinWidth=True,b_show_cof=False,\
                            b_show_shifit=False,b_show_lenght=False,b_show_overflow=False,b_show_lackglue=False):
        #所有信息均显示
        # -----------------------------
        # 检测结果合并
        # error_code
        # 	eOk = 0,        //	OK
        #	eTruefail,		//	严重
        #	eCOF			//	一般
        #obj = json.loads(str_info)
        obj=str_info
        obj=check_errorcode(obj,b_show_lackglue)
        # 基础信息
        obj_base = obj["base_info"]
        error_code = obj_base["error_code"]
        str_out = "Glue Check Result" ":" + glue_display.get_err_msg(error_code,b_show_cof)

        # 显示检测结果
        temp_font_size=font_size
        guiArray.Add(imageShowTextXY(offset_x,offset_y,str_out,glue_display.get_color(error_code,b_show_cof),font_size+temp_font_size))
        # 显示SN
        str_out = "SN:" + obj_base["SN"]
        guiArray.Add(imageShowTextXY(offset_x,offset_y+line_space+font_size+temp_font_size,str_out,glue_display.get_color(error_code,b_show_cof),font_size))
        # NG信息
        str_out_mes=""
        list_out_mes=[]
        # 分区域信息
        region_num = obj["base_info"]["region_number"]
        list_region=[]
        for i in range(region_num):
            list_region.append(i)
        obj_region = obj["region_info"]

        # NoGlue状态判断，当无胶时，所有显示检测项目均NG，有胶时正常显示
        nums = 1
        str_out_noglue = "NoGlue:"
        str_out_noglue_errorcode = 0
        if self.get_noglue_result(obj) == 1:
            str_out_noglue = str_out_noglue + "OK"
            str_out_noglue_errorcode = 0
        else:
            str_out_noglue = str_out_noglue + "NG"
            str_out_noglue_errorcode = 1
            list_out_mes.append("NoGlue")
        guiArray.Add(
            imageShowTextXY(offset_x, offset_y + (line_space + font_size) * (nums + 2) + temp_font_size, str_out_noglue,glue_display.get_color(str_out_noglue_errorcode, b_show_cof), font_size, 2))
        # 处理后续信息，当noglue时，所有检测项目均显示NG
        if str_out_noglue_errorcode == 1:
            # 占比/胶宽/面积信息，不用处理，本身NG
            # 孔洞信息，需要处理，默认NG
            for i in range(region_num):
                index = "region_{index}".format(index=i)
                obj_hole = obj_region[index]["region_info_hole"]
                region_type = obj["region_info"][index]["info_base"]["type"]
                if obj_hole["enable"] == True and region_type == "normal":
                    obj_hole["error_code"] = 1
            # 断胶信息，需要处理，默认NG
            obj["detection_gap_info"]["num"] = 999
            # 溢胶信息，需要处理，默认NG
            for i in range(region_num):
                index = "region_{index}".format(index=i)
                region_type = obj["region_info"][index]["info_base"]["type"]
                if region_type != "normal" and obj_region[index]["region_info_area"]["enable"] == True:
                    obj_region[index]["region_info_area"]["error_code"] = 1
            # 偏移信息，需要处理，默认NG
            try:
                for i in range(region_num):
                    index = "region_{index}".format(index=i)
                    obj_shift = obj_region[index]["region_info_shift"]
                    obj_shiftX = obj_region[index]["region_info_shiftX"]
                    obj_shiftY = obj_region[index]["region_info_shiftY"]
                    region_type = obj["region_info"][index]["info_base"]["type"]
                    if obj_shift["enable"] == True and region_type == "normal":
                        obj_shift["error_code"] = 1
                    if obj_shiftX["enable"] == True and region_type == "normal":
                        obj_shiftX["error_code"] = 1
                    if obj_shiftY["enable"] == True and region_type == "normal":
                        obj_shiftY["error_code"] = 1
            except:
                temp = 0  # 
            # 胶长信息，需要处理，默认NG
            try:
                for key in obj["glue_length_info"].keys():
                    if obj["glue_length_info"][key]["enable"] == True:
                        obj["glue_length_info"][key]["error_code"] = 1
            except:
                temp = 0  # 

        # 占比信息
        list_error_code=[]
        list_ng_region=[]
        nums=0
        error_codes=0
        for i in range(region_num):
            index = "region_{index}".format(index = list_region[i])
            obj_area_shift = obj_region[index]["region_info_areashift"]
            region_type = obj["region_info"][index]["info_base"]["type"]
            #print(region_type)
            if obj_area_shift["enable"]==True and region_type=="normal":
                list_error_code.append(obj_area_shift["error_code"])
                list_ng_region.append(i)
        if len(list_error_code)>0:
            nums=nums+1
            str_out_area_shirt="Glue coverage shift:"
            if sum(list_error_code)==0:
                str_out_area_shirt=str_out_area_shirt+"OK"
            else:
                if list_error_code.count(1)>0:
                    error_codes=1
                else:
                    error_codes=2
                if (error_codes!=2 and b_show_cof!=True ) or b_show_cof==True:
                    list_out_mes.append("CoverageShift")
                str_out_area_shirt=str_out_area_shirt+"NG("
                for i in range(0,len(list_error_code)):
                    if list_error_code[i]!=0:
                        str_out_area_shirt=str_out_area_shirt+"R"+str(list_ng_region[i]+1)+","
                str_out_area_shirt=str_out_area_shirt+")"
            guiArray.Add(imageShowTextXY(offset_x,offset_y+(line_space+font_size)*(nums+2)+temp_font_size,str_out_area_shirt,glue_display.get_color(error_codes,b_show_cof),font_size,2)) 

        # 孔洞信息
        list_error_code=[]
        list_ng_region=[]
        error_codes=0
        for i in range(region_num):
            index = "region_{index}".format(index = list_region[i])
            obj_hole = obj_region[index]["region_info_hole"]
            region_type = obj["region_info"][index]["info_base"]["type"]
            if obj_hole["enable"]==True and region_type=="normal" :
                list_error_code.append(obj_hole["error_code"])
                list_ng_region.append(i)
        if len(list_error_code)>0:
            nums=nums+1
            str_out_hole="Glue coverage hole:"
            if sum(list_error_code)==0:
                str_out_hole=str_out_hole+"OK"
            else:
                if list_error_code.count(1)>0:
                    error_codes=1
                else:
                    error_codes=2
                if (error_codes!=2 and b_show_cof!=True ) or b_show_cof==True:
                    list_out_mes.append("Hole")
                str_out_hole=str_out_hole+"NG("
                for i in range(0,len(list_error_code)):
                    if list_error_code[i]!=0:
                        str_out_hole=str_out_hole+"R"+str(list_ng_region[i]+1)+","
                str_out_hole=str_out_hole+")"
            guiArray.Add(imageShowTextXY(offset_x,offset_y+(line_space+font_size)*(nums+2)+temp_font_size,str_out_hole,glue_display.get_color(error_codes,b_show_cof),font_size,2))    
        
        ####面积与宽度统一归类为GlueMissing 其中37 为GlueArea
        # 面积信息
        list_error_code=[]
        list_ng_region=[]
        error_codes=0
        for i in range(region_num):
            index = "region_{index}".format(index = list_region[i])
            obj_area = obj_region[index]["region_info_area"]
            region_type = obj["region_info"][index]["info_base"]["type"]
            if obj_area["enable"]==True and region_type=="normal":
                list_error_code.append(obj_area["error_code"])
                list_ng_region.append(i)
        # 胶宽信息
        list_error_code1=[]
        list_ng_region1=[]
        for i in range(region_num):
            index = "region_{index}".format(index = list_region[i])
            obj_width = obj_region[index]["region_info_width"]
            region_type = obj["region_info"][index]["info_base"]["type"]
            if obj_width["enable"]==True and region_type=="normal":
                list_error_code1.append(obj_width["error_code"])
                list_ng_region1.append(i)
                # 最短胶宽及位置显示
                min_x_start=obj_width["min_start_pt"]["x"]
                min_y_start=obj_width["min_start_pt"]["y"]
                min_x_end=obj_width["min_end_pt"]["x"]
                min_y_end=obj_width["min_end_pt"]["y"]                                
                if self.n_mirror_mode == 1:
                    min_x_start = self.n_image_width - min_x_start
                    min_x_end = self.n_image_width - min_x_end                    
                elif self.n_mirror_mode == 2: 
                    min_y_start = self.n_image_height - min_y_start
                    min_y_end = self.n_image_height - min_y_end
                pt1=GvVisionAssembly.sc2Vector(min_x_start,min_y_start)
                pt2=GvVisionAssembly.sc2Vector(min_x_end,min_y_end)
                lineSeg=GvVisionAssembly.scLineSeg(pt1,pt2)
                str_min_width_out="{min_width}".format(min_width=round(obj_width["min_val"],self.n_format))
                if obj_width["min_val"]==0.0:
                    pos_x=obj_region[index]["info_base"]["position"]["x"]+30
                    pos_y=obj_region[index]["info_base"]["position"]["y"]+30
                else:
                    pos_x=(min_x_start+min_x_end)/2+5
                    pos_y=(min_y_start+min_y_end)/2
                temp=abs(font_size-10)
                if temp<8:
                    temp=8
                ###是否显示最短胶宽 
                if bShowMinWidth==True:
                    guiArray.Add(ShowLineSeg(lineSeg,glue_display.get_color(obj_width["error_code"],b_show_cof),0,2))
                    guiArray.Add(imageShowTextXY(pos_x,pos_y,str_min_width_out,glue_display.get_color(obj_width["error_code"],b_show_cof),temp,2))
        #面积与宽度信息合并，先面积后宽度
        list_error_code.extend(list_error_code1)   
        list_ng_region.extend(list_ng_region1)        
        if len(list_error_code)>0:
            nums=nums+1
            str_out_width="Glue missing:"
            if sum(list_error_code)==0:
                str_out_width=str_out_width+"OK"
            else:
                if list_error_code.count(1)>0:
                    error_codes=1
                else:
                    error_codes=2
                #NG原因新增
                if error_codes==1:
                    list_out_mes.append("GlueMissing")
                    str_out_width=str_out_width+"NG("
                if error_codes==2 and b_show_cof==True:
                    list_out_mes.append("GlueMissing")
                if error_codes==2: 
                    if b_show_cof==True:
                        str_out_width=str_out_width+"NG("
                    else:
                        str_out_width=str_out_width+"OK("
                for i in range(0,len(list_error_code)):
                    if list_error_code[i]!=0:
                        str_out_width=str_out_width+"R"+str(list_ng_region[i]+1)+","
                str_out_width=str_out_width+")"
            guiArray.Add(imageShowTextXY(offset_x,offset_y+(line_space+font_size)*(nums+2)+temp_font_size,str_out_width,glue_display.get_color(error_codes,b_show_cof),font_size,2))  

        # 偏移信息
        list_error_code=[]
        list_ng_region=[]
        error_codes=0
        for i in range(region_num):
            index = "region_{index}".format(index = list_region[i])
            obj_shift = obj_region[index]["region_info_shift"]
            region_type = obj["region_info"][index]["info_base"]["type"]
            #距离判断
            if obj_shift["enable"]==True and region_type=="normal":
                list_error_code.append(obj_shift["error_code"])
                if obj_shift["error_code"]>0:
                    list_ng_region.append(i)
            #X距离判断
            try:
                obj_shiftX = obj_region[index]["region_info_shiftX"]
                if obj_shiftX["enable"]==True and region_type=="normal":
                    list_error_code.append(obj_shiftX["error_code"])
                    if obj_shiftX["error_code"]>0 and list_ng_region.count(i)==0:
                        list_ng_region.append(i)
            except:
                temp=0# 
            #Y距离判断
            try:
                obj_shiftY = obj_region[index]["region_info_shiftY"]
                if obj_shiftY["enable"]==True and region_type=="normal":
                    list_error_code.append(obj_shiftY["error_code"])
                    if obj_shiftY["error_code"]>0 and list_ng_region.count(i)==0:
                        list_ng_region.append(i)
            except:
                temp=0# 
        if len(list_error_code)>0 and b_show_shifit==True:
            nums=nums+1
            str_out_shift="Glue shift:"
            if sum(list_error_code)==0:
                str_out_shift=str_out_shift+"OK"
            else:
                list_ng_region.sort()
                if list_error_code.count(1)>0:
                    error_codes=1
                    str_out_shift=str_out_shift+"NG("
                else:
                    error_codes=2
                if (error_codes!=2 and b_show_cof!=True ) or b_show_cof==True:
                    list_out_mes.append("Shift")
                if error_codes==2: 
                    if b_show_cof==True:
                        str_out_shift=str_out_shift+"NG("
                    else:
                        str_out_shift=str_out_shift+"OK("
                for i in range(0,len(list_ng_region)):
                    str_out_shift=str_out_shift+"R"+str(list_ng_region[i]+1)+","
                str_out_shift=str_out_shift+")"
            guiArray.Add(imageShowTextXY(offset_x,offset_y+(line_space+font_size)*(nums+2)+temp_font_size,str_out_shift,glue_display.get_color(error_codes,b_show_cof),font_size,2))             

        # 断胶信息及轮廓
        if self.b_show_broken == True:
            nums=nums+1
            num_brocken=obj["detection_gap_info"]["num"]
            str_out_brocken="Glue path broken:"
            error_codes=0
            if num_brocken>0:#存在断胶
                error_codes=obj_base["error_code"]
                str_out_brocken=str_out_brocken+"NG"
                list_out_mes.append("Broken")
                ###显示NG区域及长度
                try:
                    for i in range(num_brocken):
                        index = "{index}".format(index = i)
                        broken_length=obj["detection_gap_info"][index]["info"]["width"]
                        str_out_brocken_length="{broken_data}".format(broken_data=round(broken_length,self.n_format))
                        start_x=obj["detection_gap_info"][index]["info"]["start_pt"]["X"]
                        start_y=obj["detection_gap_info"][index]["info"]["start_pt"]["Y"]
                        end_x=obj["detection_gap_info"][index]["info"]["end_pt"]["X"]
                        end_y=obj["detection_gap_info"][index]["info"]["end_pt"]["Y"]
                        if self.n_mirror_mode == 1:
                            start_x = self.n_image_width - start_x
                            end_x = self.n_image_width - end_x
                        elif self.n_mirror_mode == 2:
                            start_y = self.n_image_height - start_y
                            end_y = self.n_image_height - end_y
                        scVecVec = GvVisionAssembly.sc2VectorVec()
                        for key in obj["detection_gap_info"][index]["contour"].keys():
                            temp_x=obj["detection_gap_info"][index]["contour"][key]["X"]
                            temp_y=obj["detection_gap_info"][index]["contour"][key]["Y"]
                            if self.n_mirror_mode == 1:
                                temp_x = self.n_image_width - temp_x
                            elif self.n_mirror_mode == 2:
                                temp_y = self.n_image_height - temp_y
                            pt = GvVisionAssembly.sc2Vector(temp_x,temp_y)
                            scVecVec.append(pt)
                        guiArray.Add(imageShowPolyline(scVecVec,[255,0,0],line_width))
                        guiArray.Add(imageShowTextXY((start_x+end_x)/2,(end_y+start_y)/2,str_out_brocken_length,glue_display.get_color(1,b_show_cof),font_size))
                except:
                    temp=0#
            else:#不存在断胶
                str_out_brocken=str_out_brocken+"OK"
            guiArray.Add(imageShowTextXY(offset_x,offset_y+(line_space+font_size)*(nums+2)+temp_font_size,str_out_brocken,glue_display.get_color(error_codes,b_show_cof),font_size,2))
        
        # 溢胶信息及轮廓，启用显示，不启用显示
        #判断是否有溢胶区域
        overflow_region_num=0
        error_codes_list=[]
        for i in range(0,obj["base_info"]["region_number"]):
            index = "region_{index}".format(index = i)
            region_type = obj["region_info"][index]["info_base"]["type"]
            #溢胶区域判断
            if region_type!="normal" and obj_region[index]["region_info_area"]["enable"]==True:
                overflow_region_num=overflow_region_num+1
                error_codes_list.append(obj_region[index]["region_info_area"]["error_code"])
        #有溢胶区域才进行显示
        if overflow_region_num>0 and b_show_overflow==True:
            nums=nums+1
            num_overflow=obj["detection_overflow_info"]["num"]
            str_out_overflow="Overflow:"
            error_codes=0
            if num_overflow>0:
            #error_codes状态判断
                if error_codes_list.count(1)>0:
                    error_codes=1
                else:
                    error_codes=2
                tempdatas=0
                str_out_overflow=str_out_overflow+"NG"
                if error_codes==2: 
                    if b_show_cof!=True:
                        str_out_overflow="Overflow:OK"
                if b_show_cof==True or error_codes==1:
                    list_out_mes.append("Overflow")
                ###溢胶序号排序
                startIndex=0
                for i in range(0,obj["base_info"]["region_number"]):
                    key ="region_{index}".format(index = i)   
                    region_type = obj["region_info"][key]["info_base"]["type"]
                    if region_type =="normal":
                        startIndex=startIndex+1
                ###计算溢胶面积，各区域单独输出
                str_area_overflow=[]
                list_error_code=[]
                for i in range(0,obj["base_info"]["region_number"]):
                    if i<startIndex:
                        continue
                    key ="region_{index}".format(index = i)   
                    region_type = obj["region_info"][key]["info_base"]["type"]
                    if region_type=="overflow":
                        list_error_code.append(obj["region_info"][key]["info_base"]["error_code"])
                        if obj["region_info"][key]["info_base"]["error_code"]>0:
                            val=round(obj["region_info"][key]["region_info_area"]["current_val"],self.n_format)
                            lsl=round(obj["region_info"][key]["region_info_area"]["lower_spec"],2)
                            usl=round(obj["region_info"][key]["region_info_area"]["upper_spec"],2)
                            str_temp_data="OF{index}".format(index = (i+1-startIndex))+": {overflow_data}({LSL_data},{USL_data})".format(overflow_data=val,LSL_data=lsl,USL_data=usl)
                            str_area_overflow.append(str_temp_data)
                if list_error_code.count(1)>0:
                    error_codes=1
                ###显示NG区域轮廓
                try:
                    for i in range(num_overflow):
                        index = "{index}".format(index = i)               
                        scVecVec = GvVisionAssembly.sc2VectorVec()
                        for key in obj["detection_overflow_info"][index]["contour"].keys():
                            temp_x=obj["detection_overflow_info"][index]["contour"][key]["X"]
                            temp_y=obj["detection_overflow_info"][index]["contour"][key]["Y"]
                            if self.n_mirror_mode == 1:
                                temp_x = self.n_image_width - temp_x          
                            elif self.n_mirror_mode == 2: 
                                temp_y = self.n_image_height - temp_y
                            pt = GvVisionAssembly.sc2Vector(temp_x,temp_y)
                            scVecVec.append(pt)
                        #if b_show_cof==True:
                        guiArray.Add(imageShowPolyline(scVecVec,glue_display.get_color(error_codes,b_show_cof),line_width))
                except:
                    print("No Counter")
                #并入溢胶面积
                #if len(str_area_overflow)>0 and b_show_cof==True:
                if len(str_area_overflow)>0:
                    str_out_overflow=str_out_overflow+"("
                    for str_data in str_area_overflow:
                        str_out_overflow=str_out_overflow+str_data+","
                    str_out_overflow=str_out_overflow+")"
            else:
                str_out_overflow=str_out_overflow+"OK"
            guiArray.Add(imageShowTextXY(offset_x,offset_y+(line_space+font_size)*(nums+2)+temp_font_size,str_out_overflow,glue_display.get_color(error_codes,b_show_cof),font_size,2))

        # 胶长信息
        list_error_code=[]
        str_length=[]
        enable_flage=False
        error_codes=0
        str_out_length="Gluelength:"
        lenght_index=0
        for key in obj["glue_length_info"].keys():
            lenght_index=lenght_index+1
            if obj["glue_length_info"][key]["enable"]==True:
                enable_flage=True
                if obj["glue_length_info"][key]["error_code"]>0:
                    list_error_code.append(obj["glue_length_info"][key]["error_code"])
                    lengh_dat=round(obj["glue_length_info"][key]["current_val"],self.n_format)
                    lsl=round(obj["glue_length_info"][key]["lower_spec"],2)
                    usl=round(obj["glue_length_info"][key]["upper_spec"],2)
                    str_temp_data="Length"+str(lenght_index)+":{lenght}({LSL_data},{USL_data})".format(lenght=lengh_dat,LSL_data=lsl,USL_data=usl)
                    str_length.append(str_temp_data)  
        #启用显示，不启用显示
        if enable_flage==True and b_show_lenght==True:
            if len(list_error_code)>0:
                if list_error_code.count(1)>0:
                    error_codes=1
                else:
                    error_codes=2
                str_out_length=str_out_length+"NG"
                if error_codes==2: 
                    if b_show_cof!=True:
                        str_out_length="Gluelength:OK"
                if (error_codes!=2 and b_show_cof!=True ) or b_show_cof==True:
                    list_out_mes.append("Gluelength")
                #if error_codes>0 and b_show_cof==True:
                if error_codes>0:
                    str_out_length=str_out_length+"("
                    for str_data in str_length:
                        str_out_length=str_out_length+str_data+","
                    str_out_length=str_out_length+")"
            else:
                str_out_length=str_out_length+"OK"
            nums=nums+1
            guiArray.Add(imageShowTextXY(offset_x,offset_y+(line_space+font_size)*(nums+2)+temp_font_size,str_out_length,glue_display.get_color(error_codes,b_show_cof),font_size,2))
        
        #缺胶信息
        if b_show_lackglue==True:
            show_errorcode=0
            nums=nums+1
            num_LackGlue=obj["detection_less_info"]["num"]
            str_out_LackGlue="LessGlue:"
            if num_LackGlue>0:
                list_out_mes.append("LessGlue")
                str_out_LackGlue=str_out_LackGlue+"NG"
                show_errorcode=1
            else:
                str_out_LackGlue=str_out_LackGlue+"OK"
            guiArray.Add(imageShowTextXY(offset_x,offset_y+(line_space+font_size)*(nums+2)+temp_font_size,str_out_LackGlue,glue_display.get_color(show_errorcode,b_show_cof),font_size,2))
        
        #NG信息  
        if len(list_out_mes)>0:
            str_out_mes="NG reason:"
            for i in list_out_mes:
                str_out_mes=str_out_mes+i+"/"
        guiArray.Add(imageShowTextXY(offset_x,offset_y+(line_space+font_size)*2+temp_font_size,str_out_mes,glue_display.get_color(error_code = obj_base["error_code"],b_show_cof=b_show_cof),font_size))       
        
        return guiArray 
        
    # Dùng để vẽ vùng ROI kiểm tra
    # guiArray : GuiArray dùng để hiển thị
    # str_info : dữ liệu đầu ra keo hình dạng đặc biệt
    # list_region: kiểu list, vùng (hoặc nhiều vùng) muốn hiển thị, nếu là None thì mặc định hiển thị tất cả các vùng
    # show_OK: có hiển thị vùng OK hay không, mặc định là True (hiển thị), nếu đặt false thì vùng OK không hiển thị (vùng NG bắt buộc hiển thị)
    # font_size: cỡ chữ hiển thị
    # line_width: độ rộng đường kẻ hiển thị
    # b_show_cof: True thì COF hiển thị màu vàng và dữ liệu chi tiết, False thì COF hiển thị màu xanh lá và ẩn dữ liệu chi tiết
    def show_detetion_Region(self,guiArray,str_info,list_region=None,show_OK=True,font_size=40,line_width=3,b_show_cof=True):
        #obj = json.loads(str_info)
        revise_OF_index=True#溢胶序号重新排序
        obj=str_info
        if list_region!=None:
            list_region.sort()
            region_num = len(list_region)
        else:
            region_num = obj["base_info"]["region_number"]
            list_region=[]
            for i in range(region_num):
                list_region.append(i)
        #错误信息提示
        if len(list_region)>obj["base_info"]["region_number"] or max(list_region)>obj["base_info"]["region_number"]-1:
            str_error_msg="显示区域个数{}超出工具设置个数{}或显示区域索引{}超出工具索引{}".format(len(list_region),obj["base_info"]["region_number"],max(list_region),obj["base_info"]["region_number"]-1)
            raise ValueError(str_error_msg)
        obj_region = obj["region_info"]
        ###溢胶序号排序
        startIndex=0
        for i in range(0,obj["base_info"]["region_number"]):
            key ="region_{index}".format(index = i)   
            region_type = obj["region_info"][key]["info_base"]["type"]
            if region_type == "normal":
                startIndex=startIndex+1               
        for i in range(region_num):
            index = "region_{index}".format(index = list_region[i])
            obj_single = obj_region[index]            
            # 显示轮廓
            obj_base = obj_single["info_base"]            
            # 区域错误码
            error_code = obj_base["error_code"]            
            # 区域颜色
            clr = glue_display.get_color(error_code,b_show_cof)
            #print(error_code)
            
            #判断当前检测区域是否实际检测了内容
            region_type = obj_single["info_base"]["type"]
            b_region_enable=False
            try:
                if obj_single["region_info_length"]["enable"]==True:
                    b_region_enable=True
            except:
                b_region_enable=False#
            if obj_single["region_info_width"]["enable"]==True:
                b_region_enable=True
            if obj_single["region_info_shift"]["enable"]==True:
                b_region_enable=True
            try:
                if obj_single["region_info_shiftX"]["enable"]==True:
                    b_region_enable=True
            except:
                b_region_enable=False#
            try:
                if obj_single["region_info_shiftY"]["enable"]==True:
                    b_region_enable=True
            except:
                b_region_enable=False#
            if obj_single["region_info_hole"]["enable"]==True:
                b_region_enable=True
            if obj_single["region_info_area"]["enable"]==True:
                b_region_enable=True
            if obj_single["region_info_areashift"]["enable"]==True: 
                b_region_enable=True      
            
            obj_contour = obj_base["contour"]
            scVecVec = GvVisionAssembly.sc2VectorVec()
            for key,obj_polyline in obj_contour.items():
                if self.n_mirror_mode == 0:
                    pt = GvVisionAssembly.sc2Vector(obj_polyline["X"],obj_polyline["Y"])
                if self.n_mirror_mode == 1:
                    pt = GvVisionAssembly.sc2Vector(self.n_image_width - obj_polyline["X"],obj_polyline["Y"])
                if self.n_mirror_mode == 2:
                    pt = GvVisionAssembly.sc2Vector(obj_polyline["X"],self.n_image_height - obj_polyline["Y"])
                scVecVec.append(pt)
            if (show_OK==True or error_code==1 or (error_code==2 and b_show_cof==True)) and b_region_enable==True:
                #print(error_code)
                guiArray.Add(imageShowPolyline(scVecVec,clr,line_width))
                str_out = "R{}".format(list_region[i]+1)
                if revise_OF_index!=True and obj_base["type"]=="overflow":
                    str_out = "R{}".format(list_region[i]+1-startIndex)
                if self.n_mirror_mode == 0:
                    X=obj_polyline["X"]
                    Y=obj_polyline["Y"]
                if self.n_mirror_mode == 1:
                    X=self.n_image_width-obj_polyline["X"]
                    Y=obj_polyline["Y"]
                if self.n_mirror_mode == 2:
                    X=obj_polyline["X"]
                    Y=self.n_image_height - obj_polyline["Y"]
                guiArray.Add(imageShowTextXY(X,Y,str_out,clr,font_size))
        return guiArray

    # Dùng để hiển thị thông tin NG
    # guiArray : Đối tượng GuiArray dùng để hiển thị
    # str_info : Dữ liệu đầu ra kiểm tra keo dị hình (dạng JSON)
    # list_region : Giá trị int đơn, biểu thị số thứ tự vùng cần hiển thị (bắt đầu từ 0)
    # font_size : Cỡ chữ hiển thị
    # offset_x : Độ lệch hiển thị theo trục X (so với trọng tâm ROI kiểm tra)
    # offset_y : Độ lệch hiển thị theo trục Y (so với trọng tâm ROI kiểm tra)
    # line_space : Khoảng cách giữa các dòng hiển thị
    # b_show_cof : True hiển thị COF màu vàng và thông tin chi tiết; False hiển thị COF màu xanh và ẩn thông tin chi tiết
    def show_NG_data(self,guiArray,str_info,show_region,font_size=40,offset_x=0,offset_y=0,line_space=0,b_show_cof=True):
        #obj = json.loads(str_info)
        obj=str_info
        ### Lấy chỉ số vùng keo tràn
        over_flow_index=[]
        for i in range(0,obj["base_info"]["region_number"]):
            key ="region_{index}".format(index = i)   
            region_type = obj["region_info"][key]["info_base"]["type"]
            if region_type =="overflow":
                over_flow_index.append(i)
        # Thông báo lỗi
        if show_region>obj["base_info"]["region_number"]-1:
            str_error_msg="显示区域索引{}超出工具索引{}".format(show_region,obj["base_info"]["region_number"]-1)
            raise ValueError(str_error_msg)
        obj_region = obj["region_info"]
        index = "region_{index}".format(index = show_region)
        nums=0
        # Phân loại vùng
        region_type = obj_region[index]["info_base"]["type"]
        # Thông tin chiều rộng keo
        obj_width = obj_region[index]["region_info_width"]
        error_code = obj_width["error_code"]
        obj_width_enable = obj_width["enable"]
        if error_code!=0 and obj_width_enable==True and region_type=="normal":
            nums=nums+1
            if obj_width["min_val"]<obj_width["lower_spec"]:
                out_width_data=obj_width["min_val"]
            elif obj_width["max_val"]>obj_width["upper_spec"]:
                out_width_data=obj_width["max_val"]
            else:
                out_width_data=obj_width["average_val"]
            out_width_data=round(out_width_data,self.n_format)
            lsl=round(obj_width["lower_spec"],2)
            usl=round(obj_width["upper_spec"],2)
            str_out = "R{index}".format(index = (show_region+1))+":Width NG:{widht}({LSL_data},{USL_data})".format(widht=out_width_data,LSL_data=lsl,USL_data=usl) 
            pos_x = offset_x+obj_region[index]["info_base"]["position"]["x"]
            pos_y = offset_y+obj_region[index]["info_base"]["position"]["y"]+(font_size+line_space)*(nums-1)
            if self.n_mirror_mode == 1:
                pos_x = self.n_image_width - pos_x
            elif self.n_mirror_mode == 2:
                pos_y = self.n_image_height - pos_y
            # Hiển thị
            if  (error_code==1)  or (error_code==2 and b_show_cof==True): 
                guiArray.Add(imageShowTextXY(pos_x,pos_y,str_out,glue_display.get_color(error_code,b_show_cof),font_size))

        
        # Thông tin diện tích keo
        obj_area = obj_region[index]["region_info_area"]
        error_code = obj_area["error_code"]
        obj_area_enable = obj_area["enable"]
        if error_code!=0 and obj_area_enable==True and region_type=="normal":
            nums=nums+1
            out_area_data=round(obj_area["current_val"],self.n_format)
            lsl=round(obj_area["lower_spec"],2)
            usl=round(obj_area["upper_spec"],2)
            str_out = "R{index}".format(index = (show_region+1))+":Area NG:{area_data}({LSL_data},{USL_data})".format(area_data=out_area_data,LSL_data=lsl,USL_data=usl)
            show_index=show_region
            if region_type=="overflow":
                for temp_i in range(0,len(over_flow_index)):
                    if show_region==over_flow_index[temp_i]:
                        show_index=temp_i+1
                str_out = "OF{index}".format(index = (show_index))+":{area_data}({LSL_data},{USL_data})".format(area_data=out_area_data,LSL_data=lsl,USL_data=usl)
            pos_x = offset_x+obj_region[index]["info_base"]["position"]["x"]
            pos_y = offset_y+obj_region[index]["info_base"]["position"]["y"]+(font_size+line_space)*(nums-1)
            if self.n_mirror_mode == 1:
                pos_x = self.n_image_width - pos_x
            elif self.n_mirror_mode == 2:
                pos_y = self.n_image_height - pos_y           
            # Hiển thị
            if  (error_code==1)  or (error_code==2 and b_show_cof==True): 
                guiArray.Add(imageShowTextXY(pos_x,pos_y,str_out,glue_display.get_color(error_code,b_show_cof),font_size))
 
        # Thông tin tỷ lệ keo phủ
        obj_area_shift = obj_region[index]["region_info_areashift"]
        error_code = obj_area_shift["error_code"]
        #print(error_code)
        obj_area_shift_enable = obj_area_shift["enable"]
        if error_code!=0 and obj_area_shift_enable==True and region_type=="normal":
            nums=nums+1
            out_area_shift_data=round(obj_area_shift["current_val"],self.n_format)
            lsl=round(obj_area_shift["lower_spec"],2)
            usl=round(obj_area_shift["upper_spec"],2)
            str_out = "R{index}".format(index = (show_region+1))+":CoverShift NG:{area_shift_data}({LSL_data},{USL_data})".format(area_shift_data=out_area_shift_data,LSL_data=lsl,USL_data=usl)            
            pos_x = offset_x+obj_region[index]["info_base"]["position"]["x"]
            pos_y = offset_y+obj_region[index]["info_base"]["position"]["y"]+(font_size+line_space)*(nums-1)
            if self.n_mirror_mode == 1:
                pos_x = self.n_image_width - pos_x
            elif self.n_mirror_mode == 2:
                pos_y = self.n_image_height - pos_y         
            #显示
            if  (error_code==1)  or (error_code==2 and b_show_cof==True):    
                guiArray.Add(imageShowTextXY(pos_x,pos_y,str_out,glue_display.get_color(error_code,b_show_cof),font_size))           
        
       #位置信息
        obj_shift = obj_region[index]["region_info_shift"]
        error_code = obj_shift["error_code"]
        obj_shift_enable = obj_shift["enable"]
        if error_code!=0 and obj_shift_enable==True and region_type=="normal":
            nums=nums+1
            out_shift_data=round(obj_shift["current_val"],self.n_format)
            lsl=round(obj_shift["lower_spec"],2)
            usl=round(obj_shift["upper_spec"],2)
            str_out = "R{index}".format(index = (show_region+1))+":Shift NG: {shift_data}({LSL_data},{USL_data})".format(shift_data=out_shift_data,LSL_data=lsl,USL_data=usl)
            pos_x = offset_x+obj_region[index]["info_base"]["position"]["x"]
            pos_y = offset_y+obj_region[index]["info_base"]["position"]["y"]+(font_size+line_space)*(nums-1)
            if self.n_mirror_mode == 1:
                pos_x = self.n_image_width - pos_x
            elif self.n_mirror_mode == 2:
                pos_y = self.n_image_height - pos_y            
            #显示
            if  (error_code==1)  or (error_code==2 and b_show_cof==True): 
                guiArray.Add(imageShowTextXY(pos_x,pos_y,str_out,glue_display.get_color(error_code,b_show_cof),font_size))          

        try:
            #X位置信息
            obj_shiftX = obj_region[index]["region_info_shiftX"]
            error_code = obj_shiftX["error_code"]
            obj_shift_enable = obj_shiftX["enable"]
            if error_code!=0 and obj_shift_enable==True and region_type=="normal":
                nums=nums+1
                out_shiftX_data=round(obj_shiftX["current_val"],self.n_format)
                lsl=round(obj_shiftX["lower_spec"],2)
                usl=round(obj_shiftX["upper_spec"],2)
                str_out = "R{index}".format(index = (show_region+1))+":ShiftX NG: {shiftX_data}({LSL_data},{USL_data})".format(shiftX_data=out_shiftX_data,LSL_data=lsl,USL_data=usl)
                pos_x = offset_x+obj_region[index]["info_base"]["position"]["x"]
                pos_y = offset_y+obj_region[index]["info_base"]["position"]["y"]+(font_size+line_space)*(nums-1)
                if self.n_mirror_mode == 1:
                    pos_x = self.n_image_width - pos_x
                elif self.n_mirror_mode == 2:
                    pos_y = self.n_image_height - pos_y        
                #显示
                if  (error_code==1)  or (error_code==2 and b_show_cof==True):     
                    guiArray.Add(imageShowTextXY(pos_x,pos_y,str_out,glue_display.get_color(error_code,b_show_cof),font_size)) 
        except:
            tempi=0#

        try:
            #Y位置信息
            obj_shiftY = obj_region[index]["region_info_shiftY"]
            error_code = obj_shiftY["error_code"]
            obj_shift_enable = obj_shiftY["enable"]
            if error_code!=0 and obj_shift_enable==True and region_type=="normal":
                nums=nums+1
                out_shiftY_data=round(obj_shiftY["current_val"],self.n_format)
                lsl=round(obj_shiftY["lower_spec"],2)
                usl=round(obj_shiftY["upper_spec"],2)
                str_out = "R{index}".format(index = (show_region+1))+":ShiftY NG: {shiftY_data}({LSL_data},{USL_data})".format(shiftY_data=out_shiftY_data,LSL_data=lsl,USL_data=usl)
                pos_x = offset_x+obj_region[index]["info_base"]["position"]["x"]
                pos_y = offset_y+obj_region[index]["info_base"]["position"]["y"]+(font_size+line_space)*(nums-1)
                if self.n_mirror_mode == 1:
                    pos_x = self.n_image_width - pos_x
                elif self.n_mirror_mode == 2:
                    pos_y = self.n_image_height - pos_y            
                #显示
                if  (error_code==1)  or (error_code==2 and b_show_cof==True): 
                    guiArray.Add(imageShowTextXY(pos_x,pos_y,str_out,glue_display.get_color(error_code,b_show_cof),font_size)) 
        except:
            tempi=0#

        #孔洞信息
        obj_hole = obj_region[index]["region_info_hole"]
        error_code = obj_hole["error_code"]
        obj_hole_enable = obj_hole["enable"]
        if error_code!=0 and obj_hole_enable==True and region_type=="normal":
            nums=nums+1
            out_hole_data=round(obj_hole["current_val"],self.n_format)
            lsl=round(obj_hole["lower_spec"],2)
            usl=round(obj_hole["upper_spec"],2)
            if obj_region[index]["region_info_area"]["current_val"]>0:
                temp_hole_area_rate=round(obj_hole["current_val"]/obj_region[index]["region_info_area"]["current_val"],3)
            else:
                temp_hole_area_rate=round(0.0,3)
            str_out = "R{index}".format(index = (show_region+1))+":Hole NG: {hole_data}({LSL_data},{USL_data})/{hole_rate_data}".format(hole_data=out_hole_data,LSL_data=lsl,USL_data=usl,hole_rate_data=temp_hole_area_rate)
            pos_x = offset_x+obj_region[index]["info_base"]["position"]["x"]
            pos_y = offset_y+obj_region[index]["info_base"]["position"]["y"]+(font_size+line_space)*(nums-1)
            if self.n_mirror_mode == 1:
                pos_x = self.n_image_width - pos_x
            elif self.n_mirror_mode == 2:
                pos_y = self.n_image_height - pos_y           
             #显示
            if  (error_code==1)  or (error_code==2 and b_show_cof==True): 
                guiArray.Add(imageShowTextXY(pos_x,pos_y,str_out,glue_display.get_color(error_code,b_show_cof),font_size))        

        return guiArray  

class detection_operator():
    obj_single = json.loads("""{}""")  
    error_code_total = 0
    # Thông tin cơ bản vùng kiểm tra
    str_base_info = """{"index":0,"error_code":0,"position":{"x":0,"y":0}}"""
    # Thông tin các loại lỗi phát hiện (số lượng từng loại)
    str_detection_info = """{"width_much":0,"width_less":0,"width_off":0,
"shift_over":0,"shift_lack":0,"hole":0,"area_over":0,"area_lack":0,
"residue":0,"overflow":0,"spot":0,"sparse":0,"tail":0}"""
    # Thông tin kiểm tra thông thường (loại lỗi đơn giản)
    str_normal_info = """{"error_code":0,"enable":true,"current_val":0,"lower_spec":0,"upper_spec":0}"""
    obj_normal = json.loads(str_normal_info)
    # Thông tin mở rộng kiểm tra (thông số như độ rộng, vị trí,...)
    str_normal_info_ex = """{"error_code":0,"enable":true,"average_val":0,"min_val":0,"max_val":0,
"lower_spec":0,"upper_spec":0,
"max_start_pt":{"x":0,"y":0},"max_end_pt":{"x":0,"y":0},
"min_start_pt":{"x":0,"y":0},"min_end_pt":{"x":0,"y":0}}"""

    # Gán các thông tin vào đối tượng đơn vùng kiểm tra
    obj_normal_ex = json.loads(str_normal_info_ex)
    obj_single["info_base"] = json.loads(str_base_info)
    obj_single["region_info_detection"] = json.loads(str_detection_info)
    obj_single["region_info_width"] = obj_normal_ex
    obj_single["region_info_shift"] = obj_normal_ex
    obj_single["region_info_hole"] = obj_normal
    obj_single["region_info_area"] = obj_normal
    obj_single["region_info_spot"] = obj_normal
    obj_single["region_info_aspectratio"] = obj_normal
    obj_single["region_info_areashift"] = obj_normal

    # Đối tượng tổng hợp kết quả kiểm tra
    obj_total = json.loads("""{}""")       
    
    def __init__(self):
        self;

    # Hàm thiết lập thông tin về độ rộng keo
    def set_width(cur_mean,cur_max,cur_min,spec_max,spec_min,error_code):
        # Cập nhật giá trị đo được
        detection_operator.obj_single["region_info_width"]["average_val"] = cur_mean
        detection_operator.obj_single["region_info_width"]["min_val"] = cur_min
        detection_operator.obj_single["region_info_width"]["max_val"] = cur_max
        detection_operator.obj_single["region_info_width"]["lower_spec"] = spec_min
        detection_operator.obj_single["region_info_width"]["upper_spec"] = spec_max
        # Cập nhật mã lỗi
        detection_operator.obj_single["region_info_width"]["error_code"] = error_code
        detection_operator.error_code_total = error_code
        # Cập nhật trạng thái kiểm tra tổng thể
        if cur_min == 0:
            detection_operator.obj_single["region_info_detection"]["width_off"] = 1
        if cur_min < spec_min:
            detection_operator.obj_single["region_info_detection"]["width_less"] = 1
        if cur_max > spec_max:
            detection_operator.obj_single["region_info_detection"]["width_much"] = 1        
        return True
        
    def set_shift(cur_mean,cur_max,cur_min,spec_max,spec_min,error_code):
        detection_operator.obj_single["region_info_shift"]["average_val"] = cur_mean
        detection_operator.obj_single["region_info_shift"]["min_val"] = cur_min
        detection_operator.obj_single["region_info_shift"]["max_val"] = cur_max
        detection_operator.obj_single["region_info_shift"]["lower_spec"] = spec_min
        detection_operator.obj_single["region_info_shift"]["upper_spec"] = spec_max
        # Cập nhật mã lỗi
        detection_operator.obj_single["region_info_shift"]["error_code"] = error_code
        detection_operator.error_code_total = error_code
        # Cập nhật trạng thái kiểm tra tổng thể
        if cur_min < spec_min:
            detection_operator.obj_single["region_info_detection"]["shift_lack"] = 1
        if cur_max > spec_max:
            detection_operator.obj_single["region_info_detection"]["shift_over"] = 1             
        return True
        
    def set_hole(cur_mean,spec_max,spec_min,error_code):
        detection_operator.obj_single["region_info_hole"]["average_val"] = cur_mean
        detection_operator.obj_single["region_info_hole"]["lower_spec"] = spec_min
        detection_operator.obj_single["region_info_hole"]["upper_spec"] = spec_max
        detection_operator.obj_single["region_info_hole"]["error_code"] = error_code
        detection_operator.error_code_total = error_code
        detection_operator.obj_single["region_info_detection"]["hole"] = 1 
        return True 

    def set_area(cur_mean,spec_max,spec_min,error_code):
        detection_operator.obj_single["region_info_area"]["average_val"] = cur_mean
        detection_operator.obj_single["region_info_area"]["lower_spec"] = spec_min
        detection_operator.obj_single["region_info_area"]["upper_spec"] = spec_max
        detection_operator.obj_single["region_info_area"]["error_code"] = error_code
        detection_operator.error_code_total = error_code
        detection_operator.obj_single["region_info_detection"]["hole"] = 1 
        return True
    def set_spot(cur_mean,spec_max,spec_min,error_code):
        detection_operator.obj_single["region_info_spot"]["average_val"] = cur_mean
        detection_operator.obj_single["region_info_spot"]["lower_spec"] = spec_min
        detection_operator.obj_single["region_info_spot"]["upper_spec"] = spec_max
        detection_operator.obj_single["region_info_spot"]["error_code"] = error_code
        detection_operator.error_code_total = error_code
        detection_operator.obj_single["region_info_detection"]["hole"] = 1 
        return True
    def set_aspectratio(cur_mean,spec_max,spec_min,error_code):
        detection_operator.obj_single["region_info_aspectratio"]["average_val"] = cur_mean
        detection_operator.obj_single["region_info_aspectratio"]["lower_spec"] = spec_min
        detection_operator.obj_single["region_info_aspectratio"]["upper_spec"] = spec_max
        detection_operator.obj_single["region_info_aspectratio"]["error_code"] = error_code
        detection_operator.error_code_total = error_code
        return True
    def set_areashift(cur_mean,spec_max,spec_min,error_code):
        detection_operator.obj_single["region_info_areashift"]["average_val"] = cur_mean
        detection_operator.obj_single["region_info_areashift"]["lower_spec"] = spec_min
        detection_operator.obj_single["region_info_areashift"]["upper_spec"] = spec_max
        detection_operator.obj_single["region_info_areashift"]["error_code"] = error_code
        detection_operator.error_code_total = error_code
        return True                         
    def get_result(strOrg):
        # Chuyển chuỗi JSON đầu vào thành đối tượng
        # Tạo thông tin tổng hợp từ chuỗi JSON đầu vào
        detection_operator.obj_total = json.loads(strOrg)
        # Lấy số vùng hiện tại, cần tính lại
        region_num = detection_operator.obj_total["base_info"]["region_number"]
        # Tăng số vùng lên 1
        detection_operator.obj_total["base_info"]["region_number"] = region_num + 1       
        # Cập nhật chỉ số vùng mới cho đối tượng đơn vùng kiểm tra
        detection_operator.obj_single["info_base"]["index"] = region_num + 1
        # Cập nhật mã lỗi tổng cho đối tượng đơn vùng kiểm tra
        detection_operator.obj_single["error_code"] = detection_operator.error_code_total
        # Tạo khóa vùng mới
        region_index = f"region_{region_num}"
        # Thêm đối tượng đơn vùng kiểm tra vào thông tin vùng tổng hợp
        detection_operator.obj_total["region_info"][region_index] = detection_operator.obj_single
        # Trả về đối tượng tổng hợp sau khi cập nhật
        return detection_operator.obj_total

class database_operator():
    # 记录数据字典
    mes_dict = {}

    # 姿态索引
    pos_index = 1
    detail_table_name = "REGION_INFO_1"
    base_table_name = "BASE_INFO_1"

    def getmes(self):
        return self.mes_dict
    
    # 设置数据姿态
    # 1: 姿态1
    # 2: 姿态2
    # ...
    # 用于处理同一片产品不同姿态的情况    
    def set_pos(self,pos):
        self.pos_index = pos
        self.base_table_name = "BASE_INFO_{}".format(self.pos_index)
        self.detail_table_name = "REGION_INFO_{}".format(self.pos_index)

    def record_datas(self,str_out,str_file_path,str_today,str_pic_cap,str_pic_raw,n_mes):        
         error_info=str(self.inner_record_data(str_out,str_file_path,str_today,str_pic_cap,str_pic_raw,n_mes))
         if "OK" not in error_info:
            strCurTime=datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
            #strCurDate=datetime.datetime.now().strftime('%Y%m%d')
            shutil.copyfile(str_file_path + "\\" +str_today+ "\\" + str_today + ".db", str_file_path + "\\" + str_today+"\\"+ strCurTime+"_备份"+ ".db")
            os.remove(str_file_path + "\\" + str_today+ "\\" + str_today + ".db")
            self.inner_record_data(str_out,str_file_path,str_today,str_pic_cap,str_pic_raw,n_mes)
            
            
    def inner_record_data(self,str_out,str_file_path,str_today,str_pic_cap,str_pic_raw,n_mes):
        # 数据生成
        #obj = json.loads(str_out)
        obj=str_out
        # 连接到SQLite数据库
        # 数据库文件依据上位机发送的时间来命名的.db文件
        if not os.path.exists(str_file_path):
            os.mkdir(str_file_path)

        #生成数据库
        #strCurDate=datetime.datetime.now().strftime('%Y%m%d')

        str_file_path_new=str_file_path + "\\" + str_today
        if not os.path.exists(str_file_path_new):
            os.mkdir(str_file_path_new)
        str_path = str_file_path_new + "\\" + str_today+ ".db"

        #连接数据库
        conn = sqlite3.connect(str_path)
        #关闭写同步
        conn.execute("PRAGMA synchronous = OFF")

        cursor = conn.cursor()

        # 查询表是否存在 -- 基础信息
        cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name=?",(self.base_table_name,))
        result = cursor.fetchone()

        # 解析基础信息
        obj_base_info = obj["base_info"]
 
        if result == None:
            sql_createTb = """CREATE TABLE {} (
        SN  CHAR(20),
        TIME CHAR(20),
        ERRORCODE INT,
        REGION_NUMBER INT)
        """.format(self.base_table_name)
            
            cursor.execute(sql_createTb)
            
        # 插入基础数据
        str_insert = """INSERT OR IGNORE INTO {} VALUES ('{sn}', '{time}', '{errorcode}', '{regionnum}')""".format(self.base_table_name,sn=obj_base_info["SN"], \
        time=obj_base_info["time"],errorcode=obj_base_info["error_code"], regionnum=obj_base_info["region_number"])
        conn.execute(str_insert)            
        n_region_num = obj_base_info["region_number"]
        
        #解析region info
        obj_region_info = obj["region_info"]        
        str_region_table = """CREATE TABLE {} (SN  CHAR(20),TIME CHAR(20),ERRORCODE INT""".format(self.detail_table_name)
        str_region_header = """SN,TIME,ERRORCODE"""
        str_region_insert = """INSERT OR IGNORE INTO {} VALUES ('{sn}', '{time}','{errorcode}'""".format(self.detail_table_name,sn=obj_base_info["SN"], \
        time=obj_base_info["time"],errorcode=obj_base_info["error_code"])
        strStoreName="info_base region_info_detection"   
        
        #创建待统计项的空列表，用于统计各区域的各项failure
        AreaShift_errorcode=[]   
        Hole_errorcode=[]
        Shift_errorcode=[]
        Width_errorcode=[]
        Area_errorcode=[]
        #---------------------------------------------------------------------
        #分层解析region信息，info base与region_info_detection不带enable，单独解析        
        for region_index,region_single in obj_region_info.items():
            # 前缀  eg: region_0
            region_prefix = region_index + "_"
            # 遍历第一层 eg: detection_info/width_info...
            for detection_index in region_single:
                obj_detection = region_single[detection_index] 
                #print(detection_index)               
                if str(detection_index) in strStoreName:            

                    #不存储region_info_detection的字典
                    if(detection_index == "region_info_detection"):
                        continue

                    if (type(obj_detection) == type(json.loads("""{}"""))):
                        for item_detail in obj_detection:
                            obj_detail = obj_detection[item_detail]
                            if (type(obj_detail) != type(json.loads("""{}"""))):
                                data_type = "REAL" # 默认是浮点
                                
                                if(type(obj_detail) == type(""))or str(obj_detail)=="normal":
                                    data_type = "CHAR(100)"
                                if(type(obj_detail) == type(True)):
                                   data_type = "INT"
                                   if obj_detail == True:
                                       obj_detail = 1
                                   else:
                                       obj_detail = 0                         
                                str_region_table += "," + region_prefix + detection_index + "_" + item_detail + "  " + data_type
                                str_region_header +=","+region_prefix +detection_index + "_"+item_detail
                                str_value = """'{value}'""".format(value=obj_detail)
                                str_region_insert += "," + str_value  
                                 
                else:
                    if (type(obj_detection) == type(json.loads("""{}"""))):
                         for item_detail in obj_detection:
                            obj_detail = obj_detection[item_detail]
                            #print(item_detail,obj_detail)
                            if (type(obj_detail) != type(json.loads("""{}"""))):
                                data_type = "REAL" # 默认是浮点
                                if(type(obj_detail) == type("")):
                                    data_type = "CHAR(100)"
                                if(type(obj_detail) == type(True)):
                                   data_type = "INT"
                                   if obj_detail == True:
                                       obj_detail = 1
                                   else:
                                       obj_detail = 0          
                                #-----------------------------
                                #先确认有无启用 
                                #print(obj_detection)
                                try:
                                    if obj_detection["enable"]==True:
                                        str_region_table += "," + region_prefix + detection_index + "_" + item_detail + "  " + data_type
                                        str_region_header +=","+region_prefix +detection_index + "_"+item_detail
                                        str_value = """'{value}'""".format(value=obj_detail)
                                        str_region_insert += "," + str_value                                                                                                                         
                                    else:
                                        break
                                except Exception as e:
                                    continue
                           
                        #------------------------------
                         #统计区域内的信息，用于dailyreport  
                    if detection_index=="region_info_areashift":
                          AreaShift_errorcode.append(obj_detection["error_code"])
                    if detection_index=="region_info_hole":
                          Hole_errorcode.append(obj_detection["error_code"])
                    if detection_index=="region_info_shift":
                          Shift_errorcode.append(obj_detection["error_code"])
                    if detection_index=="region_info_area":
                          Area_errorcode.append(obj_detection["error_code"])
                    if detection_index=="region_info_width":
                          Width_errorcode.append(obj_detection["error_code"])
                                                

       #---------------------------------------------------------------------------
       #统计当前产品缺陷信息,置状态位
        # 判断Coverage-shift
        zerolistareashift = list(filter(lambda x: x != 0, AreaShift_errorcode))
        #print(zerolistareashift)
        if len(zerolistareashift) != 0:
            Coverage_Shift = 0
        else:
            Coverage_Shift = 1

        output_err = "@{}".format(Coverage_Shift)
        start_index = 0
        for err in AreaShift_errorcode:
            start_index = start_index + 1
            if err != 0:
                output_err = "{}@region{}".format(output_err,start_index)
        self.mes_dict["glue_coverage_shift"] = output_err

        # 判断Coverage-Glue hole
        zerolisthole = list(filter(lambda x: x != 0, Hole_errorcode))
        #print(zerolisthole)
        if len(zerolisthole) != 0:
            Coverage_Hole = 0
        else:
            Coverage_Hole = 1

        output_err = "@{}".format(Coverage_Hole)
        start_index = 1
        for err in Hole_errorcode:
            start_index = start_index + 1
            if err != 0:
                output_err = "{}@region{}".format(output_err,start_index)
        self.mes_dict["glue_coverage_glue_hole"] = output_err
       
        #记录断胶，严重面积，严重宽度
        listErrorCodeMiss=[]
        listErrorCodeMissRegion=[]
       #解析arealist，判断errorcode
       # Glue Area
        Missing_Area=1
        Dimension_Area=1
        if sum(Area_errorcode)==0:
                Missing_Area=1
                Dimension_Area=1
        else:
             if Area_errorcode.count(1)>0:
                    Missing_Area=0
             if Area_errorcode.count(2)>0:
                    Dimension_Area=0

        output_err1 = "@{}".format(Missing_Area)
        output_err2 = "@{}".format(Dimension_Area)
        start_index = 0
        for err in Area_errorcode:
            start_index = start_index + 1
            if err == 1:
                listErrorCodeMiss.append(1)
                output_err1 = "{}@region{}".format(output_err1,start_index)
            if err == 2:
                output_err2 = "{}@region{}".format(output_err2,start_index)
        #self.mes_dict["missing_area"] = output_err1
        self.mes_dict["glue_dimension_glue_area"] = output_err2

       #解析Widthlist，判断errorcode
       # Glue Width
        Missing_Width=1
        Dimension_Width=1
        if sum(Width_errorcode)==0:
                Missing_Width=1
                Dimension_Width=1
        else:
             if Width_errorcode.count(1)>0:
                    Missing_Width=0
             if Width_errorcode.count(2)>0:
                    Dimension_Width=0

        output_err1 = "@{}".format(Missing_Width)
        output_err2 = "@{}".format(Dimension_Width)
        start_index = 0
        for err in Width_errorcode:
            start_index = start_index + 1
            if err == 1:
                listErrorCodeMiss.append(1)
                output_err1 = "{}@region{}".format(output_err1,start_index)
            if err == 2:
                output_err2 = "{}@region{}".format(output_err2,start_index)
        #self.mes_dict["missing_width"] = output_err1
        self.mes_dict["glue_dimension_glue_width"] = output_err2
        
        #判断brokeb/miss
        if len(listErrorCodeMiss)>0 or obj["detection_gap_info"]["num"]>0:
            Missing_Broken=0
        else:
            Missing_Broken=1
        output_err = "@{}".format(Missing_Broken)
        #区域信息写入
        #宽度区域
        start_index=0 
        for err in Width_errorcode:
            start_index = start_index + 1
            if err == 1:
                listErrorCodeMissRegion.append(start_index)
        #面积区域
        start_index=0 
        for err in Area_errorcode:
            start_index = start_index + 1
            if err == 1 and listErrorCodeMissRegion.count(start_index)==0:
                listErrorCodeMissRegion.append(start_index)
        #区域带入
        if len(listErrorCodeMissRegion)>0:
            listErrorCodeMissRegion.sort()
        if len(listErrorCodeMissRegion)==0 and output_err==0:
            listErrorCodeMissRegio.append(1)
        if Missing_Broken==0:
            for err_index in listErrorCodeMissRegion:
                listErrorCodeMiss.append(1)
                output_err = "{}@region{}".format(output_err,err_index)
        self.mes_dict["glue_coverage_glue_Path_broken/missing"] = output_err 
        
        # 判断Dimension-shift
        zerolistShift = list(filter(lambda x: x != 0, Shift_errorcode))
        #print(zerolistShift)
        if len(zerolistShift) != 0:
            Dimension_Shift = 0
        else:
            Dimension_Shift = 1

        output_err = "@{}".format(Dimension_Shift)
        start_index = 0
        for err in Shift_errorcode:
            start_index = start_index + 1
            if err != 0:
                output_err = "{}@region{}".format(output_err,start_index)
        self.mes_dict["glue_dimension_shift"] = output_err
        
        #溢胶
        if obj["detection_overflow_info"]["num"]>0:
            output_err = "@{}@regionN".format(0)
        else:
            output_err = "@{}".format(1)
        self.mes_dict["overflow/splatter"] = output_err 
        
        # 判断Dimension-shift
        zerolistShift = list(filter(lambda x: x != 0, Shift_errorcode))
        #print(zerolistShift)
        if len(zerolistShift) != 0:
            Dimension_Shift = 0
        else:
            Dimension_Shift = 1

        output_err = "@{}".format(Dimension_Shift)
        start_index = 0
        for err in Shift_errorcode:
            start_index = start_index + 1
            if err != 0:
                output_err = "{}@region{}".format(output_err,start_index)
        self.mes_dict["glue_dimension_shift"] = output_err
                   
        #----------------------------------------------------------------------------------
        #解析glue_length_info
        obj_gluelength_info=obj["glue_length_info"]
        gluepath_prefix="gluelength"
        for gluepath_index, gluepath_single in obj_gluelength_info.items():
            #print(gluepath_index,gluepath_single)
            for item_detail in gluepath_single:
                gluepath_detail = gluepath_single[item_detail]
                if (type(gluepath_detail) != type(json.loads("""{}"""))):
                                data_type = "REAL" # 默认是浮点
                                if(type(gluepath_detail) == type("")):
                                    data_type = "CHAR(100)"
                                if(type(gluepath_detail) == type(True)):
                                   data_type = "INT"
                                   if gluepath_detail == True:
                                       gluepath_detail = 1
                                   else:
                                       gluepath_detail = 0          
                   
                str_region_table += "," + gluepath_prefix + gluepath_index + "_" + item_detail + "  " + data_type
                str_region_header +=","+gluepath_prefix +gluepath_index + "_"+item_detail
                str_value = """{value}""".format(value=gluepath_detail)
                str_region_insert += "," + str_value   
          
        #-----------------------------------------------------------------------------------------------       
        #解析gap_info
        strgapName="num contour"
        obj_gap_info =obj["detection_gap_info"]

        #预留10位gap有效信息
        numlimit=10
        gapinfo_prefix="gluegap"      
        obj_num=obj_gap_info["num"]  
        if obj_num!=0:
            Coverage_gluePath=0
        else:            
            Coverage_gluePath=1  
        
        #多余的预留位用0补齐
        if obj_num<numlimit or obj_num==0:
           for i in range(obj_num,numlimit):
               datatype="REAL"
               str_region_table += "," + gapinfo_prefix + str(i) + "_" + "info" + "_width" + "  " + data_type
               str_region_header += ","+ gapinfo_prefix + str(i) + "_" + "info" + "_width"
               str_value = """{value}""".format(value=0.0)
               str_region_insert += "," + str_value             
         
        #--------------------------------------------------------------------- 
        #解析overflow info  
        obj_overflow_info =obj["detection_overflow_info"]
        obj_overflow_num=obj_overflow_info["num"]
        
        if obj_overflow_num!=0:
            Overflowsplatter=0
        else:
            Overflowsplatter=1          
             
        #-------------------------------------------------------------------
        #添加Detail Item，用于统计信息
        str_region_table += "," +"Coverage_Shift INT"
        str_region_header += "," +"Coverage_Shift"
        str_value = """{value}""".format(value=Coverage_Shift)
        str_region_insert += "," + str_value  


        str_region_table += "," +"Coverage_Hole INT"
        str_region_header += "," +"Coverage_Hole"
        str_value = """{value}""".format(value=Coverage_Hole)
        str_region_insert += "," + str_value     
              
        
        str_region_table += "," +"Coverage_Gluepath INT"
        str_region_header += "," +"Coverage_Gluepath"
        str_value = """{value}""".format(value=Coverage_gluePath)
        str_region_insert += "," + str_value          
        
        str_region_table += "," +"Missing_Glue_Area INT"
        str_region_header += "," +"Missing_Glue_Area"
        str_value = """{value}""".format(value=Missing_Area)
        str_region_insert += "," + str_value          
        
        str_region_table += "," +"Missing_Glue_Width INT"
        str_region_header += "," +"Missing_Glue_Width"
        str_value = """{value}""".format(value=Missing_Width)
        str_region_insert += "," + str_value  
        
        
        str_region_table += "," +"Overflow_or_Splatter INT"
        str_region_header += "," +"Overflow_or_Splatter"
        str_value = """{value}""".format(value=Overflowsplatter)
        str_region_insert += "," + str_value              
        
        str_region_table += "," +"Dimension_Glue_Area INT"
        str_region_header += "," +"Dimension_Glue_Area"
        str_value = """{value}""".format(value=Dimension_Area)
        str_region_insert += "," + str_value          
        
        str_region_table += "," +"Dimension_Glue_Width INT"
        str_region_header += "," +"Dimension_Glue_Width"
        str_value = """{value}""".format(value=Dimension_Width)
        str_region_insert += "," + str_value       
        
        str_region_table += "," +"Dimension_Shift INT"
        str_region_header += "," +"Dimension_Shift"        
        str_value = """{value}""".format(value=Dimension_Shift)
        str_region_insert += "," + str_value             
        
        
        #-----------------------------------------------------------------------------------------------------
        # 增加图片路径存储
        str_region_table += "," + "capture_image  CHAR(255)"
        str_region_header += "," + "capture_image"
        str_region_table += "," + "source_image  CHAR(255)"
        str_region_header += "," + "source_image"

        str_region_insert += "," + """'{img_cap}'""".format(img_cap = str_pic_cap)
        str_region_insert += "," + """'{img_src}'""".format(img_src = str_pic_raw)
        
        #-------------------------------------------------------------------------------------------------------
        #加入MesConnection状态位
        str_region_table +=","+"MesConnection  INT"
        str_region_header +=","+"MesConnection"
        str_region_insert += "," + """'{MesConnection}'""".format(MesConnection = n_mes)                      
        
        
        #创表语句结尾                             
        str_region_table +=")"
        str_region_insert +=")"
        #print(str_region_insert)
        
        #print(str_region_header+"\n")
        splitresult=str_region_header.split(",")
        #print(splitresult)
        #print("\n")

        try:
           # 查询表是否存在 -- 区域信息
           cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name=?",(self.detail_table_name,))
           result = cursor.fetchone()
           if result == None:
              cursor.execute(str_region_table)

           #插入数据
           #判断插入数据的创表字符串和原有数据库是否一致
           cursor.execute("SELECT * FROM {}".format(self.detail_table_name))
           result=cursor.fetchone()
           str_in = [i[0]for i in cursor.description]
           if splitresult==str_in:
               cursor.execute(str_region_insert)
               conn.commit()
               return "OK"
           else:
               conn.commit()
               return "数据表结构异常"          
        except Exception as e:
           print(str(e))
           return e
        finally:
           cursor.close()
           conn.close()

    #--------------------------------------------------------------------------
    #生成产品的详细表格，用于追溯产品信息,方便导出历史db数据导出
    def generate_csv(self,str_file_path,str_today,str_database_filename):
        # 获取以日期命名的数据库
        #strCurDate = datetime.datetime.now().strftime('%Y%m%d')
        str_file_path_new = str_file_path + "\\" + str_today
        str_path=str_file_path_new + "\\" + str_database_filename + ".db"
        if not os.path.exists(str_path):
            raise ValueError("数据库不存在")
                 

        # 创建以日期命名的.csvfile
        str_csv_file=str_file_path_new+"\\" + str_database_filename + "-{}.csv".format(self.pos_index)

        # 连接上.db数据库文件
        conn = sqlite3.connect(str_path)
        print(str_path)
        # 创建游标
        cursor = conn.cursor()

        #判断是否存在region_info这张表
        cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name=?", (self.detail_table_name,))
        print(self.detail_table_name)
        result = cursor.fetchone()
        
        #如果region_info表格不存在的话，工具报警
        if result == None:
            raise ValueError("数据库中{}不存在".format(self.detail_table_name))
        
        #如果region_info表格存在的话，则执行数据查询
        # 获取表的全部内容
        cursor.execute("SELECT * FROM {}".format(self.detail_table_name))
        results=cursor.fetchall()
        #print(results)

        #创建csv文件流，逐行写value，将数据导出
        with open(str_csv_file,'w', newline='') as csvfile:
            writer=csv.writer(csvfile)
            writer.writerow([i[0]for i in cursor.description])
            #print([i[0]for i in cursor.description])
            writer.writerows(results)

        # csv写完后，关闭游标，断开与数据库的连接
        cursor.close()
        conn.close()

        
        #生产数据信息收集
    def data_analysis(self,str_file_path,str_today,str_database_filename):
        # 创建一个以日期命名的csv文件，用于汇总信息
        #strCurDate = datetime.datetime.now().strftime('%Y%m%d')
        str_file_path_new=str_file_path + "\\" + str_today
        if not os.path.exists(str_file_path_new + "\\" + str_database_filename + ".db"):
            raise ValueError("数据库不存在")
            
        str_file_csv=str_file_path_new + "\\" +"DailyReport_"+str_database_filename +"-{}.csv".format(self.pos_index)
                
        # 连接上.db数据库文件
        conn = sqlite3.connect(str_path)
        # 创建游标
        cursor = conn.cursor()        
        #---------------------------------------------------------------------
        #查询整体生产线信息
        # 执行查询，获取生产过程的所有数
        cursor.execute("SELECT Count(*) FROM {}".format(self.detail_table_name))
        resulttotal = cursor.fetchall()
        #print(resulttotal[0][0])

        # 执行查询，获取GrossFail项的条目数 
        cursor.execute("SELECT Count(*) FROM {} WHERE ERRORCODE ==1".format(self.detail_table_name))
        resultGF = cursor.fetchall()
        #print(resultGF[0][0])
        
        # 执行查询，获取DimensionFail项的条目数
        cursor.execute("SELECT Count(*) FROM {} WHERE ERRORCODE ==2".format(self.detail_table_name))
        resultDF = cursor.fetchall()
        #print(resultDF[0][0])      
        

       #---------------------------------------------------------------------
       #查询GrossFail的信息           
        # 执行查询，获取Coverageshift项的条目数
        cursor.execute("SELECT Count(*) FROM {} WHERE Coverage_Shift==0".format(self.detail_table_name))

        resultCS = cursor.fetchall()
        #print(resultCS[0][0])
        # 执行查询，获取Coveragegluehole项的条目数 
        cursor.execute("SELECT Count(*) FROM {} WHERE Coverage_Hole==0".format(self.detail_table_name))

        resultCH = cursor.fetchall()
        #print(resultCH[0][0])
        # 执行查询，获取Coveragegluepath项的条目数 
        cursor.execute("SELECT Count(*) FROM {} WHERE Coverage_Gluepath==0".format(self.detail_table_name))

        resultCGP = cursor.fetchall()
        #print(resultCGP[0][0])
        # 执行查询，获取missingArea项的条目数 
        cursor.execute("SELECT Count(*) FROM {} WHERE Missing_Glue_Area==0".format(self.detail_table_name))

        resultMA = cursor.fetchall()
        #print(resultMA[0][0])     
        # 执行查询，获取missingwidth项的条目数 
        cursor.execute("SELECT Count(*) FROM {} WHERE Missing_Glue_Width==0".format(self.detail_table_name))
        resultMW = cursor.fetchall()
        #print(resultMW[0][0]) 
        
        #---------------------------------------------------------------------
        #统计Dimension Fail条目数       
        # 执行查询，获取Overflow项的条目数 
        cursor.execute("SELECT Count(*) FROM {} WHERE Overflow_or_Splatter==0".format(self.detail_table_name))

        resultOV = cursor.fetchall()
        #print(resultOV[0][0])
        # 执行查询，获取glueArea项的条目数
        cursor.execute("SELECT Count(*) FROM {} WHERE Dimension_Glue_area==0".format(self.detail_table_name))
        resultDA = cursor.fetchall()
        #print(resultDA[0][0])        
        
        # 执行查询，获取gluewidth项的条目数
        cursor.execute("SELECT Count(*) FROM {} WHERE Dimension_Glue_width==0".format(self.detail_table_name))
        resultDW = cursor.fetchall()
        #print(resultDW[0][0])        
        
        
        # 执行查询，获取Shift项的条目数   
        cursor.execute("SELECT Count(*) FROM {} WHERE Dimension_shift==0".format(self.detail_table_name))
        resultDS = cursor.fetchall()
        #print(resultDS[0][0])  
      
        cursor.close()
        conn.close() 
        #--------------------------------------------------------------------                    
        #生产数据进行计算
        
        Grossfailrate=resultGF[0][0]/resulttotal[0][0]
        Dimensionfailrate=resultDF[0][0]/resulttotal[0][0]
        DetailrateCS=resultCS[0][0]/resulttotal[0][0]
        DetailrateCH=resultCH[0][0]/resulttotal[0][0]
        DetailrateCGP=resultCGP[0][0]/resulttotal[0][0]
        DetailrateMA = resultMA[0][0] / resulttotal[0][0]
        DetailrateMW = resultMW[0][0] / resulttotal[0][0]
        DetailrateOV=resultOV[0][0]/resulttotal[0][0]
        DetailrateDA=resultDA[0][0]/resulttotal[0][0]
        DetailrateDW=resultDW[0][0]/resulttotal[0][0]
        DetailrateDS=resultDS[0][0]/resulttotal[0][0]
        
       #----------------------------------------------------------------------
       #将数值写入Daily Report中
       #创建表头
       
        Header=["Summary","Total","GeneralFailRate","Detail Item","NG Number","Detail_FailRate"]
       #存入数据
        Data=[
       ["AOI True fail(Gross fail)",resulttotal[0][0],Grossfailrate,"Glue Coverage-Shift",resultCS[0][0], DetailrateCS],
       ["AOI True fail(Gross fail)",resulttotal[0][0],Grossfailrate,"Glue Coverage-Glue Hole",resultCH[0][0], DetailrateCH],
       ["AOI True fail(Gross fail)",resulttotal[0][0],Grossfailrate,"Glue Coverage-Glue path Broken",resultCGP[0][0], DetailrateCGP],
       ["AOI True fail(Gross fail)",resulttotal[0][0],Grossfailrate,"Glue Missing Area",resultMA[0][0], DetailrateMA],
       ["AOI True fail(Gross fail)", resulttotal[0][0], Grossfailrate, "Glue Missing Width", resultMW[0][0],DetailrateMW],
       ["AOI Data Collection FR(Dimension)",resulttotal[0][0],Dimensionfailrate,"Overflow/Splatter",resultOV[0][0],DetailrateOV],
       ["AOI Data Collection FR(Dimension)",resulttotal[0][0],Dimensionfailrate,"Glue dimension -glue area",resultDA[0][0],DetailrateDA],
       ["AOI Data Collection FR(Dimension)",resulttotal[0][0],Dimensionfailrate,"Glue dimension -glue width",resultDW[0][0],DetailrateDW],
       ["AOI Data Collection FR(Dimension)",resulttotal[0][0],Dimensionfailrate,"Glue dimension -shift",resultDS[0][0],DetailrateDS]
       ]
       
        with open(str_file_csv,'w', newline='') as csvfile:
            writer=csv.writer(csvfile)
            writer.writerow(Header)
            writer.writerows(Data)

class result_operator():

    # Đối tượng thao tác kết quả kiểm tra tổng thể
    obj_total = json.loads("""{}""")  

    # Dùng để thay thế dữ liệu kiểm tra
    # list_data: dữ liệu dùng để thay thế, kiểu list
    # list_region: vùng cần thay thế, kiểu list
    # types: kiểu dữ liệu cần thay thế, kiểu int
    #    2 biểu thị lệch keo
    #    3 biểu thị lỗ hổng
    #    4 biểu thị diện tích
    #    5 biểu thị tỷ lệ keo
    #    6 biểu thị dịch chuyển X
    #    7 biểu thị dịch chuyển Y

    def data_replace(self,str_info,list_data,list_region,types=1,b_show_lackglue=True):
        #校检数据长度和区域长度是否一致
        #obj = json.loads(str_info)
        obj=str_info
        num1=len(list_data)
        num2=len(list_region)
        if num1!=num2:
            error_output = "list_data lens different,list_data is {},list_region is {}".format(len(list_data),len(list_region))  
            raise ValueError(error_output)
        #胶宽替换 
        if types==1:
            for i in range(0,num1):
                index = "region_{index}".format(index = list_region[i])
                obj["region_info"][index]["region_info_width"]["min_val"]=list_data[i]
                if list_data[i]>=obj["region_info"][index]["region_info_width"]["lower_spec"] and list_data[i]<=obj["region_info"][index]["region_info_width"]["upper_spec"]:
                    obj["region_info"][index]["region_info_width"]["error_code"]=0
                else:
                    obj["region_info"][index]["region_info_width"]["error_code"]=2
                #遍历error_code重新判断替换
                obj["region_info"][index]["info_base"]["error_code"]=check_region_errorcode(obj,index)
        #胶偏替代
        if types==2:
            for i in range(0,num1):
                index = "region_{index}".format(index = list_region[i])
                obj["region_info"][index]["region_info_shift"]["current_val"]=list_data[i]
                if list_data[i]>=obj["region_info"][index]["region_info_shift"]["lower_spec"] and list_data[i]<=obj["region_info"][index]["region_info_shift"]["upper_spec"]:
                    obj["region_info"][index]["region_info_shift"]["error_code"]=0
                else:
                    obj["region_info"][index]["region_info_shift"]["error_code"]=2
                #遍历error_code重新判断替换
                obj["region_info"][index]["info_base"]["error_code"]=check_region_errorcode(obj,index)
        
        #胶偏X替代
        try:
            if types==6:
                for i in range(0,num1):
                    index = "region_{index}".format(index = list_region[i])
                    obj["region_info"][index]["region_info_shiftX"]["current_val"]=list_data[i]
                    if list_data[i]>=obj["region_info"][index]["region_info_shiftX"]["lower_spec"] and list_data[i]<=obj["region_info"][index]["region_info_shiftX"]["upper_spec"]:
                        obj["region_info"][index]["region_info_shiftX"]["error_code"]=0
                    else:
                        obj["region_info"][index]["region_info_shiftX"]["error_code"]=2
                    #遍历error_code重新判断替换
                    obj["region_info"][index]["info_base"]["error_code"]=check_region_errorcode(obj,index)
        except:
            tempi=0#
        
        #胶偏Y替代
        try:
            if types==7:
                for i in range(0,num1):
                    index = "region_{index}".format(index = list_region[i])
                    obj["region_info"][index]["region_info_shiftY"]["current_val"]=list_data[i]
                    if list_data[i]>=obj["region_info"][index]["region_info_shiftY"]["lower_spec"] and list_data[i]<=obj["region_info"][index]["region_info_shiftY"]["upper_spec"]:
                        obj["region_info"][index]["region_info_shiftY"]["error_code"]=0
                    else:
                        obj["region_info"][index]["region_info_shiftY"]["error_code"]=2
                    #遍历error_code重新判断替换
                    obj["region_info"][index]["info_base"]["error_code"]=check_region_errorcode(obj,index)
        except:
            tempi=0#
        
        #孔洞替代,孔洞为Gross Fail项，NG直接为1
        if types==3:
            for i in range(0,num1):
                index = "region_{index}".format(index = list_region[i])
                obj["region_info"][index]["region_info_hole"]["current_val"]=list_data[i]
                if list_data[i]>=obj["region_info"][index]["region_info_hole"]["lower_spec"] and list_data[i]<=obj["region_info"][index]["region_info_hole"]["upper_spec"]:
                    obj["region_info"][index]["region_info_hole"]["error_code"]=0
                else:
                    obj["region_info"][index]["region_info_hole"]["error_code"]=1
                #遍历error_code重新判断替换
                obj["region_info"][index]["info_base"]["error_code"]=check_region_errorcode(obj,index)
        
        #面积替代
        if types==4:
            for i in range(0,num1):
                index = "region_{index}".format(index = list_region[i])
                obj["region_info"][index]["region_info_area"]["current_val"]=list_data[i]
                if list_data[i]>=obj["region_info"][index]["region_info_area"]["lower_spec"] and list_data[i]<=obj["region_info"][index]["region_info_area"]["upper_spec"]:
                    obj["region_info"][index]["region_info_area"]["error_code"]=0
                else:
                    obj["region_info"][index]["region_info_area"]["error_code"]=2
                #遍历error_code重新判断替换
                obj["region_info"][index]["info_base"]["error_code"]=check_region_errorcode(obj,index)
        
        #占比替代,占比为Gross Fail项，NG直接为1
        if types==5:
            for i in range(0,num1):
                index = "region_{index}".format(index = list_region[i])
                obj["region_info"][index]["region_info_areashift"]["current_val"]=list_data[i]
                if list_data[i]>=obj["region_info"][index]["region_info_areashift"]["lower_spec"] and list_data[i]<=obj["region_info"][index]["region_info_areashift"]["upper_spec"]:
                    obj["region_info"][index]["region_info_areashift"]["error_code"]=0
                else:
                    obj["region_info"][index]["region_info_areashift"]["error_code"]=1
                #遍历error_code重新判断替换
                obj["region_info"][index]["info_base"]["error_code"]=check_region_errorcode(obj,index)
        
        #重新判断整体errorcode
        obj=check_errorcode(obj,b_show_lackglue)
        return obj
        #return json.dumps(obj)
        
    # 用于检测数据获取
    # str_info，胶检输出数据
    # list_region，用于取数据的区域，list型数据
    # types用于替换的数据类型，int型数据,1表示胶宽,2表示偏移,3表示孔洞 4表示面积 5表示胶占比 6表示偏移X  7表示偏移Y
    #返回值2个list类型，一个数据，一个errorcode；其中获取胶宽时会返回最大值最小值及平均值(数据按字符串打包)，获取位置时会返回检测值，检测最大值，检测最小值(数据按字符串打包)
    def data_obtain(self,str_info,list_region=None,types=1):
        #obj=json.loads(str_info)
        obj=str_info
        #检测区域处理
        if list_region==None:
            region_num = obj["base_info"]["region_number"]
            list_region=[]
            for i in range(region_num):
                list_region.append(i) 
        num1=len(list_region)
        return_data=[]
        return_errorcode=[]
        #宽度获取
        if types==1:
            for i in range(0,num1):
                index = "region_{index}".format(index = list_region[i])
                average_val=obj["region_info"][index]["region_info_width"]["average_val"]
                min_val=obj["region_info"][index]["region_info_width"]["min_val"]
                max_val=obj["region_info"][index]["region_info_width"]["max_val"]
                str_return_data="{:.4f}({:.4f},{:.4f})".format(average_val,min_val,max_val)
                return_data.append(str_return_data)
                return_errorcode.append(obj["region_info"][index]["region_info_width"]["error_code"])
        
        #偏移获取
        if types==2:
            for i in range(0,num1):
                index = "region_{index}".format(index = list_region[i])
                average_val=obj["region_info"][index]["region_info_shift"]["average_val"]
                min_val=obj["region_info"][index]["region_info_shift"]["min_val"]
                max_val=obj["region_info"][index]["region_info_shift"]["max_val"]
                str_return_data="{:.4f}({:.4f},{:.4f})".format(average_val,min_val,max_val)
                return_data.append(str_return_data)
                return_errorcode.append(obj["region_info"][index]["region_info_shift"]["error_code"])
        
        #偏移获取X
        try:
            if types==6:
                for i in range(0,num1):
                    index = "region_{index}".format(index = list_region[i])
                    average_val=obj["region_info"][index]["region_info_shiftX"]["average_val"]
                    min_val=obj["region_info"][index]["region_info_shiftX"]["min_val"]
                    max_val=obj["region_info"][index]["region_info_shiftX"]["max_val"]
                    str_return_data="{:.4f}({:.4f},{:.4f})".format(average_val,min_val,max_val)
                    return_data.append(str_return_data)
                    return_errorcode.append(obj["region_info"][index]["region_info_shiftX"]["error_code"])
        except:
            tempi=0#
        
        #偏移获取Y
        try:
            if types==7:
                for i in range(0,num1):
                    index = "region_{index}".format(index = list_region[i])
                    average_val=obj["region_info"][index]["region_info_shiftY"]["average_val"]
                    min_val=obj["region_info"][index]["region_info_shiftY"]["min_val"]
                    max_val=obj["region_info"][index]["region_info_shiftY"]["max_val"]
                    str_return_data="{:.4f}({:.4f},{:.4f})".format(average_val,min_val,max_val)
                    return_data.append(str_return_data)
                    return_errorcode.append(obj["region_info"][index]["region_info_shiftY"]["error_code"])
        except:
            tempi=0#
        
        #孔洞获取
        if types==3:
            for i in range(0,num1):
                index = "region_{index}".format(index = list_region[i])
                current_val=obj["region_info"][index]["region_info_hole"]["current_val"]
                return_data.append(current_val)
                return_errorcode.append(obj["region_info"][index]["region_info_hole"]["error_code"])
        
        #面积获取
        if types==4:
            for i in range(0,num1):
                index = "region_{index}".format(index = list_region[i])
                current_val=obj["region_info"][index]["region_info_area"]["current_val"]
                return_data.append(current_val)
                return_errorcode.append(obj["region_info"][index]["region_info_area"]["error_code"])
        
        #占比获取
        if types==5:
            for i in range(0,num1):
                index = "region_{index}".format(index = list_region[i])
                current_val=obj["region_info"][index]["region_info_areashift"]["current_val"]
                return_data.append(current_val)
                return_errorcode.append(obj["region_info"][index]["region_info_areashift"]["error_code"])
        
        return return_data,return_errorcode

    # 合并两组相同长度的检测结果
    # 用于兼容一组无法完成全部检测内容的情况
    def merge(self,str_info1,str_info2,bOverflowColor=True,b_show_lackglue=True):
        #obj1 = json.loads(str_info1)
        #obj2 = json.loads(str_info2)
        obj1 = str_info1
        obj2 = str_info2
        obj_base1 = obj1["base_info"]
        obj_base2 = obj2["base_info"]
        
        obj_region1 = obj1["region_info"]
        obj_region2 = obj2["region_info"]
        
        # 校验SN是否相同
        sn_1 = obj_base1["SN"]
        sn_2 = obj_base2["SN"]
        if(sn_1 != sn_2):
            error_output = "SN different,region 1 is {},region 2 is {}".format(sn_1,sn_2)
            raise ValueError(error_output)

        # 校验区域长度是否相同
        num_1 = obj_base1["region_number"]
        num_2 = obj_base2["region_number"]
        #if(num_1 != num_2):
            #error_output = "region number different,region 1 is {},region 2 is {}".format(num_1,num_2)  
            #raise ValueError(error_output)
            
        # 开始合并
        # 轮廓使用region1的
        # 设置模式,如果发生冲突,默认优先使用object1的,除非特殊指定
        # 是否启用
        for key,item2 in obj_region2.items():
            item1 = obj_region1[key]
            
            # 合并宽度信息
            width_1 = item1["region_info_width"]
            width_2 = item2["region_info_width"]            
            # 如果两个都启用,存在歧义,报错       
            #if(width_2["enable"] == True and width_1["enable"] == True):
                #raise ValueError("merge width error: both enabled")       
            # 如果2启用,使用2替换1,1启用则无需进行动作       
            if(width_2["enable"] == True):
                obj_region1[key]["region_info_width"] = width_2
                
            # 合并shift信息
            shift_1 = item1["region_info_shift"]
            shift_2 = item2["region_info_shift"]       
            # 如果两个都启用,存在歧义,报错       
            #if(shift_1["enable"] == True and shift_2["enable"] == True):
                #raise ValueError("merge shift error: both enabled")       
            # 如果2启用,使用2替换1,1启用则无需进行动作       
            if(shift_2["enable"] == True):
                obj_region1[key]["region_info_shift"] = shift_2
            
            # 合并shiftX信息
            try:
                shift_1 = item1["region_info_shiftX"]
                shift_2 = item2["region_info_shiftX"]       
                # 如果两个都启用,存在歧义,报错       
                #if(shift_1["enable"] == True and shift_2["enable"] == True):
                    #raise ValueError("merge shift error: both enabled")       
                # 如果2启用,使用2替换1,1启用则无需进行动作       
                if(shift_2["enable"] == True):
                    obj_region1[key]["region_info_shiftX"] = shift_2
            except:
                tempi=0#
            
            # 合并shiftY信息
            try:
                shift_1 = item1["region_info_shiftY"]
                shift_2 = item2["region_info_shiftY"]       
                # 如果两个都启用,存在歧义,报错       
                #if(shift_1["enable"] == True and shift_2["enable"] == True):
                    #raise ValueError("merge shift error: both enabled")       
                # 如果2启用,使用2替换1,1启用则无需进行动作       
                if(shift_2["enable"] == True):
                    obj_region1[key]["region_info_shiftY"] = shift_2
            except:
                tempi=0#
            
            # 合并hole信息
            hole_1 = item1["region_info_hole"]
            hole_2 = item2["region_info_hole"]       
            # 如果两个都启用,存在歧义,报错       
            #if(hole_1["enable"] == True and hole_2["enable"] == True):
                #raise ValueError("merge hole error: both enabled")       
            # 如果2启用,使用2替换1,1启用则无需进行动作       
            if(hole_2["enable"] == True):
                obj_region1[key]["region_info_hole"] = hole_2 
            
            # 合并area信息
            area_1 = item1["region_info_area"]
            area_2 = item2["region_info_area"]       
            # 胶量不能报错,一定是两个都启用的
            # if(area_1["enable"] == True and area_2["enable"] == True):
                #raise ValueError("merge area error: both enabled")       
            # 如果2启用,使用2替换1,1启用则无需进行动作       
            if(area_2["enable"] == True):
                obj_region1[key]["region_info_area"] = area_2
            
            # 合并areashift信息
            coverage_1 = item1["region_info_areashift"]
            coverage_2 = item2["region_info_areashift"]
            # 如果两个都启用,存在歧义,报错       
            #if(coverage_1["enable"] == True and coverage_2["enable"] == True):
                #raise ValueError("merge coverage error: both enabled")       
            # 如果2启用,使用2替换1,1启用则无需进行动作       
            if(coverage_2["enable"] == True):
                obj_region1[key]["region_info_areashift"] = coverage_2
            
            #遍历error_code重新判断替换
            obj_region1[key]["info_base"]["error_code"]=check_region_errorcode(obj1,key)          
                        
        # 反向替换 
        obj1["base_info"] = obj_base1
        obj1["region_info"] = obj_region1
        obj1=check_errorcode(obj1,b_show_lackglue)
        
        
        return obj1
        #return json.dumps(obj1)

    # 合并在1后面追加结果
    # 用于兼容多个工具合并的情况
    def add(self,str_info1,str_info2,bOverflowColor=True,b_show_lackglue=True):
        #obj1 = json.loads(str_info1)
        #obj2 = json.loads(str_info2)
        obj1 = str_info1
        obj2 = str_info2
        obj_base1 = obj1["base_info"]
        obj_base2 = obj2["base_info"]
        
        obj_region1 = obj1["region_info"]
        obj_region2 = obj2["region_info"]
        
        # 校验SN是否相同
        sn_1 = obj_base1["SN"]
        sn_2 = obj_base2["SN"]
        if(sn_1 != sn_2):
            error_output = "SN different,region 1 is {},region 2 is {}".format(sn_1,sn_2)
            raise ValueError(error_output)

        # 追加区域数量
        num_1 = obj_base1["region_number"]
        num_2 = obj_base2["region_number"]
        obj_base1["region_number"] = num_1 + num_2
       
        # 开始合并
        i_region = 0
        for key,item2 in obj_region2.items():
            # 替换obj_2的索引
            i_region_new = num_1 + i_region
            str_index = "region_{}".format(i_region_new)

            # 替换region内容
            obj_region1[str_index] = item2
            obj_region1[str_index]["info_base"]["index"]=i_region_new
            i_region = i_region + 1

            #print(item2["region_info_areashift"])           
        
        #合并断胶信息
        try:
            gap_info1=obj1["detection_gap_info"]
            gap_info2=obj2["detection_gap_info"]
            num_1=gap_info1["num"]
            num_2=gap_info2["num"]
            i_region=0
            if gap_info2["num"]>0:
                for key,item2 in gap_info2.items():
                    if key=="num":
                        continue
                    i_region_new=num_1+i_region
                    str_index="{}".format(i_region_new)
                    gap_info1[str_index] = item2
                    i_region=i_region+1 
            gap_info1["num"]=num_1+num_2   
            obj1["detection_gap_info"]=gap_info1            
        except:
            tempi=0#
        
        #合并溢胶信息
        try:
            overflow_info1=obj1["detection_overflow_info"]
            overflow_info2=obj2["detection_overflow_info"]
            num_1=overflow_info1["num"]
            num_2=overflow_info2["num"]
            i_region=0
            if overflow_info2["num"]>0:
                for key,item2 in overflow_info2.items():
                    if key=="num":
                        continue
                    i_region_new=num_1+i_region
                    str_index="{}".format(i_region_new)
                    overflow_info1[str_index] = item2
                    i_region=i_region+1 
            overflow_info1["num"]=num_1+num_2   
            obj1["detection_overflow_info"]=overflow_info1 
        except:
            tempi=0#
        #合并多胶信息
        try:
            much_info1=obj1["detection_much_info"]
            much_info2=obj2["detection_much_info"]
            num_1=much_info1["num"]
            num_2=much_info2["num"]
            i_region=0
            if much_info2["num"]>0:
                for key,item2 in much_info2.items():
                    if key=="num":
                        continue
                    i_region_new=num_1+i_region
                    str_index="{}".format(i_region_new)
                    much_info1[str_index] = item2
                    i_region=i_region+1 
            much_info1["num"]=num_1+num_2   
            obj1["detection_much_info"]=much_info1 
        except:
            tempi=0#
        #合并少胶信息
        try:
            less_info1=obj1["detection_less_info"]
            less_info2=obj2["detection_less_info"]
            num_1=less_info1["num"]
            num_2=less_info2["num"]
            i_region=0
            if less_info2["num"]>0:
                for key,item2 in less_info2.items():
                    if key=="num":
                        continue
                    i_region_new=num_1+i_region
                    str_index="{}".format(i_region_new)
                    less_info1[str_index] = item2
                    i_region=i_region+1 
            less_info1["num"]=num_1+num_2   
            obj1["detection_less_info"]=less_info1 
        except:
            tempi=0#
        #合并胶长信息    
        try:
            lengh_info1=obj1["glue_length_info"]
            lengh_info2=obj2["glue_length_info"]
            i_region=0
            #判断1的胶长个数
            num_1=0
            for key in lengh_info1.keys():
                num_1=num_1+1
            for key,item2 in lengh_info2.items():
                if key=="num":
                    continue
                i_region_new=num_1+i_region
                str_index="{}".format(i_region_new)
                lengh_info1[str_index] = item2
                i_region=i_region+1   
            obj1["glue_length_info"]=lengh_info1 
        except:
            tempi=0#
        
        # 反向替换 
        obj1["base_info"] = obj_base1
        obj1["region_info"] = obj_region1
        obj1=check_errorcode(obj1,b_show_lackglue)
        return obj1
        #return json.dumps(obj1)

    def recalculate_result(self,str_info,thred_miss,thred_broken,thred_hole,thred_coverage,list_region=None):       
        # 解析info
        #obj = json.loads(str_info)
        obj=str_info
        obj_base = obj["base_info"]
        obj_region = obj["region_info"]
        
        if list_region!=None:
            list_region.sort()
            region_num = len(list_region)
        else:
            region_num = obj["base_info"]["region_number"]
            list_region=[]
            for i in range(region_num):
                list_region.append(i)
        # 整体错误码再计算
        error_code_total = obj_base["error_code"]

        # 再计算
        for i in range(0,len(list_region)):
            index="region_{}".format(list_region[i])
            item=obj_region[index]
            # 错误码
            error_code = item["info_base"]["error_code"]

            # 缺胶再计算-width
            obj_width = item["region_info_width"]
            if obj_width["min_val"] < obj_width["lower_spec"] and obj_width["enable"]==True:
                if obj_width["min_val"] < thred_miss * obj_width["lower_spec"]:
                    #obj_region_info_MSOP["glue_missing_width"] = 1
                    error_code = 1
                    obj["region_info"][index]["region_info_width"]["error_code"]=1
                    obj["region_info"][index]["info_base"]["error_code"]=1

            # 缺胶再计算-area
            obj_area = item["region_info_area"]
            if obj_area["current_val"] < obj_area["lower_spec"] and obj_area["enable"]==True:
                if obj_area["current_val"] < thred_miss * obj_area["lower_spec"]:
                    #obj_region_info_MSOP["glue_missing_area"] = 1
                    error_code = 1
                    obj["region_info"][index]["region_info_area"]["error_code"]=1
                    obj["region_info"][index]["info_base"]["error_code"]=1
            
            # glue coverage再计算
            obj_coverage = item["region_info_areashift"]
            if obj_coverage["current_val"] < thred_coverage and obj_coverage["enable"]==True:
                #obj_region_info_MSOP["glue_coverage_shift"] = 1
                error_code = 1
                obj["region_info"][index]["region_info_areashift"]["error_code"]=1
                obj["region_info"][index]["info_base"]["error_code"]=1

            # 孔洞再计算
            obj_hole = item["region_info_hole"]
            if obj_hole["current_val"] > thred_hole and obj_hole["enable"]==True:
                #obj_region_info_MSOP["glue_coverage_hole"] = 1
                error_code = 1
                obj["region_info"][index]["region_info_hole"]["error_code"]=1
                obj["region_info"][index]["info_base"]["error_code"]=1
            
            #断胶再计算
            num_brocken=obj["detection_gap_info"]["num"]
            if num_brocken>0:
                ###显示NG区域及长度
                for i in range(num_brocken): 
                    index="{}".format(i)
                    broken_length=obj["detection_gap_info"][index]["info"]["width"]
                    if broken_length>thred_broken:
                        error_code=1
                        break

            # 更新整体错误码
            if error_code == 1:
                error_code_total = 1
        # base info 再计算
        obj["base_info"]["error_code"] = error_code_total
        return obj

    #用于多级Spec的再判断，其中只进行COF至Gross判断，孔洞/胶占比/断胶本身为Gross项无需再进行再判断
    def recalculate_result_ex(self, str_info, thred_miss, list_region=None):
        # 解析info
        # obj = json.loads(str_info)
        obj = str_info
        obj_base = obj["base_info"]
        obj_region = obj["region_info"]

        if list_region != None:
            list_region.sort()
            region_num = len(list_region)
        else:
            region_num = obj["base_info"]["region_number"]
            list_region = []
            for i in range(region_num):
                list_region.append(i)
        # 整体错误码再计算
        error_code_total = obj_base["error_code"]

        # 再计算
        for i in range(0, len(list_region)):
            index = "region_{}".format(list_region[i])
            item = obj_region[index]
            # 错误码
            error_code = item["info_base"]["error_code"]

            # 缺胶再计算-width
            obj_width = item["region_info_width"]
            if obj_width["min_val"] < obj_width["lower_spec"] and obj_width["enable"] == True:
                if obj_width["min_val"] < thred_miss * obj_width["lower_spec"]:
                    # obj_region_info_MSOP["glue_missing_width"] = 1
                    error_code = 1
                    obj["region_info"][index]["region_info_width"]["error_code"] = 1
                    obj["region_info"][index]["info_base"]["error_code"] = 1

            # 缺胶再计算-area
            obj_area = item["region_info_area"]
            if obj_area["current_val"] < obj_area["lower_spec"] and obj_area["enable"] == True:
                if obj_area["current_val"] < thred_miss * obj_area["lower_spec"]:
                    # obj_region_info_MSOP["glue_missing_area"] = 1
                    error_code = 1
                    obj["region_info"][index]["region_info_area"]["error_code"] = 1
                    obj["region_info"][index]["info_base"]["error_code"] = 1

            # 更新整体错误码
            if error_code == 1:
                error_code_total = 1
        # base info 再计算
        obj["base_info"]["error_code"] = error_code_total
        return obj

class mes_upload():
    # Từ điển lưu thông tin lỗi
    __dict_info = {}

    # Tư thế chụp ảnh
    __pos_index = 1

    # Số chữ số sau dấu thập phân cho giá trị kết quả
    n_format_val = 2

    # Số chữ số sau dấu thập phân cho giới hạn trên/dưới
    n_format_spec = 2

    # Thiết lập số chữ số sau dấu thập phân cho giá trị kết quả
    def set_val_format(self,n_format):
        self.n_format_val = n_format

    # Thiết lập số chữ số sau dấu thập phân cho giới hạn trên/dưới
    def set_spec_format(self,n_format):
        self.n_format_spec = n_format

    # Lấy chuỗi tư thế hiện tại
    # get_mes_info: Thông tin lỗi (defect info)
    # pos: Tư thế của sản phẩm
    # upload_spec: Có tải lên thông số COF hay không, mặc định là false (không tải lên), true là tải lên
    def get_mes_info(self,dict_info,pos,upload_spec=False):
        self.__dict_info = dict_info
        self.__pos_index = pos

        region_num = dict_info["base_info"]["region_number"]
        # Xác định kết quả tổng hợp
        str_out = "1"
        for i_region in range(0,region_num):
            str_region = "region_{}".format(i_region)
            if self.__trans_error(dict_info["region_info"][str_region]["info_base"]["error_code"]) == 0:
                str_out = "0"
                break
        for i_region in range(0,region_num):
            str_out = str_out + self.__get_upload(i_region,False,upload_spec)

        return str_out

    # Lấy chuỗi tư thế hiện tại (kèm thông tin chiều dài keo và dịch chuyển X/Y)
    # get_mes_info_ex: thông tin lỗi
    # pos: tư thế sản phẩm
    # upload_spec: có tải lên giới hạn COF hay không, mặc định là false (không tải), true là tải lên
    def get_mes_info_ex(self,dict_info,pos,upload_spec=False):
        self.__dict_info = dict_info
        self.__pos_index = pos
        region_num = dict_info["base_info"]["region_number"]
        # Xác định kết quả tổng hợp
        str_out = "1"
        if self.__trans_error(dict_info["base_info"]["error_code"]) == 0:
            str_out = "0"

        for i_region in range(0,region_num):
            str_out = str_out + self.__get_upload(i_region,True,upload_spec)
        return str_out

    # Xử lý dữ liệu upload hiện tại, đáp ứng định dạng upload hiện tại - chủ yếu dùng cho trường hợp một tư thế của model 38
    # str_in: dữ liệu upload trả về từ kiểm tra keo
    # n_choose: chọn 1 hoặc 2, 1 là cho máy (科瑞恩); 2 là cho hệ thống khác (theo định dạng ICT quy định)
    # b_upload_mode: có bật chế độ upload hạ cấp không; True = hạ cấp (NG chuyển thành COF, COF chuyển thành OK, errorcode ép bằng 1), False = upload bình thường
    # list_ex_data: bắt buộc có khi chọn 1, dùng để bổ sung dữ liệu như đường dẫn ảnh chụp màn hình và tín hiệu có hồi keo lại hay không
    # b_open_recheck: có bật chức năng kiểm tra lại hay không; True = bật (upload kết quả kiểm tra thực tế), False = tắt (upload kết quả ép thành OK)
    def get_mes_data(self, str_in, b_upload_mode=False, n_choose=2, list_ex_data=[], b_open_recheck=True):
        if n_choose==1 and  len(list_ex_data)!=2:
            raise ValueError("请正确输入额外补充数据（截图路径与回流补胶信号）")
        if n_choose!=1 and n_choose!=2:
            raise ValueError("请正确输入机台类型，1科瑞恩，2其他")
        error_code= self.__dict_info["base_info"]["error_code"]
        str_Res_Mes="OK"
        if error_code == 0:
            str_Res_Mes = "OK"
        elif error_code == 1:
            str_Res_Mes = "FAIL"
            if b_upload_mode == True:
                str_Res_Mes = "COF"
        elif error_code == 2:
            str_Res_Mes = "COF"
            if b_upload_mode == True:
                str_Res_Mes = "OK"
        #error_code返回
        if self.__dict_info["base_info"]["error_code"]!=1:
            error_code=1
        else:
            error_code=0
        #降级模式
        if b_upload_mode==True:
            error_code=1
        #屏蔽复检强制OK模式
        if b_open_recheck==False:
            error_code=1
            str_Res_Mes="OK"
            n_reflow=0
        #模式1
        if n_choose==1:
            if isinstance(list_ex_data[0], int)==True:
                str_capimg_path=list_ex_data[1]
                n_reflow=list_ex_data[0]
            else:
                str_capimg_path = list_ex_data[0]
                n_reflow = list_ex_data[1]
            str_out="{};{},;gross@{}@{}@@,{};{}".format(error_code,str_capimg_path,error_code,str_Res_Mes,str_in[2:],n_reflow)
        #模式2
        if n_choose==2:            
            str_out = "{},gross@{}@{}@@,{}".format(error_code,error_code, str_Res_Mes,str_in[2:])

        return str_out

    # Xử lý dữ liệu upload hiện tại, đáp ứng định dạng upload hiện tại - chủ yếu dùng cho model 39 với nhiều tư thế (multi-pose) upload tổng hợp
    # list_str_in: danh sách dữ liệu upload trả về từ kiểm tra keo, sắp xếp theo thứ tự các tư thế
    # list_no_glue_state: danh sách trạng thái có keo/không keo tương ứng với mỗi tư thế, cũng theo thứ tự
    # n_choose: chọn 1 hoặc 2, 1 là cho máy (科瑞恩); 2 là cho hệ thống khác (theo định dạng ICT quy định)
    # b_upload_mode: có bật chế độ upload hạ cấp không; True = hạ cấp (NG chuyển thành COF, COF chuyển thành OK, errorcode ép bằng 1), False = upload bình thường
    # list_ex_data: danh sách, không được để trống; nếu chọn 1 thì cần điền đường dẫn ảnh chụp và tín hiệu có hồi keo; nếu chọn 2 thì cần điền vị trí file log kiểm tra lại và vị trí ảnh nén
    # list_ex_up_load_imgs_pama: danh sách, không được để trống; điền dữ liệu ảnh nén kiểm tra gửi lên MES và thông tin SPEC. Định dạng: trước là số lượng ảnh thực tế, sau là SPEC tương ứng với số lượng đó
    # b_open_recheck: có bật chức năng kiểm tra lại hay không; True = bật (upload kết quả thực tế), False = tắt (ép kết quả upload thành OK)
    def get_mes_data_Ex(self,list_str_in,list_no_glue_state,n_choose=2,list_ex_data=[],list_ex_up_load_imgs_pama=[],b_upload_mode=True,b_open_recheck=True):
        if len(list_str_in) == 0:
            raise ValueError("请正确输入胶检数据")
        if len(list_no_glue_state) == 0 :
            raise ValueError("请正确输入有无胶结果")
        if len(list_str_in) != len(list_no_glue_state) :
            raise ValueError("请正确输入有无胶结果个数,个数与胶检个数不匹配")
        if len(list_ex_data) != 2:
            raise ValueError("请正确输入额外补充数据（选择1-科瑞恩时要填入截图路径和是否回流补胶信号；选择2-博众时要填入复检数据LOG文档所在位置及图片压缩位置）")
        if len(list_ex_up_load_imgs_pama) != 2:
            raise ValueError("请正确输入额外补充数据（填入Mes压缩检测的图片数据及SPEC）")
        if n_choose != 1 and n_choose != 2:
            raise ValueError("请正确输入机台类型，1科瑞恩，2博众")
        #error_code及str_Res_mes初始化
        error_code=1
        str_Res_mes="OK"
        str_res="OK"
        #errcode及str_Res_mes逻辑判断
        if sum(list_no_glue_state)<len(list_no_glue_state):#存在有姿态无胶的情况
            error_code = 0
            str_Res_mes = "FAIL"
            str_res="NG"
        else:#姿态都有胶水
            # 遍历所有所有胶检数据
            for data in list_str_in:
                # 如果有NG，默认不降级上传,即采用逻辑：胶水检测OK发“OK”，NG发“FAIL”
                if data[0:1]== "0":
                    error_code = 0
                    str_Res_mes = "FAIL"
                    str_res = "NG"
                    # 降级上传,即采用逻辑：胶水检测OK发“OK”，NG发“COF”，无胶发“FAIL”
                    if b_upload_mode == True:
                        error_code = 1
                        str_Res_mes = "COF"
                        str_res = "OK"
                    break
        # 屏蔽复检强制OK模式
        if b_open_recheck == False:
            error_code = 1
            str_Res_mes = "OK"
            n_reflow = 0
        #判断图片上传数量
        str_up_load_imgs_state="OK"
        if list_ex_up_load_imgs_pama[0]<list_ex_up_load_imgs_pama[1]:
            str_up_load_imgs_state="NG"
        # 和并所有胶检数据
        str_all_AOI_data = ""
        for data in list_str_in:
            str_all_AOI_data = str_all_AOI_data + data[2:] + ","
        # 模式1
        if n_choose == 1:
            if isinstance(list_ex_data[0], int) == True:
                str_capimg_path = list_ex_data[1]
                n_reflow = list_ex_data[0]
            else:
                str_capimg_path = list_ex_data[0]
                n_reflow = list_ex_data[1]
            #数据格式：1;,E:\GVIMAGES\2024-12-04\ON\OK\TEST081821\BI060-01-S1-TEST081821-20241204081818-recheck2-src-OK.jpg;gross@1@OK@@,异性胶检测数据,;0;OK,3
            str_out = "{};,{};gross@{}@{}@@,{};{};{},{}".format(error_code, str_capimg_path, error_code, str_Res_mes,str_all_AOI_data, n_reflow,str_up_load_imgs_state,list_ex_up_load_imgs_pama[0])
        # 模式2
        if n_choose == 2:
            str_all_AOI_data=str_all_AOI_data.replace(",","?")
            # 数据格式：R,NG,E:\GVIMAGES\GluepathCommunication,gross@0@FAIL@@?所有单项结果?,E:\IMG\2024-11-12\TEST20241112142639.zip,OK@8@8
            str_out = "R,{},{},gross@{}@{}@@?{},{},{}@{}@{}".format(str_res, list_ex_data[0], error_code,str_Res_mes, str_all_AOI_data,list_ex_data[1],str_up_load_imgs_state,list_ex_up_load_imgs_pama[0],list_ex_up_load_imgs_pama[1])

        return str_out

    # 系统内部errorcode定义: 0,pass 1,true fail 2,cof
    # 客户系统定义：1,pass 0,fail
    # 其中cof定义为成功
    def __trans_error(self,error_code):
        if error_code !=1:
            return 1
        else:
            return 0

    # pos: 姿态
    # index: 当前姿态的第几个区域
    # is_upload_ex: 是否上传额外信息(For 37, Length,ShiftX,ShiftY) 
    def __get_upload(self,region_index,is_upload_ex,upload_spec):

        # 返回值
        str_res = ""
        str_region = "region_{}".format(region_index)
        pos_index = self.__pos_index

        # 检测名称
        glue_coverage_shift = "glue_coverage_shift_p{}_r{}".format(pos_index,region_index+1)
        glue_coverage_glue_hole = "glue_coverage_hole_p{}_r{}".format(pos_index,region_index+1)
        glue_coverage_glue_path_broken = "glue_coverage_path_broken_p{}_r{}".format(pos_index,region_index+1)
        glue_coverage_glue_width_missing = "glue_coverage_width_missing_p{}_r{}".format(pos_index,region_index+1)
        glue_coverage_glue_area_missing = "glue_coverage_area_missing_p{}_r{}".format(pos_index,region_index+1)
        cof_overflow_splatter = "overflow/splatter_p{}_r{}".format(pos_index,region_index+1)
        cof_glue_dimension_glue_area = "glue_dimension_area_p{}_r{}".format(pos_index,region_index+1)
        cof_glue_dimension_glue_width = "glue_dimension_width_p{}_r{}".format(pos_index,region_index+1)
        cof_glue_dimension_shift = "glue_dimension_shift_p{}_r{}".format(pos_index,region_index+1)
        cof_glue_dimension_glue_length = "glue_dimension_length_p{}_r{}".format(pos_index,region_index+1)
        cof_glue_dimension_shiftX = "glue_dimension_shiftX_p{}_r{}".format(pos_index,region_index+1)
        cof_glue_dimension_shiftY = "glue_dimension_shiftY_p{}_r{}".format(pos_index,region_index+1)

        # 1 coverage_shift
        dict_coverage_shift = self.__dict_info["region_info"][str_region]["region_info_areashift"]
        glue_coverage_shift = glue_coverage_shift + "@{result}@{val}@{lsl}@{usl}".format(\
            result = self.__trans_error(dict_coverage_shift["error_code"]),\
            val = round(dict_coverage_shift["current_val"],self.n_format_val),\
            lsl = round(dict_coverage_shift["lower_spec"],self.n_format_spec),\
            usl = round(dict_coverage_shift["upper_spec"],self.n_format_spec))

        # 2 glue_hole
        dict_coverage_glue_hole = self.__dict_info["region_info"][str_region]["region_info_hole"]
        glue_coverage_glue_hole = glue_coverage_glue_hole + "@{result}@{val}@{lsl}@{usl}".format(\
            result = self.__trans_error(dict_coverage_glue_hole["error_code"]),\
            val = round(dict_coverage_glue_hole["current_val"],self.n_format_val),\
            lsl = round(dict_coverage_glue_hole["lower_spec"],self.n_format_spec),\
            usl = round(dict_coverage_glue_hole["upper_spec"],self.n_format_spec))

        # 3 width
        # glue_path_broken
        # glue_coverage_glue_width_missing
        # cof_glue_dimension_glue_width
        dict_width = self.__dict_info["region_info"][str_region]["region_info_width"]

        # glue path broken spec : 0.03 - 999
        broken_res = 1

        # 断胶不受宽度检测禁用启用的影响
        if self.__dict_info["region_info"][str_region]["info_base"]["type"]!="overflow":
            # 使用缺陷个数来判定,非width为0--斜向断胶存在宽度非0但存在断胶的情况
            if self.__dict_info["region_info"][str_region]["region_info_detection"]["width_off"] > 0:
                broken_res = 0
                
            glue_coverage_glue_path_broken = glue_coverage_glue_path_broken + "@{result}@{val}@{lsl}@{usl}".format(\
            result = broken_res,\
            val = 0,\
            lsl =0 ,\
            usl = round(0.03,self.n_format_spec))
        else:
            glue_coverage_glue_path_broken=""

        # 如果宽度检测未启用,均使用占位符号
        if dict_width["enable"] == 0:
            glue_coverage_glue_width_missing = glue_coverage_glue_width_missing + "@{result}@{val}@{lsl}@{usl}".format(\
            result = 0,\
            val = 0,\
            lsl = 0,\
            usl = 0)

            cof_glue_dimension_glue_width = cof_glue_dimension_glue_width + "@{result}@{val}@{lsl}@{usl}".format(\
            result = 0,\
            val = 0,\
            lsl = 0,\
            usl = 0)

        else:
            # 严重缺陷 spec为 0.5 USL
            width_missing_res = 1
            if dict_width["error_code"] == 1:
                width_missing_res = 0
            
            glue_coverage_glue_width_missing = glue_coverage_glue_width_missing + "@{result}@{val}@{lsl}@{usl}".format(\
            result = width_missing_res,\
            val = round(dict_width["min_val"],self.n_format_val),\
            lsl = round(dict_width["lower_spec"],self.n_format_spec),\
            usl = round(dict_width["upper_spec"],self.n_format_spec))

            # 轻微缺陷
            width_dimension_res = 1
            #if dict_width["error_code"] == 2:
                #width_dimension_res = 0
            
            # dimension width fail 传导致NG的值,如果OK则传最小值
            if dict_width["min_val"] < dict_width["lower_spec"]:
                dimension_width_val = dict_width["min_val"]
            elif dict_width["max_val"] > dict_width["upper_spec"]:
                dimension_width_val = dict_width["max_val"]
            else:
                dimension_width_val = dict_width["min_val"]
            
            if upload_spec==False:
                cof_glue_dimension_glue_width = cof_glue_dimension_glue_width + "@{result}@{val}@@".format(\
                result = width_dimension_res,\
                val = round(dimension_width_val,self.n_format_val))
            else:
                cof_glue_dimension_glue_width = cof_glue_dimension_glue_width + "@{result}@{val}@{lsl}@{usl}".format(\
                result = width_dimension_res,\
                val = round(dimension_width_val,self.n_format_val),\
                lsl = round(dict_width["lower_spec"],self.n_format_spec),\
                usl = round(dict_width["upper_spec"],self.n_format_spec))

        # 4 area
        # type == overflow 使用overflow
        # type != overflow 使用area missing/dimension fail
        # cof_glue_dimension_glue_area
        # glue_coverage_glue_area_missing
        dict_area = self.__dict_info["region_info"][str_region]["region_info_area"]
        region_type = self.__dict_info["region_info"][str_region]["info_base"]["type"]
        # 如果面积检测未启用,均使用占位符号
        if region_type != "overflow":
            if dict_area["enable"] == 0:
                glue_coverage_glue_area_missing = glue_coverage_glue_area_missing + "@{result}@{val}@{lsl}@{usl}".format(\
                result = 0,\
                val = 0,\
                lsl = 0,\
                usl = 0)

                cof_glue_dimension_glue_area = cof_glue_dimension_glue_area + "@{result}@@".format(\
                result = 0)

                # overflow
                cof_overflow_splatter = cof_overflow_splatter + "@{result}@@".format(\
                result = 0)
                
            else:
                # 严重缺陷 spec为 0.5 USL
                area_missing_res = 1
                if dict_area["error_code"] == 1:
                    area_missing_res = 0
                
                glue_coverage_glue_area_missing = glue_coverage_glue_area_missing + "@{result}@{val}@{lsl}@{usl}".format(\
                result = area_missing_res,\
                val = round(dict_area["current_val"],self.n_format_val),\
                lsl = round(dict_area["lower_spec"],self.n_format_spec),\
                usl = round(dict_area["upper_spec"],self.n_format_spec))

                # 轻微缺陷
                area_dimension_res = 1
                #if dict_area["error_code"] == 2:
                    #area_dimension_res = 0
                if upload_spec==False:
                    cof_glue_dimension_glue_area = cof_glue_dimension_glue_area + "@{result}@{val}@@".format(\
                    result = area_dimension_res,\
                    val = round(dict_area["current_val"],self.n_format_val))
                else:
                    cof_glue_dimension_glue_area = cof_glue_dimension_glue_area + "@{result}@{val}@{lsl}@{usl}".format(\
                    result = area_dimension_res,\
                    val = round(dict_area["current_val"],self.n_format_val),\
                    lsl = round(dict_area["lower_spec"],self.n_format_spec),\
                    usl = round(dict_area["upper_spec"],self.n_format_spec))

                # overflow
                cof_overflow_splatter = cof_overflow_splatter + "@{result}@{val:.4f}@@".format(\
                result = 1,\
                val = round(dict_area["current_val"],self.n_format_val))
        else:
            glue_coverage_glue_area_missing = glue_coverage_glue_area_missing + "@{result}@{val}@{lsl}@{usl}".format(\
                result = 0,\
                val = 0,\
                lsl = 0,\
                usl = 0)

            cof_glue_dimension_glue_area = cof_glue_dimension_glue_area + "@{result}@@".format(\
                result = 0)
            if upload_spec==False:
                cof_overflow_splatter = cof_overflow_splatter + "@{result}@{val}@@".format(\
                result = self.__trans_error(dict_area["error_code"]),\
                val=dict_area["current_val"])
            else:
                cof_overflow_splatter = cof_overflow_splatter + "@{result}@{val}@{lsl}@{usl}".format(\
                result = self.__trans_error(dict_area["error_code"]),\
                val = round(dict_area["current_val"],self.n_format_val),\
                lsl = round(dict_area["lower_spec"],self.n_format_spec),\
                usl = round(dict_area["upper_spec"],self.n_format_spec))

        # 5 shift
        dict_shift = self.__dict_info["region_info"][str_region]["region_info_shift"]
        if upload_spec==False:
            cof_glue_dimension_shift = cof_glue_dimension_shift + "@{result}@{val}@@".format(\
            result = self.__trans_error(dict_shift["error_code"]),\
            val = round(dict_shift["current_val"],self.n_format_val))
        else:
            cof_glue_dimension_shift = cof_glue_dimension_shift + "@{result}@{val}@{lsl}@{usl}".format(\
            result = self.__trans_error(dict_shift["error_code"]),\
            val = round(dict_shift["current_val"],self.n_format_val),\
            lsl = round(dict_shift["lower_spec"],self.n_format_spec),\
            usl = round(dict_shift["upper_spec"],self.n_format_spec))             

        # 6 shiftX
        dict_shiftX = self.__dict_info["region_info"][str_region]["region_info_shiftX"]
        if upload_spec==False:
            cof_glue_dimension_shiftX = cof_glue_dimension_shiftX + "@{result}@{val}@@".format(\
            result = self.__trans_error(dict_shiftX["error_code"]),\
            val = round(dict_shiftX["current_val"],self.n_format_val)) 
        else:
            cof_glue_dimension_shiftX = cof_glue_dimension_shiftX + "@{result}@{val}@{lsl}@{usl}".format(\
            result = self.__trans_error(dict_shiftX["error_code"]),\
            val = round(dict_shiftX["current_val"],self.n_format_val),\
            lsl = round(dict_shiftX["lower_spec"],self.n_format_spec),\
            usl = round(dict_shiftX["upper_spec"],self.n_format_spec)) 

        # 7 shiftY
        dict_shiftY = self.__dict_info["region_info"][str_region]["region_info_shiftY"]
        if upload_spec==False:
            cof_glue_dimension_shiftY = cof_glue_dimension_shiftY + "@{result}@{val}@@".format(\
            result = self.__trans_error(dict_shiftY["error_code"]),\
            val = round(dict_shiftY["current_val"],self.n_format_val)) 
        else:
            cof_glue_dimension_shiftY = cof_glue_dimension_shiftY + "@{result}@{val}@{lsl}@{usl}".format(\
            result = self.__trans_error(dict_shiftY["error_code"]),\
            val = round(dict_shiftY["current_val"],self.n_format_val),\
            lsl = round(dict_shiftY["lower_spec"],self.n_format_spec),\
            usl = round(dict_shiftY["upper_spec"],self.n_format_spec))
                            
        # 8 length
        try:
            str_region_index = "{}".format(region_index)
            dict_length = self.__dict_info["glue_length_info"][str_region_index]
            if upload_spec==False:
                cof_glue_dimension_glue_length = cof_glue_dimension_glue_length + "@{result}@{val}@@".format(\
                result = self.__trans_error(dict_length["error_code"]),\
                val = round(dict_length["current_val"],self.n_format_val)) 
            else:
                cof_glue_dimension_glue_length = cof_glue_dimension_glue_length + "@{result}@{val:.4f}@{lsl:.4f}@{usl:.4f}".format(\
                result = self.__trans_error(dict_length["error_code"]),\
                val = round(dict_length["current_val"],self.n_format_val),\
                lsl = round(dict_length["lower_spec"],self.n_format_spec),\
                usl = round(dict_length["upper_spec"],self.n_format_spec))
        except:
            cof_glue_dimension_glue_length=""

        if dict_coverage_shift["enable"] == False:
            glue_coverage_shift = ""
        if dict_coverage_glue_hole["enable"] == False:
            glue_coverage_glue_hole = ""
        if dict_width["enable"] == False:
            glue_coverage_glue_width_missing = ""
            cof_glue_dimension_glue_width = ""
        if dict_area["enable"] == False:
            glue_coverage_glue_area_missing = ""
            cof_glue_dimension_glue_area = ""
            cof_overflow_splatter = ""
        if dict_shift["enable"] == False:
            cof_glue_dimension_shift = ""
        if dict_shiftX["enable"] == False:
            cof_glue_dimension_shiftX = ""
        if dict_shiftY["enable"] == False:
            cof_glue_dimension_shiftY = ""
        try:
            if dict_length["enable"] == False:
                cof_glue_dimension_glue_length = "" 
        except:
            cof_glue_dimension_glue_length = "" 

        if dict_area["enable"] == True:
            if region_type == "overflow":
                glue_coverage_glue_area_missing = ""
                cof_glue_dimension_glue_area = ""
            else:
                cof_overflow_splatter = ""

        str_mes = ""
        if len(glue_coverage_shift) != 0:
            str_mes = str_mes + "," + glue_coverage_shift
        if len(glue_coverage_glue_hole) != 0:
            str_mes = str_mes + "," + glue_coverage_glue_hole
        if len(glue_coverage_glue_path_broken) != 0:
            str_mes = str_mes + "," + glue_coverage_glue_path_broken
        if len(glue_coverage_glue_width_missing) != 0:
            str_mes = str_mes + "," + glue_coverage_glue_width_missing
        if len(glue_coverage_glue_area_missing) != 0:
            str_mes = str_mes + "," + glue_coverage_glue_area_missing
        if len(cof_overflow_splatter) != 0:
            str_mes = str_mes + "," + cof_overflow_splatter
        if len(cof_glue_dimension_glue_area) != 0:
            str_mes = str_mes + "," + cof_glue_dimension_glue_area
        if len(cof_glue_dimension_glue_width) != 0:
            str_mes = str_mes + "," + cof_glue_dimension_glue_width
        if len(cof_glue_dimension_shift) != 0:
            str_mes = str_mes + "," + cof_glue_dimension_shift
        if len(cof_glue_dimension_glue_length) != 0:
            str_mes = str_mes + "," + cof_glue_dimension_glue_length
        if len(cof_glue_dimension_shiftX) != 0:
            str_mes = str_mes + "," + cof_glue_dimension_shiftX
        if len(cof_glue_dimension_shiftY) != 0:
            str_mes = str_mes + "," + cof_glue_dimension_shiftY  
       
        return str_mes