
if GvVar.GetVar("#str_Flowpath")=="L":
    baseX=GvVar.GetVar("#dbasepointX_1")
    baseY=GvVar.GetVar("#dbasepointY_1")
else:
    baseX=GvVar.GetVar("#dbasepointX_2")
    baseY=GvVar.GetVar("#dbasepointY_2")
baseL=GvVar.GetVar("#dDistance_Standard")

SPEC=abs(GvVar.GetVar("#dbasepoint_up")) #基准上限
SPEC_L=abs(GvVar.GetVar("#dDistance_up"))
liveX= GvVar.GetVar("#SendX") #实时坐标
liveY=GvVar.GetVar("#SendY")
liveL=GvVar.GetVar("#dDistance")

def showSytel(index,FontSize=50):
    guiStyle = GvVisionAssembly.GsScriptGuiStyle()
    guiStyle.bVisible = True
    guiStyle.nLineStyle = 2
    guiStyle.nLineWidth = 2
    if index==1:
        guiStyle.clrLineColor = [0,255,0]
    elif index==2:
        guiStyle.clrLineColor = [255,255,0]
    elif index==3:
        guiStyle.clrLineColor = [255,0,0]
    guiStyle.bLabelVisible = True
    guiStyle.lFontSize = FontSize
    return  guiStyle


def ShowInfo(baseX,liveX,SPEC):
    index=0
    spec1=SPEC*0.5
    spec2=SPEC*0.8
    delX=liveX-baseX
    if abs(delX)<spec1 or delX==spec1:
        index=1
    elif abs(delX)>spec1 and  (abs(delX)<spec2 or abs(delX)== spec2) :
        index=2
    else:
        index=3
    return index
    
def CreatShowInfo(guiStyle,X,Y,Text):
    guiText = GvVisionAssembly.GsScriptGuiText()
    guiText.sScriptGuiStyle = guiStyle
    guiText.strText =Text
    guiText.posX = X
    guiText.posY = Y
    guiText.deg = 0.0
    return guiText

def CreatText(liveX,baseX,SPEC,X):
    strShowX="{}: {:.2f} [{:.2f},{:.2f}] \r\n🔼{:.2f}".format(X,liveX,baseX-SPEC,baseX+SPEC,liveX-baseX) 
    return strShowX

guiArray = GvVisionAssembly.GcScriptGuiArray()
X="X"
Y="Y"
L="L"
listText=[[CreatText(liveX,baseX,SPEC,X),ShowInfo(baseX,liveX,SPEC)],[CreatText(liveY,baseY,SPEC,Y),ShowInfo(baseY,liveY,SPEC)],[CreatText(liveL,baseL,SPEC_L,L),ShowInfo(liveL,baseL,SPEC_L)]]         
for i in range(0,len(listText)):
    guiArray.Add(CreatShowInfo(showSytel(listText[i][1],100),4250,20+i*280,listText[i][0])) 
if GvVar.GetVar("#str_Flowpath")=="L": 
    GvGuiDataAgent.SetGraphicDisplay("左流道定位", guiArray)  
else:
    GvGuiDataAgent.SetGraphicDisplay("右流道定位", guiArray)    