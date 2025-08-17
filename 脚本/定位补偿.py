offsetX=-GvVar.GetVar("#dOffsetGuiding_X1")
offsetY=-GvVar.GetVar("#dOffsetGuiding_Y1")

offset=GvVisionAssembly.GcCoordPos(offsetX,offsetY,0)

GvTool.SetToolData("姿态1胶路_5433.补偿值",offset)