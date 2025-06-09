import json
import os
# 获取SN
strSN = GvTool.GetToolData("图像源工具.当前文件名称")  # Ex: "Image_ABE000123456F_001.bmp"
SN = strSN[6:19]  # 获取SN ----> "ABE000123456F"

str_A = GvTool.GetToolData("胶路检测_4692.缺陷序列化结果")
str_1 = json.loads(str_A) #   ---> jsonGluePath.json

# 获取面积信息
region_info = str_1["region_info"]
# 获取 current_val region_0, region_1, region_2 (R1, R2, R3)
R1 = region_info["region_0"]["region_info_area"]["current_val"]
R2 = region_info["region_1"]["region_info_area"]["current_val"]
R3 = region_info["region_2"]["region_info_area"]["current_val"]

def WriteFile(path,filename,header,data):
    if(not os.path.exists(path)):
        os.makedirs(path)
    if(not os.path.exists(path+filename)):
        file=open(path+filename,"a")
        file.write(header)
        file.write(data)
        file.close()
    else:
        file=open(path+filename,"a")
        file.write(data)
        file.close()

path = "D:\\Luster\\test\\"
filename = "a.csv"
header = "SN,R1,R2,R3\n"
data = "{:s},{:.3f},{:.3f},{:.3f}\n".format(SN, R1, R2, R3)

WriteFile(path, filename, header, data)
