<<<<<<< HEAD
import sys
import math
# import numpy
from ScFoolProof import ScFoolProof

# sys.path.append(r'C:\Program Files\VISIONAssembly_x64')
import GvVisionAssembly


class ScShape(object):

    ##########################
    #####点阵中增加点
    ###########################
    # VectorVec 点阵数组
    # Pos 二维向量点
    # VectorVec 返回值 多点
    @staticmethod
    def ScShapePolylineAddPoint(VectorVec, Pos):
        VectorVec.append(Pos)
        return True

    ##########################
    #####点阵中增加圆弧段
    ###########################
    # VectorVec 点阵数组
    # centerpos 圆弧的圆心
    # R=50  半径，默认50
    # startAng=0.0  起始角度 默认0度
    # endAng 终点角度  默认90°
    # VectorVec 返回值 多点
    @staticmethod
    def ScShapePolylineAddArc(VectorVec, centerpos, R=50, startAng=0.0, endAng=90.0, dstep=0.1):
        if startAng <= endAng:
            for i in range(math.floor(startAng * 100), math.ceil(endAng * 100), math.ceil(100 * dstep)):
                VectorVec.append(GvVisionAssembly.sc2Vector(R * math.cos(i * math.pi / 18000) + centerpos.GetX(),
                                                            R * math.sin(i * math.pi / 18000) + centerpos.GetY()))

        else:
            for i in range(math.floor(startAng * 100), math.ceil(endAng * 100), -math.ceil(100 * dstep)):
                VectorVec.append(GvVisionAssembly.sc2Vector(R * math.cos(i * math.pi / 18000) + centerpos.GetX(),
                                                            R * math.sin(i * math.pi / 18000) + centerpos.GetY()))
        return VectorVec

    ##########################
    #####利用点阵生成多边形曲线
    ###########################
    # VectorVec 点阵数组
    # polyline 待生成的多边形曲线
    # 返回值 polyline 多边形曲线
    @staticmethod
    def ScShapePolyline(VectorVec, polyline):
        polyline = GvVisionAssembly.scPolyline(VectorVec, True)
        return polyline

    ##########################
    #####点阵结果偏移
    ###########################
    # VectorVec 点阵数组
    # transx=0,transy=0,transd=0  新的位置偏移
    # 返回值 VectorVec  返回多点的位置
    @staticmethod
    def ScShapeTransPostion(VectorVec, transx=0, transy=0, transd=0):
        # print(len(VectorVec))
        VectorVecRet = GvVisionAssembly.sc2VectorVec()
        posRet = GvVisionAssembly.sc2Vector()
        for i in range(0, len(VectorVec)):
            pos = VectorVec[i]
            posRet.SetX(
                pos.GetX() * math.cos(transd * math.pi / 180) - pos.GetY() * math.sin(transd * math.pi / 180) + transx)
            posRet.SetY(
                pos.GetX() * math.sin(transd * math.pi / 180) + pos.GetY() * math.cos(transd * math.pi / 180) + transy)
            VectorVecRet.append(posRet)

        for i in range(0, len(VectorVec)):
            pos = VectorVec[i]
            VectorVec[i].SetX(VectorVecRet[i].GetX())
            VectorVec[i].SetY(VectorVecRet[i].GetY())

        return VectorVec

    ##########################
    #####找线结果偏移工具，偏移出一个找线结果
    ###########################
    # line0 找线基准位置
    # line1 偏移后的找线位置（定义在源文件中，在函数中被修改）
    # Sc2XformLinear 二维线性变换偏移值
    # 返回值 VectorVec  返回多点的位置
    @staticmethod
    def ScShapeTransPostionLinear(VectorVec, Sc2XformLinear):
        # print(len(VectorVec))
        VectorVecRet = GvVisionAssembly.sc2VectorVec()
        posRet = GvVisionAssembly.sc2Vector()
        a00 = Sc2XformLinear.GetMatrix().GetElement(0, 0)
        a01 = Sc2XformLinear.GetMatrix().GetElement(0, 1)
        a10 = Sc2XformLinear.GetMatrix().GetElement(1, 0)
        a11 = Sc2XformLinear.GetMatrix().GetElement(1, 1)
        TX = Sc2XformLinear.GetTrans().GetX()
        TY = Sc2XformLinear.GetTrans().GetY()

        for i in range(0, len(VectorVec)):
            pos = VectorVec[i]
            posRet.SetX(pos.GetX() * a00 + pos.GetY() * a01 + TX)
            posRet.SetY(pos.GetX() * a10 + pos.GetY() * a11 + TY)
            VectorVecRet.append(posRet)

        for i in range(0, len(VectorVec)):
            pos = VectorVec[i]
            VectorVec[i].SetX(VectorVecRet[i].GetX())
            VectorVec[i].SetY(VectorVecRet[i].GetY())

        return VectorVec

    ##########################
    #####找线结果偏移工具，偏移出一个找线结果
    ###########################
    # line0 找线基准位置
    # line1 偏移后的找线位置（定义在源文件中，在函数中被修改）
    # doffset 偏移值，int类型，可正可负
    # 返回值 line1  返回找线结果
    @staticmethod
    def ScShapeLineOffset(line0, line1, doffset):
        pos = line0.GetPos()
        dangle = line0.GetRotation().ToDouble() * 180.0 / math.pi
        rad = line0.GetRotation()
        print(dangle)
        pos2 = GvVisionAssembly.sc2Vector()

        pos2.SetX(pos.GetX() + doffset * math.cos(line0.GetRotation().ToDouble() + math.pi / 2.0))
        pos2.SetY(pos.GetY() + doffset * math.sin(line0.GetRotation().ToDouble() + math.pi / 2.0))

        line1.SetPos(pos2)
        line1.SetRotation(rad)

        return line1

        ##########################
        #####找线结果偏移工具，偏移出一个找线结果
        ###########################
        # line0 找线基准位置
        # line1 偏移后的找线位置（定义在源文件中，在函数中被修改）
        # doffset 偏移值，int类型，可正可负
        # 返回值 line1  返回找线结果

    @staticmethod
    def ScShapeffsetLineO(line0, doffset):
        line1 = GvVisionAssembly.scLine()
        pos = line0.GetPos()
        dangle = line0.GetRotation().ToDouble() * 180.0 / math.pi
        rad = line0.GetRotation()
        print(dangle)
        pos2 = GvVisionAssembly.sc2Vector()

        pos2.SetX(pos.GetX() + doffset * math.cos(line0.GetRotation().ToDouble() + math.pi / 2.0))
        pos2.SetY(pos.GetY() + doffset * math.sin(line0.GetRotation().ToDouble() + math.pi / 2.0))

        line1.SetPos(pos2)
        line1.SetRotation(rad)

        return line1

    ##########################
    #####找线工具检测区域设置
    ###########################
    # 一般用来对找圆工具的圆环ROI区域做位置变换
    # GuiFindLineEx 获取找圆工具的 “查找区域”
    # transx=0,transy=0,transd=0 位置偏移值
    # 返回值 GuiFindLineEx  找线工具查找区域
    @staticmethod
    def ScShapeTranslineSearchRec(GuiFindLineEx, transx=0, transy=0, transd=0):
        # print(len(VectorVec))
        AffineRec = GuiFindLineEx.GetAffineRect()
        AffineRec.SetCenter(GvVisionAssembly.sc2Vector(transx, transy))
        AffineRec.SetXRotation(GvVisionAssembly.scRadian(transd * math.pi / 180.0))
        GuiFindLineEx.SetAffineRect(AffineRec)
        return GuiFindLineEx

    ##########################
    #####找圆工具检测区域设置
    ###########################
    # 一般用来对找圆工具的圆环ROI区域做位置变换
    # GuiFindCircleEx 获取找圆工具的 “查找区域”
    # center sc2vector类型，表示远心坐标
    # startPhi=0.0 起始角度
    # spanPhi=360。0  默认转角
    # stdRadius=0，半径值，默认为0的情况下为原始的半径（不改变），设定不为0时，按照
    # RadialScale=0.0，径向比例
    # 返回值 GuiFindCircleEx  圆环形查找区域
    @staticmethod
    def ScShapeTransCircleSearchAnn(GuiFindCircleEx, center, startPhi=0.0, spanPhi=360.0, stdRadius=0, RadialScale=0.0):
        # print(len(VectorVec))
        AnnulusSection = GuiFindCircleEx.GetAnnulusSection()
        AnnulusSection.SetCenter(center)
        AnnulusSection.SetStartPhi(GvVisionAssembly.scRadian(startPhi * math.pi / 180.0))
        AnnulusSection.SetSpanPhi(GvVisionAssembly.scRadian(spanPhi * math.pi / 180.0))
        if not stdRadius == 0:
            AnnulusSection.SetRadius(stdRadius)
        if not RadialScale == 0.0:
            AnnulusSection.SetRadialScale(RadialScale)

        GuiFindCircleEx.SetAnnulusSection(AnnulusSection)
        return GuiFindCircleEx

    ##########################
    #####blob工具或者检测工具的检测区域设置
    ###########################

    # 一般用来对blob工具的圆环ROI区域做位置变换
    # Annulus 获取blob工具的 “公开圆环形ROI”
    # center sc2vector类型，表示远心坐标
    # stdRadius=0，半径值，默认为0的情况下为原始的半径（不改变），设定不为0时，按照
    # RadialScale=0.0，径向比例
    # 返回值 Annulus  圆环形区域
    @staticmethod
    def ScShapeTransAnnulus(Annulus, center, stdRadius=0, RadialScale=0.0):
        # print(len(VectorVec))
        Annulus.SetCenter(center)
        if not stdRadius == 0:
            Annulus.SetRadius(stdRadius)
        if not RadialScale == 0.0:
            Annulus.SetRadialScale(RadialScale)
        return Annulus

    # 一般用来对blob工具的圆ROI区域做位置变换
    # Circle 获取blob工具的 “公开圆形ROI”
    # center sc2vector类型，表示远心坐标
    # stdRadius=0，矩形长宽值，默认为0的情况下为原始的半径（不改变），设定不为0时，按照
    # 返回值 Circle  圆形区域
    @staticmethod
    def ScShapeTransCircle(Circle, center, stdRadius=0):
        # print(len(VectorVec))
        Circle.SetCenter(center)
        if not stdRadius == 0:
            Circle.SetRadius(stdRadius)

        return Circle

    # 一般用来对blob工具的矩形ROI区域做位置变换
    # Rec 获取blob工具的 “公开矩形ROI”
    # center sc2vector类型，表示仿射矩形中点坐标
    # dw=0,dh=0，矩形长宽值，默认为0的情况下为原始的长宽（不改变），设定不为0时，按照
    # 返回值 Rec  矩形区域
    @staticmethod
    def ScShapeTransRec(Rec, center, dw=0, dh=0):
        # print(len(VectorVec))
        # Circle.SetCenter( center )
        W = Rec.GetWidth()
        H = Rec.GetHeight()
        if not dw == 0:
            W = dw
        if not dh == 0:
            H = dh
        Rec.Set(center.GetX() - W / 2.0, center.GetY() - H / 2.0, W, H)
        return Rec

    # 一般用来对blob工具的仿射矩形ROI区域做位置变换
    # Rec 获取blob工具的 “仿射矩形ROI”
    # center sc2vector类型，表示仿射矩形中点坐标
    # # transd 需要旋转的角度，默认为0
    # dw=0,dh=0，矩形长宽值，默认为0的情况下为原始的长宽（不改变），设定不为0时，按照
    # 返回值 Rec  仿射矩形区域
    @staticmethod
    def ScShapeTransAffinRec(Rec, center, transd=0.0, dw=0, dh=0):
        # print(len(VectorVec))
        # Circle.SetCenter( center )
        W = Rec.GetXLength()
        H = Rec.GetYLength()
        Rec.SetCenter(center)
        Rec.SetXRotation(GvVisionAssembly.scRadian(transd * math.pi / 180.0))
        if not dw == 0:
            W = dw
        if not dh == 0:
            H = dh
        Rec.SetXLength(W)
        Rec.SetYLength(H)
        return Rec

    # 一般用来对blob工具的多边形ROI区域做位置变换
    # self  ScShape类本身
    # Polyline 获取blob工具的 “公开多边形ROI”
    # VectorVec 生成的标准检测区域的点阵
    # transx # transy # transd 需要偏移的特征点的位置坐标，相对于标准检测区域
    # 返回值 Polyline  多边形ROI 区域
    def ScShapeTransPolyline(self, Polyline, VectorVec, transx=0, transy=0, transd=0):
        # print(len(VectorVec))
        # Circle.SetCenter( center )
        VectorVec2 = GvVisionAssembly.sc2VectorVec()
        VectorVec2 = VectorVec
        self.ScShapeTransPostion(VectorVec2, transx, transy, transd)
        Polyline = GvVisionAssembly.scPolyline(VectorVec2, True)

        return Polyline

    # 两条线交点  含防呆
    # line0 输入线1  scLine类型 线1  坐标的角度与线1 的角度相同
    # line1 输入线2  scLine类型 线2
    # GcCoodPos  GcCoodPos类型，本地定义，
    # bFoolProof BOOL类型  是否防呆  默认Flase
    # stdAngle 标准设定角度   正常角度0-180°  默认90.0°
    # AngleLimit 标准设定公差  正常角度0-180°  默认1.0°
    # strlabel 标识 默认"L1&L2"
    # 返回值 Bool类型  True，表示正常（含不防呆），False 表示异常
    @staticmethod
    def ScShapeLineCross(line0, line1, GcCoodPos, bFoolProof=False, stdAngle=90, AngleLimit=1, strlabel="L1&L2"):
        pos = line0.Intersect(line1)[0]
        GcCoodPos.X = pos.GetX()
        GcCoodPos.Y = pos.GetY()
        dangle = line0.GetRotation().SignedNormMod180().ToDouble() * 180.0 / math.pi
        if math.fabs(dangle) < 45:
            GcCoodPos.D = dangle
        else:
            GcCoodPos.D = line0.GetRotation().NormMod180().ToDouble() * 180.0 / math.pi

        if not bFoolProof:
            return True
        else:
            return ScFoolProof.ScFoolProofline2(line0, line1, stdAngle, AngleLimit, strlabel)

    # 两横两纵四条边的交点
    # self  ScShape类本身
    # lineup 输入线1  scLine类型 上横线
    # linedn 输入线2  scLine类型 下横线
    # linelt 输入线3  scLine类型 左竖线
    # linert 输入线4  scLine类型 右竖线
    # GcCoodPosVec  GcCoodPos类型数组，本地定义，
    # bFoolProof BOOL类型  是否防呆  默认Flase

    # 返回值 errorcode  int类型  1，表示正常（含不防呆），21左上角异常，22右下角异常，23右上角异常，24左下角异常
    def ScShapeLineCross4Lines(self, lineup, linedn, linelt, linert, GcCoodPosVec, bFoolProof=False, dangleLimit=1):
        bul = self.ScShapeLineCross(lineup, linelt, GcCoodPosVec[0], bFoolProof, 90, dangleLimit, "左上交线")
        bdr = self.ScShapeLineCross(linedn, linert, GcCoodPosVec[1], bFoolProof, 90, dangleLimit, "右下交线")
        bur = self.ScShapeLineCross(lineup, linert, GcCoodPosVec[2], bFoolProof, 90, dangleLimit, "右上交线")
        bdl = self.ScShapeLineCross(linedn, linelt, GcCoodPosVec[3], bFoolProof, 90, dangleLimit, "左下交线")

        if len(GcCoodPosVec) > 4:
            GcCoodPosVec[4].X = (GcCoodPosVec[0].X + GcCoodPosVec[1].X + GcCoodPosVec[2].X + GcCoodPosVec[3].X) / 4.0
            GcCoodPosVec[4].Y = (GcCoodPosVec[0].Y + GcCoodPosVec[1].Y + GcCoodPosVec[2].Y + GcCoodPosVec[3].Y) / 4.0
            GcCoodPosVec[4].D = (lineup.GetRotation().ToDouble() * 180.0 / math.pi + linedn.GetRotation().ToDouble() * 180.0 / math.pi) / 2.0

        if not bFoolProof:
            return 1
        elif bul and bdr and bur and bdl:
            return 1
        elif not bul:
            return 21
        elif not bdr:
            return 22
        elif not bur:
            return 23
        elif not bdl:
            return 24
        else:
            return 25

    # 获取直线的角度
    # self  ScShape类本身
    # line  输入直线
    # dAngle 直线预设角度，比如返回一个90度附近的角度（固定取值90/-90/0/180/270）其余返回本值
    # 返回值 resAngle  double类型，返回角度
    #
    def ScShapeLineGetAngle(self, line, dAngle=0):

        resAngle = 0
        if dAngle == 0:
            resAngle = line.GetRotation().SignedNormMod180().ToDouble() * 180.0 / math.pi
        elif dAngle == 90:
            resAngle = line.GetRotation().NormMod180().ToDouble() * 180.0 / math.pi
        elif dAngle == 180:
            resAngle = line.GetRotation().SignedNormMod180().ToDouble() * 180.0 / math.pi + 180.0
        elif dAngle == 270:
            resAngle = line.GetRotation().NormMod180().ToDouble() * 180.0 / math.pi + 180.0
        elif dAngle == -90:
            resAngle = line.GetRotation().NormMod180().ToDouble() * 180.0 / math.pi - 180.0
        else:
            resAngle = line.GetRotation().Norm().ToDouble() * 180.0 / math.pi

        return resAngle

    # 把任意一个点,在图像坐标系下旋转到另一个点位置
    # VecP 图像上任意一点 scvector 类型
    # dangle 角度值。±180.0
    # Veccenter scvector 类型
    def ScRotateVector(self, VecP, dangle=0, Veccenter=GvVisionAssembly.sc2Vector(0, 0)):
        ResVec = GvVisionAssembly.sc2Vector(0, 0)
        arcangle = dangle * math.pi / 180.0
        P1X = VecP.GetX()
        P1Y = VecP.GetY()
        P0X = Veccenter.GetX()
        P0Y = Veccenter.GetY()
        cosA = math.cos(arcangle)
        sinA = math.sin(arcangle)

        ResVec.SetX((P1X - P0X) * cosA - (P1Y - P0Y) * sinA + P0X)
        ResVec.SetY((P1X - P0X) * sinA + (P1Y - P0Y) * cosA + P0Y)
        return ResVec

    # 计算点数组到直线的最大距离
    # Vec 数组点
    # benchline 基准线
    # bonesidetype 测量类型
    # bonesidetype=0,检测绝对位置上下左右不分
    # bonesidetype=1,左右检测右边
    # bonesidetype=2,左右检测左边
    # bonesidetype=3,上下检测下边
    # bonesidetype=4,上下检测上边
    # bfoolproof=False，是否防呆，默认不防呆
    # dLimit=10.0 防呆spec
    # 返回值【最大距离，最大距离对应的序号，最大距离是否满足要求，【【变换前点坐标，是否满足距离范围】，【】，……】】

    def ScaxDisVecToLine(self, Vec, benchline, bonesidetype=1, bfoolproof=False, dLimit=10.0):
        maxdistance = 0
        maxdistanceindex = 0
        maxdisfalg = True
        dis = 0
        res = []
        angle = 0
        pos = benchline.GetPos()
        if bonesidetype == 0 or bonesidetype == 1 or bonesidetype == 2:
            angle = self.ScShapeLineGetAngle(self, benchline, 90)
            for i in range(len(Vec)):
                respos = self.ScRotateVector(self, Vec[i], 90 - angle, pos)
                if bonesidetype == 0:
                    dis = math.fabs(respos.GetX() - pos.GetX())
                elif bonesidetype == 1:
                    dis = respos.GetX() - pos.GetX()
                elif bonesidetype == 2:
                    dis = pos.GetX() - respos.GetX()

                if bfoolproof and dis > dLimit:
                    res.append([Vec[i], False])
                else:
                    res.append([Vec[i], True])

                if dis > maxdistance:
                    maxdistance = dis
                    maxdistanceindex = i
                    if bfoolproof and dis > dLimit:
                        maxdisfalg = False
        else:

            angle = self.ScShapeLineGetAngle(self, benchline, 0)
            for i in range(len(Vec)):
                respos = self.ScRotateVector(self, Vec[i], 0 - angle, pos)
                if bonesidetype == 3:
                    dis = respos.GetY() - pos.GetY()
                else:
                    dis = pos.GetY() - respos.GetY()

                if bfoolproof and dis > dLimit:
                    res.append([Vec[i], False])
                else:
                    res.append([Vec[i], True])

                if dis > maxdistance:
                    maxdistance = dis
                    maxdistanceindex = i
                    if bfoolproof and dis > dLimit:
                        maxdisfalg = False

        return [maxdistance, maxdistanceindex, maxdisfalg, res]

    # 显示一个点到一条直线的距离的线段
    # VecP 点scvector类型
    # benchline 基准线 Sclinel类型
    # 返回值 SclineSeg 线段类型
    def ScDisPointToLine(self, VecP, benchline):
        angle = ScShape.ScShapeLineGetAngle(self, benchline, 0)
        rot = GvVisionAssembly.scRadian((90 - angle) * math.pi / 180.0)
        lineVer = GvVisionAssembly.scLine(VecP, rot)
        P2 = lineVer.Intersect(benchline)[0]

        return GvVisionAssembly.scLineSeg(VecP, P2)

    # 查找一个矩形的中心
    # 返回值 Scvector类型
    def ScGetRectCenter(self, rec):
        x_min = rec.GetUL().GetX()
        y_min = rec.GetUL().GetY()
        x_max = rec.GetLR().GetX()
        y_max = rec.GetLL().GetY()
        x_center = (x_max + x_min) / 2
        y_center = (y_max + y_min) / 2
        return GvVisionAssembly.sc2Vector(x_center, y_center)

    # 查找一个放射矩形的中心
    # 返回值 Scvector类型
    def ScGetAffRectCenter(self, rec):
        x_min = rec.GetUL().GetX()
        y_min = rec.GetUL().GetY()
        x_max = rec.GetLR().GetX()
        y_max = rec.GetLL().GetY()
        x_center = (x_max + x_min) / 2
        y_center = (y_max + y_min) / 2
        return GvVisionAssembly.sc2Vector(x_center, y_center)

    # 获取两个向量点之间的距离
    # 返回值 double 类型
    def ScGetDisofVec(self, Vector1, Vector2):
        distance = math.sqrt(pow((Vector1.GetX() - Vector2.GetX()), 2) + pow((Vector1.GetY() - Vector2.GetY()), 2))
        return distance

    # 过滤掉靠的比较近的结果
    # 返回值 list 类型
    def ScResultfilter(self, center_list, new_center_list, distance_threthold=100):
        delete_list_all = []
        for i, center1 in enumerate(center_list):
            if i not in delete_list_all:
                delete_list = []
                delete_list.append(i)
                for j, center2 in enumerate(center_list):
                    if j > i and j not in delete_list_all:
                        distance = self.ScGetDisofVec(self, center1, center2)
                        if distance < distance_threthold:
                            delete_list.append(j)
                            delete_list_all.append(j)
                temp_center_x = 0
                temp_center_y = 0
                idx = 0
                for idx, center_num in enumerate(delete_list):
                    temp_center_x += center_list[center_num].GetX()
                    temp_center_y += center_list[center_num].GetY()
                mean_x = temp_center_x / (idx + 1)
                mean_y = temp_center_y / (idx + 1)

                new_center_list.append(GvVisionAssembly.sc2Vector(mean_x, mean_y))

        return new_center_list

    # 获取子图区域
    def ScGetsubImagRec(self, new_center_list, imgls, window=256, rigionlimit=[0, 0, 2500, 2500], height=5100,
                        width=5100):
        dx_min = rigionlimit[0]
        dy_min = rigionlimit[1]
        dx_max = rigionlimit[2]
        dy_max = rigionlimit[3]
        cut_x = 0
        cut_y = 0
        for center in new_center_list:
            cut_x_min = max(center.GetX() - window / 2 + cut_x, 1)  # 超出边界限制
            cut_y_min = max(center.GetY() - window / 2 + cut_y, 1)
            cut_x_max = min(center.GetX() + window / 2 + cut_x, width)
            cut_y_max = min(center.GetY() + window / 2 + cut_y, height)
            if cut_x_max == width:
                cut_x_min = cut_x_max - window
            if cut_y_max == height:
                cut_y_min = cut_y_max - window
            cut_x_center = center.GetX() + cut_x
            cut_y_center = center.GetY() + cut_y
            print(cut_x_center, cut_y_center)
            if dx_min < cut_x_center < dx_max and dy_min < cut_y_center < dy_max:
                roi_rect = GvVisionAssembly.scRect(cut_x_min, cut_y_min, window, window)  # 左上角坐标+宽高
                imgls.append(roi_rect)

    # 判断矩形结果中心是否在另一个矩形区域内
    def ScIsReccenterInRec(self, rec1, rec2):
        PCenter = self.ScGetRectCenter(self, rec1)
        if rec2.GetUL().GetX() < PCenter.GetX() < rec2.GetLR().GetX() and rec2.GetUL().GetY() < PCenter.GetY() < rec2.GetLR().GetY():
            return True
        else:
            return False

    def GetRandAngle(self, p1, p2):
        L1 = GvVisionAssembly.scLine(p1, p2 - p1)
        angle = L1.GetRotation().Norm().ToDouble()
        R = GvVisionAssembly.DistancePoint2Point(p1, p2).distance
        res = GvVisionAssembly.sc2Vector(R, angle)
        return res

    def GetOriginalPos(self, stdPos, vec):
        X = vec.GetX() * math.cos(vec.GetY())
        Y = vec.GetX() * math.sin(vec.GetY())
        res = GvVisionAssembly.sc2Vector(X, Y) + stdPos
        return res

    def GetP2Vec(self, pos, VecL, VecU, index):
        minIndex = 0
        startU = index - 20
        res = GvVisionAssembly.sc2Vector(0, 0)

        if startU < 0:
            startU = 0

        endU = index + 20
        if endU > len(VecU):
            endU = len(VecU)

        endL = index + 20
        if endL > len(VecL):
            endL = len(VecL)

        minium = 999.99
        minIndex = 0
        # print(startU,endL,endU)
        for i in range(startU, endL, 1):
            dtempR = abs(pos.GetY() - VecL[i].GetY())
            if minium > dtempR:
                minium = dtempR
                minIndex = i
        if pos.GetX() < VecL[minIndex].GetX():
            res.SetX(1)
            return res

        minium = 999.99
        minIndex = 0
        for i in range(startU, endU, 1):
            dtempR = abs(pos.GetY() - VecU[i].GetY())
            if minium > dtempR:
                minium = dtempR
                minIndex = i
        if pos.GetX() > VecU[minIndex].GetX():
            res.SetY(1)
            return res
        return res

    def IsPonitInRect(self, PT, Rect):
        Result = False
        if PT.GetX() > Rect.GetUL().GetX() and PT.GetY() > Rect.GetUL().GetY() and PT.GetX() < Rect.GetLR().GetX() and PT.GetY() < Rect.GetLR().GetY():
            Result = True
        else:
            Result = False
