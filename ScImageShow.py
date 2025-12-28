import sys
# sys.path.append(r'C:\Program Files\VISIONAssembly_x64')
import GvVisionAssembly
import math

# Đã được, chỉ cần để đường dẫn là thư mục chứa file .pyd là xong

class ScImageShow:
    '''
    Chương trình phiên bản cũ, dùng nội bộ
    '''

    '''
    Hàm phiên bản cũ
    '''
# Dùng XY để biểu diễn vị trí hiển thị của chuỗi văn bản cần hiện @
    @staticmethod
    def imageShowTextXY(posX=100, posY=100, strmsg="hello", clrLineColor=[0, 255, 0], lFontSize=100):
        # 设置GUI格式
        guiStyle = GvVisionAssembly.GsScriptGuiStyle()
        guiStyle.bVisible = True
        guiStyle.nLineStyle = 2
        guiStyle.nLineWidth = 2
        guiStyle.clrLineColor = clrLineColor
        guiStyle.bLabelVisible = True
        guiStyle.strLabelFont = "Calibri"
        guiStyle.lFontSize = lFontSize
        ######## GUI设置 ########

        # 文本GUI显示设置
        guiText = GvVisionAssembly.GsScriptGuiText()
        guiText.sScriptGuiStyle = guiStyle
        guiText.strText = strmsg
        guiText.posX = posX
        guiText.posY = posY
        guiText.deg = 0.0
        # guiArray.Add(guiText)
        # 将GUI数组设置到视图
        return guiText


#用二维向量的位置显示文字
    def imageShowTextPos(pos,strmsg="hello",clrLineColor = [0, 255, 0],lFontSize = 100):
        # 设置GUI格式
        guiStyle = GvVisionAssembly.GsScriptGuiStyle()
        guiStyle.bVisible = True
        guiStyle.nLineStyle = 2
        guiStyle.nLineWidth = 2
        guiStyle.clrLineColor = clrLineColor
        guiStyle.bLabelVisible = True
        guiStyle.strLabelFont = "Calibri"
        guiStyle.lFontSize = lFontSize
        ######## GUI设置 ########

        # 文本GUI显示设置
        guiText = GvVisionAssembly.GsScriptGuiText()
        guiText.sScriptGuiStyle = guiStyle
        guiText.strText = strmsg
        guiText.posX = pos.GetX()
        guiText.posY = pos.GetY()
        guiText.deg = 0.0
        #guiArray.Add(guiText)
        # 将GUI数组设置到视图
        return guiText

#用二维向量的位置显示圆
    def imageShowCircle(centerpos,R=50,clrLineColor = [0, 255, 0],nLineWidth = 1):
        guiStyle = GvVisionAssembly.GsScriptGuiStyle()
        guiStyle.bVisible = True
        guiStyle.nLineStyle = 0
        guiStyle.nLineWidth = nLineWidth
        guiStyle.clrLineColor = clrLineColor
        guiStyle.bLabelVisible = True
        guiStyle.strLabel = ""  # 如果不需要显示label标签，这一行代码可以删除
        guiStyle.strLabelFont = "Arial"
        guiStyle.lFontSize = 20

        guiCircle = GvVisionAssembly.GsScriptGuiCircle()
        #center = GvVisionAssembly.sc2Vector(100, 100)  # 圆心位置
        guiCircle.circle = GvVisionAssembly.scCircle(centerpos, R)
        guiCircle.sScriptGuiStyle = guiStyle
        #guiArray.Add(guiCircle)
        return guiCircle

