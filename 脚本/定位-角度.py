# 上位机是否开启角度修正功能  1-开启 0-未开启
nAngleModify = GvVar.GetVar("#nAngleModify")

if nAngleModify == 1:
    scLineAngle = GvTool.GetToolData("高级找线工具_5538.直线绝对角度")
    GvTool.SetToolData("直线生成工具_5701.线段角度",scLineAngle)
    
else:
    scLineAngle = GvTool.GetToolData("轴位置生成工具_5483.平台轴位置.PosD")
    GvTool.SetToolData("直线生成工具_5701.线段角度",scLineAngle)
