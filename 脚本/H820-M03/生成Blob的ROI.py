from ScImageShow import ScImageShow
guiArray = GvVisionAssembly.GcScriptGuiArray()

point=GvTool.GetToolData("找任意曲线工具_6844.采样拟合点集GUI")
scVec=GvVisionAssembly.sc2VectorVec()
for i in range(0,len(point)):
    tempPoint=GvVisionAssembly.sc2Vector( point[i].pt.GetX(), point[i].pt.GetY())
    scVec.append(tempPoint)

print(len(scVec))
GvTool.SetToolData("Blob工具_6840.公开多边形ROI",GvVisionAssembly.scPolyline(scVec,True))
