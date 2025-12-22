from ScImageShow import ScImageShow

Pos_Center = GvTool.GetToolData("多圆多线查找工具_005.中点_007")
blob_Count = GvTool.GetToolData("Blob工具_012.结果个数")

PosX = Pos_Center.GetX()
PosY = Pos_Center.GetY()
GvVar.SetVar("#X",PosX)
GvVar.SetVar("#Y",PosY)

print("X:" + str(PosX))
print("Y:" + str(PosY))
print("blob_Count:" + str(blob_Count))
    
nRed = 0
nGreen = 0
strSend = GvVar.GetVar("#str_Send")
strNG = GvVar.GetVar("#strNG")
step = GvVar.GetVar("#step")

if(blob_Count == 3):
    nRed = 0
    nGreen = 255
    strSend += f"[{PosX:.3f},{PosY:.3f}] "
    GvVar.SetVar("#str_Send",strSend)
    print("OK")
else:
    nRed = 255
    nGreen = 0
    strNG += "{:d},".format(step)
    GvVar.SetVar("#strNG",strNG)
    print("NG")
    nRed, nGreen = 255, 0
    # Lưu tọa độ X và Y cách nhau dấu |, các điểm cách nhau dấu ;
    strNG_Coords = GvVar.GetVar("#strNG_Coords")
    strNG_Coords += "{:.3f}|{:.3f};".format(PosX, PosY)
    GvVar.SetVar("#strNG_Coords", strNG_Coords)
    print("NG")
guiArray = GvVisionAssembly.GcScriptGuiArray()

print("strSend: " + strSend)
print("Step: " + str(step))
GvVar.SetVar("#str_Send",strSend)

ScImageShow.ImageShowTextXY(ScImageShow, guiArray,10,0, "X: {:3f}".format(PosX),[nRed,nGreen,0], 50, 0)
ScImageShow.ImageShowTextXY(ScImageShow, guiArray,10,50, "Y: {:3f}".format(PosY),[nRed,nGreen,0], 50, 0)
ScImageShow.ImageShowTextXY(ScImageShow, guiArray,10,100, "Blob count: {:d}".format(blob_Count),[nRed,nGreen,0], 50, 0)

GvGuiDataAgent.SetGraphicDisplay("View-1", guiArray)