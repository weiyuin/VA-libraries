MarkPoint=GvTool.GetToolData("找任意曲线工具_018.全部探测点")
pointvec=GvVisionAssembly.sc2VectorVec()
pointvec.extend(MarkPoint)
for i in range(0,len(MarkPoint)):
    #kich co ROI laay tu diem do` 018
    X=pointvec[len(MarkPoint)-i-1].GetX()-2
    Y=pointvec[len(MarkPoint)-i-1].GetY()-2
    point=GvVisionAssembly.sc2Vector(X,Y)
    pointvec.append(point)



GvTool.SetToolData("Blob工具_021.公开多边形ROI",GvVisionAssembly.scPolyline(pointvec,True))