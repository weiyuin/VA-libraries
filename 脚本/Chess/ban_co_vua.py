from ScImageShow import ScImageShow

guiArray = GvVisionAssembly.GcScriptGuiArray()
X_Start = 400
Y_Start = 90
Column_count = 9
Row_count = 9
Size = 80
def CreatPos(column,row):
    CurrentX = X_Start + (Size*column)
    CurrentY = Y_Start + (Size*row)
    return GvVisionAssembly.sc2Vector(CurrentX,CurrentY)
def CreatText(PosText,text):
    # PosText([0,15],[9,-15])
    # PosText = [[column,X],[row,Y]]
    CurrentX = X_Start + (Size*PosText[0][0] + PosText[0][1])
    CurrentY = Y_Start + (Size*PosText[1][0] + PosText[1][1])
    PositionText = GvVisionAssembly.sc2Vector(CurrentX,CurrentY)
    ScImageShow.ImageShowTextPos(ScImageShow, guiArray,PositionText,text,[0,0,255],50)
def DrawBlack(column,row):
    # Center = CreatPos(column,row)
    CurrentX = X_Start + (Size*column) + Size/2
    CurrentY = Y_Start + (Size*row) + Size/2
    Center = GvVisionAssembly.sc2Vector(CurrentX,CurrentY)
    for size in range (5,80,5):
        ScImageShow.ImageShowRecCenter(ScImageShow, guiArray,Center,size,size,[0, 0, 0],3)
#==================Ve ban co
#draw column
for column in range(Column_count):
    PosUp = CreatPos(column,0)
    PosDown = CreatPos(column,8)
    ScImageShow.ImageShowLineSegVec(ScImageShow,guiArray,PosUp,PosDown,[0, 255, 0],1,0)
#draw row
for row in range(Row_count):
    PosLeft = CreatPos(0,row)
    PosRight = CreatPos(8,row)
    ScImageShow.ImageShowLineSegVec(ScImageShow,guiArray,PosLeft,PosRight,[0, 255, 0],1,0)
#Text
text_row = ["A","B","C","D","E","F","G","H"]
for column in range(Column_count-1):
    CreatText(([column,25],[0,-60]),str(text_row[column]))
    CreatText(([column,25],[8,0]),str(text_row[column]))
for row in range(Row_count-1):
    CreatText(([0,-35],[row,10]),str(row + 1))
    CreatText(([8,35],[row,10]),str(row + 1))
for column in range(0,Column_count-1,1):
    for row in range(0,Row_count-1,2):
        if column % 2 == 0:
            DrawBlack(column,row)
        if column % 2 != 0:
            DrawBlack(column,row+1)
# DrawBlack(0,2)
# DrawBlack(1,1)
GvGuiDataAgent.SetGraphicDisplay("View-2",guiArray)