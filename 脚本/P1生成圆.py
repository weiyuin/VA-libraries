import math
bLeftOrRight=GvVar.GetVar("@bLeftOrRight")
ImgWidth=GvVar.GetVar("@nImgWidth")

center=GvTool.GetToolData("1_820.图像坐标")[0]
   
rotation1= 0.0
print(rotation1)
def point(point,d,center):
    posx=center.GetX()
    posy=center.GetY()
    posx1=point.GetX()
    posy1=point.GetY()
    x1=(posx1-posx)*math.cos(d*math.pi/180)-(posy1-posy)*math.sin(d*math.pi/180)+posx
    y1=(posx1-posx)*math.sin(d*math.pi/180)+(posy1-posy)*math.cos(d*math.pi/180)+posy
    pointoff=GvVisionAssembly.sc2Vector(x1,y1)
    return pointoff
f=0
print(f)
p1=GvVisionAssembly.sc2Vector(center.GetX()-f,center.GetY())
p2=GvVisionAssembly.sc2Vector(center.GetX()+f,center.GetY())
p11=point(p1,rotation1,center)

if bLeftOrRight==False:
    p11=GvVisionAssembly.sc2Vector(ImgWidth-p11.GetX(),p11.GetY())

e=0.22/GvVar.GetVar("@dPixelScale1")/2
print(e)
c=GvVisionAssembly.sc2Vector(e,e)
d=GvVisionAssembly.scRadian(0)

scEllipse1=GvVisionAssembly.scEllipse(p11,c,d)

GvTool.SetToolData("P1灰度检测工具_1431.椭圆检测区域",scEllipse1)