#用点向量生成多边形
    def imageShowPolyline(VectorVec,clrLineColor = [0, 255, 0],nLineWidth = 1):
        guiStyle = GvVisionAssembly.GsScriptGuiStyle()
        guiStyle.bVisible = True
        guiStyle.nLineStyle = 0
        guiStyle.nLineWidth = nLineWidth
        guiStyle.clrLineColor = clrLineColor
        guiStyle.bLabelVisible = True
        guiStyle.strLabel = ""  # 如果不需要显示label标签，这一行代码可以删除
        guiStyle.strLabelFont = "Arial"
        guiStyle.lFontSize = 20

        guiPolyline = GvVisionAssembly.GsScriptGuiPolyline()
        guiPolyline.polyline = GvVisionAssembly.scPolyline(VectorVec, True)
        guiStyle.strLabel = ""  # 如果不需要显示label标签，这一行代码可以删除
        guiPolyline.sScriptGuiStyle = guiStyle

        #guiArray.Add(guiCircle)
        return guiPolyline

    #用直线显示直线的位置
    def imageShowLine(line,clrLineColor = [0, 255, 0],nLineWidth = 1):
        guiStyle = GvVisionAssembly.GsScriptGuiStyle()
        guiStyle.bVisible = True
        guiStyle.nLineStyle = 0
        guiStyle.nLineWidth = nLineWidth
        guiStyle.clrLineColor = clrLineColor
        guiStyle.bLabelVisible = True
        guiStyle.strLabel = ""  # 如果不需要显示label标签，这一行代码可以删除
        guiStyle.strLabelFont = "Arial"
        guiStyle.lFontSize = 20

        # Gui直线

        guiLine = GvVisionAssembly.GsScriptGuiLine()
        guiLine.line = line
        guiLine.sScriptGuiStyle = guiStyle

        return guiLine


    #用线段显示线段的位置
    def imageShowLineSeg(self,lineSeg,clrLineColor = [0, 255, 0],nLineWidth = 1):
        guiStyle = GvVisionAssembly.GsScriptGuiStyle()
        guiStyle.bVisible = True
        guiStyle.nLineStyle = 0
        guiStyle.nLineWidth = nLineWidth
        guiStyle.clrLineColor = clrLineColor
        guiStyle.bLabelVisible = True
        guiStyle.strLabel = ""  # 如果不需要显示label标签，这一行代码可以删除
        guiStyle.strLabelFont = "Arial"
        guiStyle.lFontSize = 20

        # Gui直线
        guiLineSeg = GvVisionAssembly.GsScriptGuiLineSeg()
        guiLineSeg.lineSeg = lineSeg
        guiLineSeg.sScriptGuiStyle = guiStyle

        return guiLineSeg

    # Hiển thị dấu chữ thập (cross) theo kiểu vector
    # self         : chính là đối tượng lớp ScImageShow
    # Vec          : vector 2D chứa vị trí và góc xoay (x, y, angle)
    # guiArray     : mảng ảnh để vẽ lên (buffer hiển thị)
    # size         : kích thước của dấu chữ thập (độ dài mỗi nhánh)
    # clrLineColor : màu vẽ đường line
    # nLineWidth   : độ dày nét vẽ
    def imagechowCrossVec(self,Vec,clrLineColor = [0, 255, 0],nLineWidth = 1):
        # 设置GUI格式
        guiStyle = GvVisionAssembly.GsScriptGuiStyle()
        guiStyle.bVisible = True
        guiStyle.nLineStyle = 2
        guiStyle.nLineWidth = nLineWidth
        guiStyle.clrLineColor = clrLineColor
        guiStyle.bLabelVisible = True
        guiStyle.strLabelFont = "Arial"
        guiStyle.lFontSize = 100
        # 获取GUI显示数组
        # 十字GUI显示设置
        guiCross = GvVisionAssembly.GsScriptGuiCross()
        guiCross.sScriptGuiStyle = guiStyle
        guiCross.cross.SetX(Vec.GetX())
        guiCross.cross.SetY(Vec.GetY())
        return guiCross



    # Hiển thị十字 (dấu chữ thập) theo vị trí và tư thế (pose)
    # self         : chính là đối tượng lớp ScImageShow
    # Cood         : tọa độ + góc xoay (pose) cần vẽ
    # guiArray     : mảng ảnh để hiển thị/vẽ lên
    # size         : kích thước của十字 (chiều dài mỗi nhánh)
    # clrLineColor : màu vẽ đường line
    # nLineWidth   : độ dày nét vẽ
    def imagechowCrossCood(self, Cood,guiArray, size=10,clrLineColor=[0, 255, 0], nLineWidth=1):
    # 设置GUI格式
        guiStyle = GvVisionAssembly.GsScriptGuiStyle()
        guiStyle.bVisible = True
        guiStyle.nLineStyle = 2
        guiStyle.nLineWidth = nLineWidth
        guiStyle.clrLineColor = clrLineColor
        guiStyle.bLabelVisible = True
        guiStyle.strLabelFont = "Arial"
        guiStyle.lFontSize = 100
    # 获取GUI显示数组

        C = GvVisionAssembly.scCircle(GvVisionAssembly.sc2Vector(Cood.X,Cood.Y), size)
        L1 = GvVisionAssembly.scLine(GvVisionAssembly.sc2Vector(Cood.X,Cood.Y), GvVisionAssembly.scRadian(Cood.D*math.pi/180.0))
        L2 = GvVisionAssembly.scLine(GvVisionAssembly.sc2Vector(Cood.X, Cood.Y), GvVisionAssembly.scRadian((Cood.D+90) * math.pi / 180.0))


        P=GvVisionAssembly.InterSectLineCircle(L1, C)
        P1 = P.points[0]
        P2 = P.points[1]
        LineSeg1=GvVisionAssembly.scLineSeg(P1,P2)
        guiArray.Add(self.imageShowLineSeg(self,LineSeg1,clrLineColor,nLineWidth))

        P=GvVisionAssembly.InterSectLineCircle(L2, C)
        P3 = P.points[0]
        P4 = P.points[1]
        LineSeg2=GvVisionAssembly.scLineSeg(P3,P4)
        guiArray.Add(self.imageShowLineSeg(self,LineSeg2,clrLineColor,nLineWidth))

        return True


    '''
    新版本函数
    '''

    # Hiển thị text tại tọa độ XY (có thể xoay góc)
    # self         : chính instance của lớp ScImageShow
    # guiArray     : mảng ảnh để vẽ chữ lên (buffer hiển thị)
    # posX         : tọa độ X (kiểu double)
    # posY         : tọa độ Y (kiểu double)
    # strmsg       : chuỗi văn bản cần hiển thị (string)
    # clrLineColor : màu chữ, định dạng RGB, mặc định [0, 255, 0] → xanh lá
    # lFontSize    : cỡ chữ (int)
    # degree       : góc xoay chữ (độ), mặc định 0.0 (không xoay)
    def ImageShowTextXY(self,guiArray,posX=100,posY=100,strmsg="hello",clrLineColor = [0, 255, 0],lFontSize = 100,degree=0.0):
    # 设置GUI格式
        guiStyle = GvVisionAssembly.GsScriptGuiStyle()
        guiStyle.bVisible = True
        guiStyle.nLineStyle = 2
        guiStyle.nLineWidth = 2
        guiStyle.clrLineColor = clrLineColor
        guiStyle.bLabelVisible = True
        guiStyle.strLabelFont = "Calibri"
        guiStyle.lFontSize = lFontSize
        ######## GUI设置 ########

        # 文本GUI显示设置
        guiText = GvVisionAssembly.GsScriptGuiText()
        guiText.sScriptGuiStyle = guiStyle
        guiText.strText = strmsg
        guiText.posX = posX
        guiText.posY = posY
        guiText.deg = degree

        guiArray.Add(guiText)
        # 将GUI数组设置到视图
        return True


    # Hiển thị văn bản tại vị trí sử dụng vector hai chiều mới
    # self: bản thân lớp ScImageShow
    # guiArray: mảng hiển thị guiArray
    # pos: kiểu ScVector, biểu thị vị trí hiển thị
    # strmsg: kiểu string, nội dung cần hiển thị
    # clrLineColor: kiểu RGB, mặc định là [0, 255, 0] (màu xanh lá)
    # lFontSize: kiểu int, cỡ chữ
    def ImageShowTextPos(self,guiArray,pos,strmsg="hello",clrLineColor=[0, 255, 0],lFontSize=100):
        # 设置GUI格式
        guiStyle = GvVisionAssembly.GsScriptGuiStyle()
        guiStyle.bVisible = True
        guiStyle.nLineStyle = 2
        guiStyle.nLineWidth = 2
        guiStyle.clrLineColor = clrLineColor
        guiStyle.bLabelVisible = True
        guiStyle.strLabelFont = "Calibri"
        guiStyle.lFontSize = lFontSize
        ######## GUI设置 ########

        # 文本GUI显示设置
        guiText = GvVisionAssembly.GsScriptGuiText()
        guiText.sScriptGuiStyle = guiStyle
        guiText.strText = strmsg
        guiText.posX = pos.GetX()
        guiText.posY = pos.GetY()
        guiText.deg = 0.0
        guiArray.Add(guiText)
        # 将GUI数组设置到视图
        return guiText

    # Vẽ hình tròn theo vị trí vector 2D (phiên bản mới)
    # self         : chính instance của lớp ScImageShow
    # guiArray     : mảng ảnh để vẽ lên (buffer hiển thị)
    # centerpos    : kiểu ScVector, tọa độ tâm đường tròn (x, y, có thể kèm góc)
    # R            : kiểu int, bán kính đường tròn (pixel)
    # clrLineColor : màu vẽ viền, kiểu RGB, mặc định [0, 255, 0] → xanh lá
    # nLineWidth   : kiểu int, độ dày nét vẽ (line width)
    def ImageShowCircle(self,guiArray,centerpos, R=50, clrLineColor=[0, 255, 0], nLineWidth=1):
        guiStyle = GvVisionAssembly.GsScriptGuiStyle()
        guiStyle.bVisible = True
        guiStyle.nLineStyle = 0
        guiStyle.nLineWidth = nLineWidth
        guiStyle.clrLineColor = clrLineColor
        guiStyle.bLabelVisible = True
        guiStyle.strLabel = ""  # 如果不需要显示label标签，这一行代码可以删除
        guiStyle.strLabelFont = "Arial"
        guiStyle.lFontSize = 20

        guiCircle = GvVisionAssembly.GsScriptGuiCircle()
        # center = GvVisionAssembly.sc2Vector(100, 100)  # 圆心位置
        guiCircle.circle = GvVisionAssembly.scCircle(centerpos, R)
        guiCircle.sScriptGuiStyle = guiStyle
        guiArray.Add(guiCircle)
        return True

    # Vẽ hình tròn theo đối tượng ScCircle (phiên bản mới)
    # self         : chính instance của lớp ScImageShow
    # guiArray     : mảng ảnh để vẽ lên (buffer hiển thị)
    # circle       : kiểu ScCircle, chứa thông tin tâm và bán kính của đường tròn
    # R            : kiểu int, bán kính đường tròn (thường dùng để override hoặc làm tham số phụ)
    # clrLineColor : màu viền, kiểu RGB, mặc định [0, 255, 0] → xanh lá cây
    # nLineWidth   : kiểu int, độ dày nét vẽ (line width)
    def ImageShowWholeCircle(self,guiArray,circle, clrLineColor=[0, 255, 0], nLineWidth=1):
        guiStyle = GvVisionAssembly.GsScriptGuiStyle()
        guiStyle.bVisible = True
        guiStyle.nLineStyle = 0
        guiStyle.nLineWidth = nLineWidth
        guiStyle.clrLineColor = clrLineColor
        guiStyle.bLabelVisible = True
        guiStyle.strLabel = ""  # 如果不需要显示label标签，这一行代码可以删除
        guiStyle.strLabelFont = "Arial"
        guiStyle.lFontSize = 20

        guiCircle = GvVisionAssembly.GsScriptGuiCircle()
        guiCircle.circle = circle
        guiCircle.sScriptGuiStyle = guiStyle
        guiArray.Add(guiCircle)
        return True


    # Vẽ đa giác từ tập hợp các điểm vector
    # self         : chính instance của lớp ScImageShow
    # guiArray     : mảng ảnh để vẽ lên (buffer hiển thị)
    # VectorVec    : kiểu ScVectorVec, danh sách các điểm (vector) tạo thành đa giác
    # clrLineColor : màu viền đa giác, kiểu RGB, mặc định [0, 255, 0] → xanh lá
    # nLineWidth   : độ dày đường viền (line width), kiểu int
    def ImageShowPolyline(self,guiArray,VectorVec, clrLineColor=[0, 255, 0], nLineWidth=1):
        guiStyle = GvVisionAssembly.GsScriptGuiStyle()
        guiStyle.bVisible = True
        guiStyle.nLineStyle = 0
        guiStyle.nLineWidth = nLineWidth
        guiStyle.clrLineColor = clrLineColor
        guiStyle.bLabelVisible = True
        guiStyle.strLabel = ""  # 如果不需要显示label标签，这一行代码可以删除
        guiStyle.strLabelFont = "Arial"
        guiStyle.lFontSize = 20

        guiPolyline = GvVisionAssembly.GsScriptGuiPolyline()
        guiPolyline.polyline = GvVisionAssembly.scPolyline(VectorVec, True)
        guiStyle.strLabel = ""  # 如果不需要显示label标签，这一行代码可以删除
        guiPolyline.sScriptGuiStyle = guiStyle

        guiArray.Add(guiPolyline)
        return guiPolyline



    # Vẽ đường thẳng theo đối tượng ScLine
    # self         : chính instance của lớp ScImageShow
    # guiArray     : mảng ảnh để vẽ lên (buffer hiển thị)
    # line         : kiểu ScLine, đối tượng chứa thông tin đường thẳng cần hiển thị
    # clrLineColor : màu đường thẳng, kiểu RGB, mặc định [0, 255, 0] → xanh lá
    # nLineWidth   : độ dày nét vẽ (line width), kiểu int
    def ImageShowLine(self,guiArray,line,clrLineColor = [0, 255, 0],nLineWidth = 1):
        guiStyle = GvVisionAssembly.GsScriptGuiStyle()
        guiStyle.bVisible = True
        guiStyle.nLineStyle = 0
        guiStyle.nLineWidth = nLineWidth
        guiStyle.clrLineColor = clrLineColor
        guiStyle.bLabelVisible = True
        guiStyle.strLabel = ""  # 如果不需要显示label标签，这一行代码可以删除
        guiStyle.strLabelFont = "Arial"
        guiStyle.lFontSize = 20

        # Gui直线

        guiLine = GvVisionAssembly.GsScriptGuiLine()
        guiLine.line = line
        guiLine.sScriptGuiStyle = guiStyle
        guiArray.Add(guiLine)
        return True

    # Vẽ vùng hình chữ nhật (rectangle)
    # self         : chính instance của lớp ScImageShow
    # guiArray     : mảng ảnh để vẽ lên (buffer hiển thị)
    # rect         : kiểu scRect, đối tượng chứa thông tin hình chữ nhật
    # clrLineColor : màu viền, kiểu RGB, mặc định [0, 255, 0] → xanh lá
    # nLineWidth   : độ dày viền (line width), kiểu int
    # strLabel     : chuỗi nhãn hiển thị bên cạnh rectangle (mặc định rỗng "")
    def ImageShowRec(self, guiArray, rect, clrLineColor=[0, 255, 0], nLineWidth=1,strLabel = ""):
        guiStyle = GvVisionAssembly.GsScriptGuiStyle()
        guiStyle.bVisible = True
        guiStyle.nLineStyle = 0
        guiStyle.nLineWidth = nLineWidth
        guiStyle.clrLineColor = clrLineColor
        guiStyle.bLabelVisible = True
        guiStyle.strLabel = ""  # 如果不需要显示label标签，这一行代码可以删除
        guiStyle.strLabelFont = "Arial"
        guiStyle.lFontSize = 20
        # 矩形GUI
        guiRect = GvVisionAssembly.GsScriptGuiRect()
        guiRect.rect = rect
        guiStyle.strLabel = strLabel

        guiRect.sScriptGuiStyle = guiStyle

        guiArray.Add(guiRect)
        return True

    # Hiển thị vùng hình chữ nhật
    # self: Chính là lớp ScImageShow
    # guiArray: Mảng hiển thị guiArray
    # centerPos: Kiểu scVector, biểu thị vị trí tâm hình chữ nhật
    # W: Kiểu double, biểu thị chiều rộng hình chữ nhật
    # H: Kiểu double, biểu thị chiều cao hình chữ nhật
    # clrLineColor: Kiểu RGB, mặc định là [0, 255, 0] màu xanh lá
    # nLineWidth: Kiểu int, biểu thị độ rộng nét vẽ
    # strLabel = "": Kiểu string, hiển thị nhãn (tên/số hiệu) của hình chữ nhật
    def ImageShowRecCenter(self, guiArray,centerPos,W=100,H=200, clrLineColor=[0, 255, 0], nLineWidth=1,strLabel = ""):
        guiStyle = GvVisionAssembly.GsScriptGuiStyle()
        guiStyle.bVisible = True
        guiStyle.nLineStyle = 0
        guiStyle.nLineWidth = nLineWidth
        guiStyle.clrLineColor = clrLineColor
        guiStyle.bLabelVisible = True
        guiStyle.strLabel = strLabel
        guiStyle.strLabelFont = "Arial"
        guiStyle.lFontSize = 20
        # 矩形GUI
        pos=GvVisionAssembly.sc2Vector(centerPos.GetX()- W/2.0,centerPos.GetY()- H/2.0)
        rect= GvVisionAssembly.scRect(pos,GvVisionAssembly.sc2Vector(W,H))
        guiRect = GvVisionAssembly.GsScriptGuiRect()
        guiRect.rect = rect
        guiRect.sScriptGuiStyle = guiStyle

        guiArray.Add(guiRect)
        return True

    # Hiển thị vùng hình chữ nhật (Affine)
    # self: Chính là lớp ScImageShow
    # guiArray: Mảng hiển thị guiArray
    # affinerect: Kiểu scaffinerect, biểu thị hình chữ nhật affine (hình chữ nhật có thể xoay)
    # clrLineColor: Kiểu RGB, mặc định là [0, 255, 0] màu xanh lá
    # nLineWidth: Kiểu int, biểu thị độ rộng nét vẽ
    # strLabel = "": Kiểu string, hiển thị nhãn của hình chữ nhật
    def ImageShowAffRec(self, guiArray, affinerect, clrLineColor=[0, 255, 0], nLineWidth=1,strLabel = ""):
        guiStyle = GvVisionAssembly.GsScriptGuiStyle()
        guiStyle.bVisible = True
        guiStyle.nLineStyle = 0
        guiStyle.nLineWidth = nLineWidth
        guiStyle.clrLineColor = clrLineColor
        guiStyle.bLabelVisible = True
        guiStyle.strLabel = strLabel
        guiStyle.strLabelFont = "Arial"
        guiStyle.lFontSize = 20
        # 仿射矩形Gui对象
        affinerect_gui = GvVisionAssembly.GsScriptGuiAffineRect()
        affinerect_gui.sScriptGuiStyle = guiStyle
        affinerect_gui.affineRect = affinerect

        guiArray.Add(affinerect_gui)
        return True


    # Hiển thị vùng hình chữ nhật
    # self: Chính là lớp ScImageShow
    # guiArray: Mảng hiển thị guiArray
    # centerPos: Kiểu scVector, biểu thị vị trí (tâm) hình chữ nhật
    # W: Kiểu double, biểu thị chiều rộng hình chữ nhật
    # H: Kiểu double, biểu thị chiều cao hình chữ nhật
    # clrLineColor: Kiểu RGB, mặc định là [0, 255, 0] màu xanh lá
    # nLineWidth: Kiểu int, biểu thị độ rộng nét vẽ
    # strLabel = "": Kiểu string, hiển thị nhãn (tên) của hình chữ nhật
    def ImageShowAffRecCenter(self, guiArray,centerPos,W=100,H=200,dangle=0.0, clrLineColor=[0, 255, 0], nLineWidth=1,strLabel = ""):
        guiStyle = GvVisionAssembly.GsScriptGuiStyle()
        guiStyle.bVisible = True
        guiStyle.nLineStyle = 0
        guiStyle.nLineWidth = nLineWidth
        guiStyle.clrLineColor = clrLineColor
        guiStyle.bLabelVisible = True
        guiStyle.strLabel = strLabel
        guiStyle.strLabelFont = "Arial"
        guiStyle.lFontSize = 20
        xRotation=GvVisionAssembly.scRadian(dangle*math.pi/180.0)
        skew=GvVisionAssembly.scRadian(0.0*math.pi/180.0)


        affrect=GvVisionAssembly.scAffineRect(centerPos, W, H, xRotation, skew)

        # 仿射矩形Gui对象
        affinerect_gui = GvVisionAssembly.GsScriptGuiAffineRect()
        affinerect_gui.affineRect = affrect
        affinerect_gui.sScriptGuiStyle = guiStyle

        guiArray.Add(affinerect_gui)
        return True

    # Sử dụng đoạn thẳng để hiển thị vị trí của đoạn thẳng
    # self: Chính là lớp ScImageShow
    # guiArray: Mảng hiển thị guiArray
    # line: Kiểu ScLineSeg, biểu thị đoạn thẳng
    # clrLineColor: Kiểu RGB, mặc định là [0, 255, 0] màu xanh lá
    # nLineWidth: Kiểu int, biểu thị độ rộng (độ dày) của nét vẽ
    def ImageShowLineSeg(self,guiArray,lineSeg, clrLineColor=[0, 255, 0], nLineWidth=1):
        guiStyle = GvVisionAssembly.GsScriptGuiStyle()
        guiStyle.bVisible = True
        guiStyle.nLineStyle = 0
        guiStyle.nLineWidth = nLineWidth
        guiStyle.clrLineColor = clrLineColor
        guiStyle.bLabelVisible = True
        guiStyle.strLabel = ""  # 如果不需要显示label标签，这一行代码可以删除
        guiStyle.strLabelFont = "Arial"
        guiStyle.lFontSize = 20

        # Gui直线
        guiLineSeg = GvVisionAssembly.GsScriptGuiLineSeg()
        guiLineSeg.lineSeg = lineSeg
        guiLineSeg.sScriptGuiStyle = guiStyle
        guiArray.Add(guiLineSeg)
        return True

    # Sử dụng đoạn thẳng để hiển thị vị trí của đoạn thẳng
    # self: Chính là lớp ScImageShow
    # guiArray: Mảng hiển thị guiArray
    # Pos1/Pos2: Kiểu ScVector, biểu thị vector hai chiều (2D)
    # clrLineColor: Kiểu RGB, mặc định là [0, 255, 0] màu xanh lá
    # nLineWidth: Kiểu int, biểu thị độ rộng (độ dày) của nét vẽ
    def ImageShowLineSegVec(self,guiArray,Pos1,Pos2, clrLineColor=[0, 255, 0], nLineWidth=1,nLineStyle=0):
        guiStyle = GvVisionAssembly.GsScriptGuiStyle()
        guiStyle.bVisible = True
        guiStyle.nLineStyle = nLineStyle
        guiStyle.nLineWidth = nLineWidth
        guiStyle.clrLineColor = clrLineColor
        guiStyle.bLabelVisible = True
        guiStyle.strLabel = ""  # 如果不需要显示label标签，这一行代码可以删除
        guiStyle.strLabelFont = "Arial"
        guiStyle.lFontSize = 20

        lineSeg=GvVisionAssembly.scLineSeg(Pos1,Pos2)

        # Gui直线
        guiLineSeg = GvVisionAssembly.GsScriptGuiLineSeg()
        guiLineSeg.lineSeg = lineSeg
        guiLineSeg.sScriptGuiStyle = guiStyle
        guiArray.Add(guiLineSeg)
        return True

    # Hiển thị hình chữ thập (cross) cho vector
    # self: Chính là lớp ScImageShow
    # Vec: Vị trí vector 2 chiều (bao gồm cả góc)
    # guiArray: Mảng hiển thị
    # clrLineColor: Màu hiển thị
    # nLineWidth: Độ rộng nét vẽ (độ dày)
    def ImagechowCrossVec(self,guiArray, Vec, clrLineColor=[0, 255, 0], nLineWidth=1):
        # 设置GUI格式
        guiStyle = GvVisionAssembly.GsScriptGuiStyle()
        guiStyle.bVisible = True
        guiStyle.nLineStyle = 2
        guiStyle.nLineWidth = nLineWidth
        guiStyle.clrLineColor = clrLineColor
        guiStyle.bLabelVisible = True
        guiStyle.strLabelFont = "Arial"
        guiStyle.lFontSize = 100
        # 获取GUI显示数组
        # 十字GUI显示设置
        guiCross = GvVisionAssembly.GsScriptGuiCross()
        guiCross.sScriptGuiStyle = guiStyle
        guiCross.cross.SetX(Vec.GetX())
        guiCross.cross.SetY(Vec.GetY())

        guiArray.Add(guiCross)
        return guiCross


    # Vẽ một loạt dấu chữ thập (cross) từ mảng vector (hỗ trợ nhiều điểm cùng lúc)
    # self         : chính instance của lớp ScImageShow
    # Vec          : mảng/list các vector 2D (mỗi vector chứa x, y và góc xoay)
    # guiArray     : mảng ảnh để vẽ lên (buffer hiển thị)
    # clrLineColor : màu vẽ các cross (RGB, mặc định thường xanh lá)
    # nLineWidth   : độ dày nét vẽ của các cross
    def ImagechowCrossSc2Vec(self,guiArray, Sc2Vec, clrLineColor=[0, 255, 0], nLineWidth=1):
        # 设置GUI格式
        guiStyle = GvVisionAssembly.GsScriptGuiStyle()
        guiStyle.bVisible = True
        guiStyle.nLineStyle = 2
        guiStyle.nLineWidth = nLineWidth
        guiStyle.clrLineColor = clrLineColor
        guiStyle.bLabelVisible = True
        guiStyle.strLabelFont = "Arial"
        guiStyle.lFontSize = 100
        # 获取GUI显示数组
        # 十字GUI显示设置
        guiCross = GvVisionAssembly.GsScriptGuiCross()
        guiCross.sScriptGuiStyle = guiStyle
        for i in range(len(Sc2Vec)):
            Vec=Sc2Vec[i]
            guiCross.cross.SetX(Vec.GetX())
            guiCross.cross.SetY(Vec.GetY())
            guiArray.Add(guiCross)
        return guiCross



    # Vẽ dấu chữ thập (cross) theo vị trí + tư thế (pose) — có xoay góc
    # self         : chính instance của lớp ScImageShow
    # Cood         : tọa độ + góc xoay (pose) cần hiển thị (x, y, angle)
    # guiArray     : mảng ảnh để vẽ lên (buffer hiển thị)
    # size         : kích thước của dấu chữ thập (độ dài mỗi nhánh)
    # clrLineColor : màu vẽ (RGB, mặc định thường là xanh lá)
    # nLineWidth   : độ dày nét vẽ
    def ImagechowCrossCood(self, guiArray, Cood, size=10, clrLineColor=[0, 255, 0], nLineWidth=1):
        # 设置GUI格式
        guiStyle = GvVisionAssembly.GsScriptGuiStyle()
        guiStyle.bVisible = True
        guiStyle.nLineStyle = 2
        guiStyle.nLineWidth = nLineWidth
        guiStyle.clrLineColor = clrLineColor
        guiStyle.bLabelVisible = True
        guiStyle.strLabelFont = "Arial"
        guiStyle.lFontSize = 100
        # 获取GUI显示数组

        C = GvVisionAssembly.scCircle(GvVisionAssembly.sc2Vector(Cood.X, Cood.Y), size)
        L1 = GvVisionAssembly.scLine(GvVisionAssembly.sc2Vector(Cood.X, Cood.Y),  GvVisionAssembly.scRadian(Cood.D * math.pi / 180.0))
        L2 = GvVisionAssembly.scLine(GvVisionAssembly.sc2Vector(Cood.X, Cood.Y),  GvVisionAssembly.scRadian((Cood.D + 90) * math.pi / 180.0))

        P = GvVisionAssembly.InterSectLineCircle(L1, C)
        P1 = P.points[0]
        P2 = P.points[1]
        LineSeg1 = GvVisionAssembly.scLineSeg(P1, P2)
        guiArray.Add(self.imageShowLineSeg(self, LineSeg1, clrLineColor, nLineWidth))

        P = GvVisionAssembly.InterSectLineCircle(L2, C)
        P3 = P.points[0]
        P4 = P.points[1]
        LineSeg2 = GvVisionAssembly.scLineSeg(P3, P4)
        guiArray.Add(self.imageShowLineSeg(self, LineSeg2, clrLineColor, nLineWidth))

        return True


    # 显示圆弧
    # self 类本身ScImageShow
    # guiArray 显示数组
    # center 圆弧中心，scvector类型数据
    #radius 圆弧半径 double类型数据
    #startPhi 起始角度
    #spanPhi# 跨度角度
    # clrLineColor 显示颜色
    # nLineWidth 线宽
    def ImagechowArc(self, guiArray, center, radius=10.0, startPhi=90.0, spanPhi=90.0, clrLineColor=[0, 255, 0], nLineWidth=1):
        startPhiR = GvVisionAssembly.scRadian(math.pi * startPhi / 180.0)
        spanPhiR = GvVisionAssembly.scRadian(math.pi * spanPhi / 180.0)
        circularArc = GvVisionAssembly.scCircularArc(center, radius, startPhiR, spanPhiR)

        guistyle = GvVisionAssembly.GsScriptGuiStyle()
        guistyle.nLineWidth = nLineWidth
        guistyle.clrLineColor = clrLineColor

        ##创建圆弧Gui
        circularArc_gui = GvVisionAssembly.GsScriptGuiCircularArc()
        circularArc_gui.sScriptGuiStyle = guistyle
        circularArc_gui.circularArc = circularArc

        guiArray.Add(circularArc_gui)
        return True

    # 显示圆弧本身
    # self 类本身ScImageShow
    # Cood 位置姿态生成的位置（含角度）
    # guiArray 显示数组
    # size 尺寸大小
    # clrLineColor 显示颜色
    # nLineWidth 线宽
    def ImagechowArc(self, guiArray, arc,  clrLineColor=[0, 255, 0], nLineWidth=1,nLineStyle=0):
        circularArc = arc
        ##Gui风格
        guistyle = GvVisionAssembly.GsScriptGuiStyle()
        guistyle.nLineWidth = nLineWidth
        guistyle.clrLineColor = clrLineColor
        guistyle.nLineStyle=nLineStyle

        ##创建圆弧Gui
        circularArc_gui = GvVisionAssembly.GsScriptGuiCircularArc()
        circularArc_gui.sScriptGuiStyle = guistyle
        circularArc_gui.circularArc = circularArc

        ##将圆弧Gui添加到Gui数组中
        guiArray.Add(circularArc_gui)




    def GetArcBy3Pos(self,p1, p2, p3):
        midpos1 = GvVisionAssembly.sc2Vector((p1.GetX() + p2.GetX()) / 2.0, (p1.GetY() + p2.GetY()) / 2.0)
        vec1 = p2 - p1
        L1 = GvVisionAssembly.scLine(midpos1, GvVisionAssembly.sc2Vector((0 - vec1.GetY()), (vec1.GetX())))

        midpos2 = GvVisionAssembly.sc2Vector((p3.GetX() + p2.GetX()) / 2.0, (p3.GetY() + p2.GetY()) / 2.0)
        vec2 = p2 - p3
        L2 = GvVisionAssembly.scLine(midpos2, GvVisionAssembly.sc2Vector((0 - vec2.GetY()), (vec2.GetX())))

        centerpos = L1.Intersect(L2)[0]
        R = GvVisionAssembly.DistancePoint2Point(centerpos, p2).distance
        #print(centerpos.GetX(), centerpos.GetY(), R)

        vecstart = p1 - centerpos
        Lstart = GvVisionAssembly.scLine(centerpos, p1 - centerpos)
        Lmid = GvVisionAssembly.scLine(centerpos, p2 - centerpos)
        startangle = Lstart.GetRotation()
        startapan = GvVisionAssembly.scRadian(Lstart.GetAngle(Lmid).ToDouble() * 2)

        arc = GvVisionAssembly.scCircularArc(centerpos, R, startangle, startapan)
        return arc

    def ImageDrawGlueLine(self,Gluedata, P0, guiArray, dwith=1,bshowtext=False,bshowGlue=True):
        ncount = Gluedata.GetCurveCount()

        StartPos = GvVisionAssembly.sc2Vector(0, 0)
        MiddlePos = GvVisionAssembly.sc2Vector(0, 0)
        EndPos = GvVisionAssembly.sc2Vector(0, 0)
        GvVisionAssembly.GetCurveSegStartPoint(Gluedata, 0, StartPos)
        nowidth = int(dwith / 2)
        if nowidth < 1:
            nowidth = 1
        if bshowGlue:
            self.ImageShowLineSegVec(self, guiArray, P0, StartPos, [0, 255, 0], nowidth, 1)  # 两点显示线段

        for i in range(0, ncount):
            GvVisionAssembly.GetCurveSegStartPoint(Gluedata, i, StartPos)
            GvVisionAssembly.GetCurveSegEndPoint(Gluedata, i, EndPos)
            if bshowtext:
                if i!=0:
                    self.ImageShowTextPos(self, guiArray, StartPos, str(i-1), [0, 255, 0], 50)
                self.ImagechowCrossVec(self, guiArray, StartPos, [0, 255, 0], nowidth)
            bHit = GvVisionAssembly.GetCurveSegType(Gluedata, i)
            if bHit and bshowGlue:
                bArc = GvVisionAssembly.GetCurveSegIsArc(Gluedata, i)
                if bArc:
                    GvVisionAssembly.GetCurveSegMidPoint(Gluedata, i, MiddlePos)
                    self.ImagechowArc(self,guiArray,self.GetArcBy3Pos(self,StartPos,MiddlePos,EndPos),[0, 255, 0], dwith)
                else:
                    self.ImageShowLineSegVec(self, guiArray, StartPos, EndPos, [0, 255, 0],dwith)  # 两点显示线段
            elif not bHit and bshowGlue:
                bArc = GvVisionAssembly.GetCurveSegIsArc(Gluedata, i)
                if bArc:
                    GvVisionAssembly.GetCurveSegMidPoint(Gluedata, i, MiddlePos)
                    self.ImagechowArc(self, guiArray, self.GetArcBy3Pos(self, StartPos, MiddlePos, EndPos), [0, 255, 0],dwith,2)
                else:
                    self.ImageShowLineSegVec(self, guiArray, StartPos, EndPos, [0, 255, 0], nowidth, 1)  # 两点显示线段

    # Hiển thị một chuỗi dữ liệu
    # self: bản thân lớp ScImageShow
    # guiArray: mảng hiển thị
    # info: danh sách cần hiển thị
    # info là mảng 2 chiều
    # info=[[status],\           1 phần tử, về nguyên tắc chỉ hiển thị OK/NG, OK mặc định màu xanh lá / NG mặc định màu đỏ, dòng đầu chỉ hiển thị OK/NG
    # ["SN",SN],\                2 phần tử, phần tử đầu là tên, phần tử thứ hai là giá trị thực tế
    # ["Cavity",cavityN],\
    # ["Nozzle",NozzleN],\
    # [],\         dòng trống biểu thị dòng trắng
    # [],\
    # [],\
    # [],\
    # ["length","mm",0.5,0.1,0.8],\   5 phần tử, phần tử đầu là tên, thứ hai là đơn vị, thứ ba là giá trị thực tế, thứ tư là giá trị nhỏ nhất, thứ năm là giá trị lớn nhất
    # ["length2","mm",0.5,0.1,0.7],\
    # ["length3","mm",0.5,0.1,0.6],\
    # ["length2","mm",0.5,0.1,0.5],\
    # ["length2","mm",0.5,0.6,0.8],\
    # ["CT","ms",100,90,250]]
    # fontsizesize: kích thước chữ, mặc định là 50
    # màu NG là đỏ, OK là xanh lá

    def ListShow(self,guiArray, info, fontsize=50,PosX=0,PosY=0):
        # 获取 GUI 显示数组——重要初始化显示数组
        if (info[0][0] == "OK" or info[0][0] == "Ok" or info[0][0] == "ok"):
            rgb = [0, 255, 0]
        else:
            rgb = [255, 0, 0]
        self.ImageShowTextXY(self,guiArray, 50+PosX, round(0.5 * fontsize)+PosY, info[0][0], rgb, round(fontsize * 1.5))
        for i in range(1, len(info)):
            if len(info[i]) == 5:
                if (info[i][2] >= info[i][3] and info[i][2] <= info[i][4]):
                    rgb = [0, 255, 0]
                else:
                    rgb = [255, 0, 0]
                self.ImageShowTextXY(self,guiArray, 50+PosX, (i + 1) * fontsize+PosY,"{}: {:.3f}{} ({},{})".format(info[i][0], info[i][2], info[i][1],info[i][3], info[i][4]), rgb, fontsize)

            elif len(info[i]) == 4:
                if info[i][0] == "POS" or info[i][0] == "Pos":
                    rgb = [0, 255, 0]
                    self.ImageShowTextXY(self,guiArray, 50+PosX, (i + 1) * fontsize+PosY, "{}({:.2f},{:.2f},{:.2f})".format(info[i][0], info[i][1], info[i][2], info[i][3]), rgb,fontsize)
                else:
                    rgb = [0, 255, 0]
                    self.ImageShowTextXY(self,guiArray, 50+PosX, (i + 1) * fontsize+PosY,"{},{},{},{})".format(info[i][0], info[i][1], info[i][2], info[i][3]),rgb, fontsize)

            elif len(info[i]) == 3:
                if info[i][0] == "POS" or info[i][0] == "Pos":
                    rgb = [0, 255, 0]
                    self.ImageShowTextXY(self,guiArray, 50+PosX, (i + 1) * fontsize+PosY,"{}({:.2f},{:.2f})".format(info[i][0], info[i][1], info[i][2]),rgb, fontsize)
                elif info[i][2] == "OK" or info[i][2] == "Ok" or info[i][2] == "ok":
                    rgb = [0, 255, 0]
                    self.ImageShowTextXY(self,guiArray, 50+PosX, (i + 1) * fontsize+PosY, "{}:{}".format(info[i][0], info[i][1]),rgb, fontsize)
                elif  info[i][2] == "NG" or info[i][2] == "Ng" or info[i][2] == "ng":
                    rgb = [255, 0, 0]
                    self.ImageShowTextXY(self,guiArray, 50+PosX, (i + 1) * fontsize+PosY, "{}:{}".format(info[i][0], info[i][1]), rgb,fontsize)
                else:
                    rgb = [0, 255, 0]
                    self.ImageShowTextXY(self,guiArray, 50+PosX, (i + 1) * fontsize+PosY, "{}:{:.3f}{}".format(info[i][0], info[i][2], info[i][1]), rgb,fontsize)

            elif len(info[i]) == 2:
                rgb = [0, 255, 0]
                self.ImageShowTextXY(self,guiArray, 50+PosX, (i + 1) * fontsize+PosY,"{}: {}".format(info[i][0], info[i][1]), rgb, fontsize)

            elif len(info[i]) == 1:
                rgb = [0, 255, 0]
                self.ImageShowTextXY(self,guiArray, 50+PosX, (i + 1) * fontsize+PosY,"{}".format(info[i][0]), rgb, fontsize)

            elif len(info[i]) ==0:
                pass

            else:
                noteType = GvVisionAssembly.GeMsgReportType.eMRTError
                GvVisionAssembly.ReportMessage("超出显示范围 out of content", noteType, False)
                rgb = [255, 0, 0]
                self.ImageShowTextXY(self,guiArray, 50 + PosX, (i + 1) * fontsize+PosY, "超出显示范围 out of content", rgb, fontsize)

        if (len(info[0])>1):
            if (info[0][0] == "OK"):
                rgb = [0, 255, 0]
            else:
                rgb = [255, 0, 0]
            self.ImageShowTextXY(self,guiArray, 50+PosX, round((len(info)+1) * fontsize)+PosY, info[0][1], rgb, round(fontsize * 1.5))


    # Hiển thị thông tin watermark (chữ mờ)
    # self: bản thân lớp ScImageShow
    # guiArray: mảng hiển thị
    # StrInfo: thông tin watermark cần hiển thị, kiểu string
    # EngVer: phiên bản, kiểu string, dạng XX.XX (phiên bản lớn/nhỏ)
    # height: chiều cao ảnh, mặc định là 2048
    # fontsizesize: kích thước chữ, mặc định là 50
    # rgb = [200, 200, 200]: màu sắc, mặc định là trắng

    def MetaShow(self,guiArray, StrInfo, EngVer, height=2048, fontsize=50, rgb=[200, 200, 200]):
        info = StrInfo.split(",")
        Meta_Version = info[0]
        print(info[13])
        if Meta_Version == "0001":
            N = int(info[13]) + 6
            for i in range(0, int(info[13])):
                self.ImageShowTextXY(self, guiArray, 50, height - (N - i ) * fontsize, "{}".format(info[14 + i]),rgb, fontsize)
            self.ImageShowTextXY(self, guiArray, 50, height - (N + 1) * fontsize, "Station ID：{}".format(info[4]), rgb,fontsize)
        if Meta_Version == "0002":
            N = int(info[13]) + 7
            for i in range(0, int(info[13])):
                self.ImageShowTextXY(self, guiArray, 50, height - (N - i ) * fontsize, "{}".format(info[14 + i]),rgb, fontsize)
            self.ImageShowTextXY(self, guiArray, 50, height - (N+1) * fontsize, "Station ID：{}".format(info[4]), rgb,fontsize)
            self.ImageShowTextXY(self, guiArray, 50, height - (7) * fontsize, "Color：{}".format(info[14 + int(info[13])]), rgb, fontsize)
        self.ImageShowTextXY(self, guiArray, 50, height - (6) * fontsize, "Meta Version：{}".format(info[0]), rgb,fontsize)
        self.ImageShowTextXY(self, guiArray, 50, height - (5) * fontsize, "Gain：{:.3}".format(info[11]), rgb, fontsize)
        self.ImageShowTextXY(self, guiArray, 50, height - (4) * fontsize, "Exposure Time:{:.8} s".format(info[12]),rgb, fontsize)
        self.ImageShowTextXY(self, guiArray, 50, height - (3) * fontsize, "{}_{}".format(info[1], info[2]), rgb,fontsize)
        self.ImageShowTextXY(self, guiArray, 50, height - (2) * fontsize, "Version: {}".format(EngVer), rgb, fontsize)