=======
import sys
import math
# import numpy
from ScFoolProof import ScFoolProof

# sys.path.append(r'C:\Program Files\VISIONAssembly_x64')
import GvVisionAssembly


class ScShape(object):

    ##########################
    #####点阵中增加点
    ###########################
    # VectorVec 点阵数组
    # Pos 二维向量点
    # VectorVec 返回值 多点
    @staticmethod
    def ScShapePolylineAddPoint(VectorVec, Pos):
        VectorVec.append(Pos)
        return True

    ##########################
    #####点阵中增加圆弧段
    ###########################
    # VectorVec 点阵数组
    # centerpos 圆弧的圆心
    # R=50  半径，默认50
    # startAng=0.0  起始角度 默认0度
    # endAng 终点角度  默认90°
    # VectorVec 返回值 多点
    @staticmethod
    def ScShapePolylineAddArc(VectorVec, centerpos, R=50, startAng=0.0, endAng=90.0, dstep=0.1):
        if startAng <= endAng:
            for i in range(math.floor(startAng * 100), math.ceil(endAng * 100), math.ceil(100 * dstep)):
                VectorVec.append(GvVisionAssembly.sc2Vector(R * math.cos(i * math.pi / 18000) + centerpos.GetX(),
                                                            R * math.sin(i * math.pi / 18000) + centerpos.GetY()))

        else:
            for i in range(math.floor(startAng * 100), math.ceil(endAng * 100), -math.ceil(100 * dstep)):
                VectorVec.append(GvVisionAssembly.sc2Vector(R * math.cos(i * math.pi / 18000) + centerpos.GetX(),
                                                            R * math.sin(i * math.pi / 18000) + centerpos.GetY()))
        return VectorVec

    ##########################
    #####利用点阵生成多边形曲线
    ###########################
    # VectorVec 点阵数组
    # polyline 待生成的多边形曲线
    # 返回值 polyline 多边形曲线
    @staticmethod
    def ScShapePolyline(VectorVec, polyline):
        polyline = GvVisionAssembly.scPolyline(VectorVec, True)
        return polyline

    ##########################
    #####点阵结果偏移
    ###########################
    # VectorVec 点阵数组
    # transx=0,transy=0,transd=0  新的位置偏移
    # 返回值 VectorVec  返回多点的位置
    @staticmethod
    def ScShapeTransPostion(VectorVec, transx=0, transy=0, transd=0):
        # print(len(VectorVec))
        VectorVecRet = GvVisionAssembly.sc2VectorVec()
        posRet = GvVisionAssembly.sc2Vector()
        for i in range(0, len(VectorVec)):
            pos = VectorVec[i]
            posRet.SetX(
                pos.GetX() * math.cos(transd * math.pi / 180) - pos.GetY() * math.sin(transd * math.pi / 180) + transx)
            posRet.SetY(
                pos.GetX() * math.sin(transd * math.pi / 180) + pos.GetY() * math.cos(transd * math.pi / 180) + transy)
            VectorVecRet.append(posRet)

        for i in range(0, len(VectorVec)):
            pos = VectorVec[i]
            VectorVec[i].SetX(VectorVecRet[i].GetX())
            VectorVec[i].SetY(VectorVecRet[i].GetY())

        return VectorVec

    ##########################
    #####找线结果偏移工具，偏移出一个找线结果
    ###########################
    # line0 找线基准位置
    # line1 偏移后的找线位置（定义在源文件中，在函数中被修改）
    # Sc2XformLinear 二维线性变换偏移值
    # 返回值 VectorVec  返回多点的位置
    @staticmethod
    def ScShapeTransPostionLinear(VectorVec, Sc2XformLinear):
        # print(len(VectorVec))
        VectorVecRet = GvVisionAssembly.sc2VectorVec()
        posRet = GvVisionAssembly.sc2Vector()
        a00 = Sc2XformLinear.GetMatrix().GetElement(0, 0)
        a01 = Sc2XformLinear.GetMatrix().GetElement(0, 1)
        a10 = Sc2XformLinear.GetMatrix().GetElement(1, 0)
        a11 = Sc2XformLinear.GetMatrix().GetElement(1, 1)
        TX = Sc2XformLinear.GetTrans().GetX()
        TY = Sc2XformLinear.GetTrans().GetY()

        for i in range(0, len(VectorVec)):
            pos = VectorVec[i]
            posRet.SetX(pos.GetX() * a00 + pos.GetY() * a01 + TX)
            posRet.SetY(pos.GetX() * a10 + pos.GetY() * a11 + TY)
            VectorVecRet.append(posRet)

        for i in range(0, len(VectorVec)):
            pos = VectorVec[i]
            VectorVec[i].SetX(VectorVecRet[i].GetX())
            VectorVec[i].SetY(VectorVecRet[i].GetY())

        return VectorVec

    ##########################
    #####找线结果偏移工具，偏移出一个找线结果
    ###########################
    # line0 找线基准位置
    # line1 偏移后的找线位置（定义在源文件中，在函数中被修改）
    # doffset 偏移值，int类型，可正可负
    # 返回值 line1  返回找线结果
    @staticmethod
    def ScShapeLineOffset(line0, line1, doffset):
        pos = line0.GetPos()
        dangle = line0.GetRotation().ToDouble() * 180.0 / math.pi
        rad = line0.GetRotation()
        print(dangle)
        pos2 = GvVisionAssembly.sc2Vector()

        pos2.SetX(pos.GetX() + doffset * math.cos(line0.GetRotation().ToDouble() + math.pi / 2.0))
        pos2.SetY(pos.GetY() + doffset * math.sin(line0.GetRotation().ToDouble() + math.pi / 2.0))

        line1.SetPos(pos2)
        line1.SetRotation(rad)

        return line1

        ##########################
        #####找线结果偏移工具，偏移出一个找线结果
        ###########################
        # line0 找线基准位置
        # line1 偏移后的找线位置（定义在源文件中，在函数中被修改）
        # doffset 偏移值，int类型，可正可负
        # 返回值 line1  返回找线结果

    @staticmethod
    def ScShapeffsetLineO(line0, doffset):
        line1 = GvVisionAssembly.scLine()
        pos = line0.GetPos()
        dangle = line0.GetRotation().ToDouble() * 180.0 / math.pi
        rad = line0.GetRotation()
        print(dangle)
        pos2 = GvVisionAssembly.sc2Vector()

        pos2.SetX(pos.GetX() + doffset * math.cos(line0.GetRotation().ToDouble() + math.pi / 2.0))
        pos2.SetY(pos.GetY() + doffset * math.sin(line0.GetRotation().ToDouble() + math.pi / 2.0))

        line1.SetPos(pos2)
        line1.SetRotation(rad)

        return line1

    ##########################
    #####找线工具检测区域设置
    ###########################
    # 一般用来对找圆工具的圆环ROI区域做位置变换
    # GuiFindLineEx 获取找圆工具的 “查找区域”
    # transx=0,transy=0,transd=0 位置偏移值
    # 返回值 GuiFindLineEx  找线工具查找区域
    @staticmethod
    def ScShapeTranslineSearchRec(GuiFindLineEx, transx=0, transy=0, transd=0):
        # print(len(VectorVec))
        AffineRec = GuiFindLineEx.GetAffineRect()
        AffineRec.SetCenter(GvVisionAssembly.sc2Vector(transx, transy))
        AffineRec.SetXRotation(GvVisionAssembly.scRadian(transd * math.pi / 180.0))
        GuiFindLineEx.SetAffineRect(AffineRec)
        return GuiFindLineEx

    ##########################
    #####找圆工具检测区域设置
    ###########################
    # 一般用来对找圆工具的圆环ROI区域做位置变换
    # GuiFindCircleEx 获取找圆工具的 “查找区域”
    # center sc2vector类型，表示远心坐标
    # startPhi=0.0 起始角度
    # spanPhi=360。0  默认转角
    # stdRadius=0，半径值，默认为0的情况下为原始的半径（不改变），设定不为0时，按照
    # RadialScale=0.0，径向比例
    # 返回值 GuiFindCircleEx  圆环形查找区域
    @staticmethod
    def ScShapeTransCircleSearchAnn(GuiFindCircleEx, center, startPhi=0.0, spanPhi=360.0, stdRadius=0, RadialScale=0.0):
        # print(len(VectorVec))
        AnnulusSection = GuiFindCircleEx.GetAnnulusSection()
        AnnulusSection.SetCenter(center)
        AnnulusSection.SetStartPhi(GvVisionAssembly.scRadian(startPhi * math.pi / 180.0))
        AnnulusSection.SetSpanPhi(GvVisionAssembly.scRadian(spanPhi * math.pi / 180.0))
        if not stdRadius == 0:
            AnnulusSection.SetRadius(stdRadius)
        if not RadialScale == 0.0:
            AnnulusSection.SetRadialScale(RadialScale)

        GuiFindCircleEx.SetAnnulusSection(AnnulusSection)
        return GuiFindCircleEx

    ##########################
    #####blob工具或者检测工具的检测区域设置
    ###########################

    # 一般用来对blob工具的圆环ROI区域做位置变换
    # Annulus 获取blob工具的 “公开圆环形ROI”
    # center sc2vector类型，表示远心坐标
    # stdRadius=0，半径值，默认为0的情况下为原始的半径（不改变），设定不为0时，按照
    # RadialScale=0.0，径向比例
    # 返回值 Annulus  圆环形区域
    @staticmethod
    def ScShapeTransAnnulus(Annulus, center, stdRadius=0, RadialScale=0.0):
        # print(len(VectorVec))
        Annulus.SetCenter(center)
        if not stdRadius == 0:
            Annulus.SetRadius(stdRadius)
        if not RadialScale == 0.0:
            Annulus.SetRadialScale(RadialScale)
        return Annulus

    # 一般用来对blob工具的圆ROI区域做位置变换
    # Circle 获取blob工具的 “公开圆形ROI”
    # center sc2vector类型，表示远心坐标
    # stdRadius=0，矩形长宽值，默认为0的情况下为原始的半径（不改变），设定不为0时，按照
    # 返回值 Circle  圆形区域
    @staticmethod
    def ScShapeTransCircle(Circle, center, stdRadius=0):
        # print(len(VectorVec))
        Circle.SetCenter(center)
        if not stdRadius == 0:
            Circle.SetRadius(stdRadius)

        return Circle

    # 一般用来对blob工具的矩形ROI区域做位置变换
    # Rec 获取blob工具的 “公开矩形ROI”
    # center sc2vector类型，表示仿射矩形中点坐标
    # dw=0,dh=0，矩形长宽值，默认为0的情况下为原始的长宽（不改变），设定不为0时，按照
    # 返回值 Rec  矩形区域
    @staticmethod
    def ScShapeTransRec(Rec, center, dw=0, dh=0):
        # print(len(VectorVec))
        # Circle.SetCenter( center )
        W = Rec.GetWidth()
        H = Rec.GetHeight()
        if not dw == 0:
            W = dw
        if not dh == 0:
            H = dh
        Rec.Set(center.GetX() - W / 2.0, center.GetY() - H / 2.0, W, H)
        return Rec

    # 一般用来对blob工具的仿射矩形ROI区域做位置变换
    # Rec 获取blob工具的 “仿射矩形ROI”
    # center sc2vector类型，表示仿射矩形中点坐标
    # # transd 需要旋转的角度，默认为0
    # dw=0,dh=0，矩形长宽值，默认为0的情况下为原始的长宽（不改变），设定不为0时，按照
    # 返回值 Rec  仿射矩形区域
    @staticmethod
    def ScShapeTransAffinRec(Rec, center, transd=0.0, dw=0, dh=0):
        # print(len(VectorVec))
        # Circle.SetCenter( center )
        W = Rec.GetXLength()
        H = Rec.GetYLength()
        Rec.SetCenter(center)
        Rec.SetXRotation(GvVisionAssembly.scRadian(transd * math.pi / 180.0))
        if not dw == 0:
            W = dw
        if not dh == 0:
            H = dh
        Rec.SetXLength(W)
        Rec.SetYLength(H)
        return Rec

    # 一般用来对blob工具的多边形ROI区域做位置变换
    # self  ScShape类本身
    # Polyline 获取blob工具的 “公开多边形ROI”
    # VectorVec 生成的标准检测区域的点阵
    # transx # transy # transd 需要偏移的特征点的位置坐标，相对于标准检测区域
    # 返回值 Polyline  多边形ROI 区域
    def ScShapeTransPolyline(self, Polyline, VectorVec, transx=0, transy=0, transd=0):
        # print(len(VectorVec))
        # Circle.SetCenter( center )
        VectorVec2 = GvVisionAssembly.sc2VectorVec()
        VectorVec2 = VectorVec
        self.ScShapeTransPostion(VectorVec2, transx, transy, transd)
        Polyline = GvVisionAssembly.scPolyline(VectorVec2, True)

        return Polyline

    # 两条线交点  含防呆
    # line0 输入线1  scLine类型 线1  坐标的角度与线1 的角度相同
    # line1 输入线2  scLine类型 线2
    # GcCoodPos  GcCoodPos类型，本地定义，
    # bFoolProof BOOL类型  是否防呆  默认Flase
    # stdAngle 标准设定角度   正常角度0-180°  默认90.0°
    # AngleLimit 标准设定公差  正常角度0-180°  默认1.0°
    # strlabel 标识 默认"L1&L2"
    # 返回值 Bool类型  True，表示正常（含不防呆），False 表示异常
    @staticmethod
    def ScShapeLineCross(line0, line1, GcCoodPos, bFoolProof=False, stdAngle=90, AngleLimit=1, strlabel="L1&L2"):
        pos = line0.Intersect(line1)[0]
        GcCoodPos.X = pos.GetX()
        GcCoodPos.Y = pos.GetY()
        dangle = line0.GetRotation().SignedNormMod180().ToDouble() * 180.0 / math.pi
        if math.fabs(dangle) < 45:
            GcCoodPos.D = dangle
        else:
            GcCoodPos.D = line0.GetRotation().NormMod180().ToDouble() * 180.0 / math.pi

        if not bFoolProof:
            return True
        else:
            return ScFoolProof.ScFoolProofline2(line0, line1, stdAngle, AngleLimit, strlabel)

    # 两横两纵四条边的交点
    # self  ScShape类本身
    # lineup 输入线1  scLine类型 上横线
    # linedn 输入线2  scLine类型 下横线
    # linelt 输入线3  scLine类型 左竖线
    # linert 输入线4  scLine类型 右竖线
    # GcCoodPosVec  GcCoodPos类型数组，本地定义，
    # bFoolProof BOOL类型  是否防呆  默认Flase

    # 返回值 errorcode  int类型  1，表示正常（含不防呆），21左上角异常，22右下角异常，23右上角异常，24左下角异常
    def ScShapeLineCross4Lines(self, lineup, linedn, linelt, linert, GcCoodPosVec, bFoolProof=False, dangleLimit=1):
        bul = self.ScShapeLineCross(lineup, linelt, GcCoodPosVec[0], bFoolProof, 90, dangleLimit, "左上交线")
        bdr = self.ScShapeLineCross(linedn, linert, GcCoodPosVec[1], bFoolProof, 90, dangleLimit, "右下交线")
        bur = self.ScShapeLineCross(lineup, linert, GcCoodPosVec[2], bFoolProof, 90, dangleLimit, "右上交线")
        bdl = self.ScShapeLineCross(linedn, linelt, GcCoodPosVec[3], bFoolProof, 90, dangleLimit, "左下交线")

        if len(GcCoodPosVec) > 4:
            GcCoodPosVec[4].X = (GcCoodPosVec[0].X + GcCoodPosVec[1].X + GcCoodPosVec[2].X + GcCoodPosVec[3].X) / 4.0
            GcCoodPosVec[4].Y = (GcCoodPosVec[0].Y + GcCoodPosVec[1].Y + GcCoodPosVec[2].Y + GcCoodPosVec[3].Y) / 4.0
            GcCoodPosVec[4].D = (lineup.GetRotation().ToDouble() * 180.0 / math.pi + linedn.GetRotation().ToDouble() * 180.0 / math.pi) / 2.0

        if not bFoolProof:
            return 1
        elif bul and bdr and bur and bdl:
            return 1
        elif not bul:
            return 21
        elif not bdr:
            return 22
        elif not bur:
            return 23
        elif not bdl:
            return 24
        else:
            return 25

    # 获取直线的角度
    # self  ScShape类本身
    # line  输入直线
    # dAngle 直线预设角度，比如返回一个90度附近的角度（固定取值90/-90/0/180/270）其余返回本值
    # 返回值 resAngle  double类型，返回角度
    #
    def ScShapeLineGetAngle(self, line, dAngle=0):

        resAngle = 0
        if dAngle == 0:
            resAngle = line.GetRotation().SignedNormMod180().ToDouble() * 180.0 / math.pi
        elif dAngle == 90:
            resAngle = line.GetRotation().NormMod180().ToDouble() * 180.0 / math.pi
        elif dAngle == 180:
            resAngle = line.GetRotation().SignedNormMod180().ToDouble() * 180.0 / math.pi + 180.0
        elif dAngle == 270:
            resAngle = line.GetRotation().NormMod180().ToDouble() * 180.0 / math.pi + 180.0
        elif dAngle == -90:
            resAngle = line.GetRotation().NormMod180().ToDouble() * 180.0 / math.pi - 180.0
        else:
            resAngle = line.GetRotation().Norm().ToDouble() * 180.0 / math.pi

        return resAngle

    # 把任意一个点,在图像坐标系下旋转到另一个点位置
    # VecP 图像上任意一点 scvector 类型
    # dangle 角度值。±180.0
    # Veccenter scvector 类型
    def ScRotateVector(self, VecP, dangle=0, Veccenter=GvVisionAssembly.sc2Vector(0, 0)):
        ResVec = GvVisionAssembly.sc2Vector(0, 0)
        arcangle = dangle * math.pi / 180.0
        P1X = VecP.GetX()
        P1Y = VecP.GetY()
        P0X = Veccenter.GetX()
        P0Y = Veccenter.GetY()
        cosA = math.cos(arcangle)
        sinA = math.sin(arcangle)

        ResVec.SetX((P1X - P0X) * cosA - (P1Y - P0Y) * sinA + P0X)
        ResVec.SetY((P1X - P0X) * sinA + (P1Y - P0Y) * cosA + P0Y)
        return ResVec

    # 计算点数组到直线的最大距离
    # Vec 数组点
    # benchline 基准线
    # bonesidetype 测量类型
    # bonesidetype=0,检测绝对位置上下左右不分
    # bonesidetype=1,左右检测右边
    # bonesidetype=2,左右检测左边
    # bonesidetype=3,上下检测下边
    # bonesidetype=4,上下检测上边
    # bfoolproof=False，是否防呆，默认不防呆
    # dLimit=10.0 防呆spec
    # 返回值【最大距离，最大距离对应的序号，最大距离是否满足要求，【【变换前点坐标，是否满足距离范围】，【】，……】】

    def ScaxDisVecToLine(self, Vec, benchline, bonesidetype=1, bfoolproof=False, dLimit=10.0):
        maxdistance = 0
        maxdistanceindex = 0
        maxdisfalg = True
        dis = 0
        res = []
        angle = 0
        pos = benchline.GetPos()
        if bonesidetype == 0 or bonesidetype == 1 or bonesidetype == 2:
            angle = self.ScShapeLineGetAngle(self, benchline, 90)
            for i in range(len(Vec)):
                respos = self.ScRotateVector(self, Vec[i], 90 - angle, pos)
                if bonesidetype == 0:
                    dis = math.fabs(respos.GetX() - pos.GetX())
                elif bonesidetype == 1:
                    dis = respos.GetX() - pos.GetX()
                elif bonesidetype == 2:
                    dis = pos.GetX() - respos.GetX()

                if bfoolproof and dis > dLimit:
                    res.append([Vec[i], False])
                else:
                    res.append([Vec[i], True])

                if dis > maxdistance:
                    maxdistance = dis
                    maxdistanceindex = i
                    if bfoolproof and dis > dLimit:
                        maxdisfalg = False
        else:

            angle = self.ScShapeLineGetAngle(self, benchline, 0)
            for i in range(len(Vec)):
                respos = self.ScRotateVector(self, Vec[i], 0 - angle, pos)
                if bonesidetype == 3:
                    dis = respos.GetY() - pos.GetY()
                else:
                    dis = pos.GetY() - respos.GetY()

                if bfoolproof and dis > dLimit:
                    res.append([Vec[i], False])
                else:
                    res.append([Vec[i], True])

                if dis > maxdistance:
                    maxdistance = dis
                    maxdistanceindex = i
                    if bfoolproof and dis > dLimit:
                        maxdisfalg = False

        return [maxdistance, maxdistanceindex, maxdisfalg, res]

    # 显示一个点到一条直线的距离的线段
    # VecP 点scvector类型
    # benchline 基准线 Sclinel类型
    # 返回值 SclineSeg 线段类型
    def ScDisPointToLine(self, VecP, benchline):
        angle = ScShape.ScShapeLineGetAngle(self, benchline, 0)
        rot = GvVisionAssembly.scRadian((90 - angle) * math.pi / 180.0)
        lineVer = GvVisionAssembly.scLine(VecP, rot)
        P2 = lineVer.Intersect(benchline)[0]

        return GvVisionAssembly.scLineSeg(VecP, P2)

    # 查找一个矩形的中心
    # 返回值 Scvector类型
    def ScGetRectCenter(self, rec):
        x_min = rec.GetUL().GetX()
        y_min = rec.GetUL().GetY()
        x_max = rec.GetLR().GetX()
        y_max = rec.GetLL().GetY()
        x_center = (x_max + x_min) / 2
        y_center = (y_max + y_min) / 2
        return GvVisionAssembly.sc2Vector(x_center, y_center)

    # 查找一个放射矩形的中心
    # 返回值 Scvector类型
    def ScGetAffRectCenter(self, rec):
        x_min = rec.GetUL().GetX()
        y_min = rec.GetUL().GetY()
        x_max = rec.GetLR().GetX()
        y_max = rec.GetLL().GetY()
        x_center = (x_max + x_min) / 2
        y_center = (y_max + y_min) / 2
        return GvVisionAssembly.sc2Vector(x_center, y_center)

    # 获取两个向量点之间的距离
    # 返回值 double 类型
    def ScGetDisofVec(self, Vector1, Vector2):
        distance = math.sqrt(pow((Vector1.GetX() - Vector2.GetX()), 2) + pow((Vector1.GetY() - Vector2.GetY()), 2))
        return distance

    # 过滤掉靠的比较近的结果
    # 返回值 list 类型
    def ScResultfilter(self, center_list, new_center_list, distance_threthold=100):
        delete_list_all = []
        for i, center1 in enumerate(center_list):
            if i not in delete_list_all:
                delete_list = []
                delete_list.append(i)
                for j, center2 in enumerate(center_list):
                    if j > i and j not in delete_list_all:
                        distance = self.ScGetDisofVec(self, center1, center2)
                        if distance < distance_threthold:
                            delete_list.append(j)
                            delete_list_all.append(j)
                temp_center_x = 0
                temp_center_y = 0
                idx = 0
                for idx, center_num in enumerate(delete_list):
                    temp_center_x += center_list[center_num].GetX()
                    temp_center_y += center_list[center_num].GetY()
                mean_x = temp_center_x / (idx + 1)
                mean_y = temp_center_y / (idx + 1)

                new_center_list.append(GvVisionAssembly.sc2Vector(mean_x, mean_y))

        return new_center_list

    # 获取子图区域
    def ScGetsubImagRec(self, new_center_list, imgls, window=256, rigionlimit=[0, 0, 2500, 2500], height=5100,
                        width=5100):
        dx_min = rigionlimit[0]
        dy_min = rigionlimit[1]
        dx_max = rigionlimit[2]
        dy_max = rigionlimit[3]
        cut_x = 0
        cut_y = 0
        for center in new_center_list:
            cut_x_min = max(center.GetX() - window / 2 + cut_x, 1)  # 超出边界限制
            cut_y_min = max(center.GetY() - window / 2 + cut_y, 1)
            cut_x_max = min(center.GetX() + window / 2 + cut_x, width)
            cut_y_max = min(center.GetY() + window / 2 + cut_y, height)
            if cut_x_max == width:
                cut_x_min = cut_x_max - window
            if cut_y_max == height:
                cut_y_min = cut_y_max - window
            cut_x_center = center.GetX() + cut_x
            cut_y_center = center.GetY() + cut_y
            print(cut_x_center, cut_y_center)
            if dx_min < cut_x_center < dx_max and dy_min < cut_y_center < dy_max:
                roi_rect = GvVisionAssembly.scRect(cut_x_min, cut_y_min, window, window)  # 左上角坐标+宽高
                imgls.append(roi_rect)

    # 判断矩形结果中心是否在另一个矩形区域内
    def ScIsReccenterInRec(self, rec1, rec2):
        PCenter = self.ScGetRectCenter(self, rec1)
        if rec2.GetUL().GetX() < PCenter.GetX() < rec2.GetLR().GetX() and rec2.GetUL().GetY() < PCenter.GetY() < rec2.GetLR().GetY():
            return True
        else:
            return False

    def GetRandAngle(self, p1, p2):
        L1 = GvVisionAssembly.scLine(p1, p2 - p1)
        angle = L1.GetRotation().Norm().ToDouble()
        R = GvVisionAssembly.DistancePoint2Point(p1, p2).distance
        res = GvVisionAssembly.sc2Vector(R, angle)
        return res

    def GetOriginalPos(self, stdPos, vec):
        X = vec.GetX() * math.cos(vec.GetY())
        Y = vec.GetX() * math.sin(vec.GetY())
        res = GvVisionAssembly.sc2Vector(X, Y) + stdPos
        return res

    def GetP2Vec(self, pos, VecL, VecU, index):
        minIndex = 0
        startU = index - 20
        res = GvVisionAssembly.sc2Vector(0, 0)

        if startU < 0:
            startU = 0

        endU = index + 20
        if endU > len(VecU):
            endU = len(VecU)

        endL = index + 20
        if endL > len(VecL):
            endL = len(VecL)

        minium = 999.99
        minIndex = 0
        # print(startU,endL,endU)
        for i in range(startU, endL, 1):
            dtempR = abs(pos.GetY() - VecL[i].GetY())
            if minium > dtempR:
                minium = dtempR
                minIndex = i
        if pos.GetX() < VecL[minIndex].GetX():
            res.SetX(1)
            return res

        minium = 999.99
        minIndex = 0
        for i in range(startU, endU, 1):
            dtempR = abs(pos.GetY() - VecU[i].GetY())
            if minium > dtempR:
                minium = dtempR
                minIndex = i
        if pos.GetX() > VecU[minIndex].GetX():
            res.SetY(1)
            return res
        return res

    def IsPonitInRect(self, PT, Rect):
        Result = False
        if PT.GetX() > Rect.GetUL().GetX() and PT.GetY() > Rect.GetUL().GetY() and PT.GetX() < Rect.GetLR().GetX() and PT.GetY() < Rect.GetLR().GetY():
            Result = True
        else:
            Result = False
>>>>>>> c64d729fd419c4ce1675d7be701b9a882322c69d
        return Result