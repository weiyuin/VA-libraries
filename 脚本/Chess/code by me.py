from ScImageShow import ScImageShow
guiArray = GvVisionAssembly.GcScriptGuiArray()
X_Start = 400
Y_Start = 100
kich_thuoc = 80
MAU_DO = [255, 0, 0]
MAU_XANH_DEN = [0, 0, 255]
def toado(cot,hang):
    X = X_Start + (cot*kich_thuoc)
    Y = Y_Start + (hang*kich_thuoc)
    return GvVisionAssembly.sc2Vector(X,Y)
def ve_quan(cot,hang,ten,mau):
    centerpos = toado(cot,hang)
    centerposText = GvVisionAssembly.sc2Vector(toado(cot,hang).GetX() - 20,toado(cot,hang).GetY() - 10)
    ScImageShow.ImageShowCircle(ScImageShow,guiArray,centerpos,40, mau,1)
    ScImageShow.ImageShowTextPos(ScImageShow,guiArray,centerposText,ten,mau,30)
#Ve Ban Co
#Ve hang ngang
for row in range(10):
    Point_Left = toado(0,row)
    Point_Right = toado(8,row)
    ScImageShow.ImageShowLineSegVec(ScImageShow,guiArray,Point_Left,Point_Right,[0,255,0],1,0)
#Ve hang doc
for column in range(9):
    Point_Up = toado(column,0)
    Point_Down = toado(column,9)
    if column == 0 or column == 8:
        ScImageShow.ImageShowLineSegVec(ScImageShow,guiArray,Point_Up,Point_Down,[0,255,0],1,0)
    else:
        # continue
        Point_Up_Red = toado(column,0)
        Point_Down_Red = toado(column,4)
        Point_Up_Blue = toado(column,5)
        Point_Down_Blue = toado(column,9)
        ScImageShow.ImageShowLineSegVec(ScImageShow,guiArray,Point_Up_Red,Point_Down_Red,[0,255,0],1,0)
        ScImageShow.ImageShowLineSegVec(ScImageShow,guiArray,Point_Up_Blue,Point_Down_Blue,[0,255,0],1,0)
#Ve cung
Point_Red_A = toado(3,0)
Point_Red_B = toado(5,0)
Point_Red_C = toado(3,2)
Point_Red_D = toado(5,2)
ScImageShow.ImageShowLineSegVec(ScImageShow,guiArray,Point_Red_A,Point_Red_D,[0,255,0],1,0)
ScImageShow.ImageShowLineSegVec(ScImageShow,guiArray,Point_Red_B,Point_Red_C,[0,255,0],1,0)
Point_Blue_A = toado(3,7)
Point_Blue_B = toado(5,7)
Point_Blue_C = toado(3,9)
Point_Blue_D = toado(5,9)
ScImageShow.ImageShowLineSegVec(ScImageShow,guiArray,Point_Blue_A,Point_Blue_D,[0,255,0],1,0)
ScImageShow.ImageShowLineSegVec(ScImageShow,guiArray,Point_Blue_B,Point_Blue_C,[0,255,0],1,0)
#Ve quan
for column in range(0,10,2):
    ve_quan(column,3,"tot",MAU_DO)
    ve_quan(column,6,"tot",MAU_XANH_DEN)
GvGuiDataAgent.SetGraphicDisplay("View-1",guiArray)