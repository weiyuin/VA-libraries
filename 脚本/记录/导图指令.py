import os
stt_val = GvTool.GetToolData("数据包解析工具_003.输出数据1")
stt_str = str(stt_val).strip()
GvVar.SetVar("#N",stt_val)

#FOLDER ANH
folder_path = r"D:\AnhVatLieu"
#LINK: D:\AnhVatLieu\ + STT + .BMP
full_path = os.path.join(folder_path, "{}.BMP".format(stt_str))

#是否找到

strReadResult = True

#CHECK & SET
if os.path.exists(full_path):
    std_path = GvVisionAssembly.GsFilePath(full_path)
    GvTool.SetToolData("采集_004.文件路径", std_path)
    bReadResult = True
else:
    bReadResult = False

print(full_path)
GvVar.SetVar("#bReadResult",bReadResult)