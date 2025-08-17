offsetX = GvTool.GetToolData("姿态1胶路_5433.补偿值").X
offsetY = GvTool.GetToolData("姿态1胶路_5433.补偿值").Y

GvVar.SetVar("#dStation1_1_X",GvTool.GetToolData("姿态1胶路_5433.胶路起始点").GetX()+offsetX)
GvVar.SetVar("#dStation1_1_Y",GvTool.GetToolData("姿态1胶路_5433.胶路起始点").GetY()+offsetY)