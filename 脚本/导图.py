import os

def traverse_files(fileDirPath, SN, nPos):
    imagefiles = []
    
    # Bước 1: Duyệt toàn bộ thư mục và thư mục con, tìm file có chứa SN
    for root, dirs, files in os.walk(fileDirPath):
        for file in files:
            if SN in file:                                      # phải có SN sản phẩm
                fullpath = os.path.join(root, file)
                # Bước 2: Kiểm tra xem trong toàn bộ đường dẫn (root + file) có chứa đúng số pose không
                if str(nPos) in fullpath:                       # chỉ cần có số 1,2,3,4,5 là được
                    imagefiles.append(fullpath)
                    break                                       # tìm được 1 tấm là đủ, tránh trùng
    return imagefiles

# ================== Phần chính ==================
fileDirPath = GvVar.GetVar("@strfileDirPath")
SN          = GvVar.GetVar("@strReadSN")
nPos        = GvVar.GetVar("@nReadPos")   # 1 ~ 5

strReadResult = ""

if nPos not in [1,2,3,4,5]:
    strReadResult = "姿态错误，只支持1-5"
elif GvVisionAssembly.GetSystemState():
    strReadResult = "导图失败,请先切换到离线模式"
else:
    imagefiles = traverse_files(fileDirPath, SN, nPos)
    if len(imagefiles) == 0:
        strReadResult = "导图失败,未找到符合条件的文件"
    else:
        std_path = GvVisionAssembly.GsFilePath(imagefiles[0])
        strReadResult = "导图成功,{}".format(imagefiles[0])
        
        # Gán vào tool tương ứng với từng pose
        if   nPos == 1: GvTool.SetToolData("工位1采图_4192.文件路径", std_path)
        elif nPos == 2: GvTool.SetToolData("工位1采图_5412.文件路径", std_path)
        elif nPos == 3: GvTool.SetToolData("工位1采图_XXXX.文件路径", std_path)  # thay XXXX bằng tool pose 3 thật
        elif nPos == 4: GvTool.SetToolData("工位1采图_YYYY.文件路径", std_path)  # thay YYYY bằng tool pose 4 thật
        elif nPos == 5: GvTool.SetToolData("工位1采图_ZZZZ.文件路径", std_path)  # thay ZZZZ bằng tool pose 5 thật

GvVar.SetVar("@strReadResult", strReadResult)