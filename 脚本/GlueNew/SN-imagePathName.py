#离线
pathImg = GvTool.GetToolData("图像源工具_001.文件路径")
print(pathImg)
ImgName = pathImg.filePath
strSN = ImgName.split("\\")[-1].split(".")[0]
print(strSN)
strSN = "Tung"
if GvVisionAssembly.GetSystemState() == False:
    strSN = GvTool.GetToolData("图像源工具_001.当前文件名称")

#在线
else:
    strSN = "NguyenCongTung"
print(strSN)
GvVar.SetVar("#strSN",strSN)