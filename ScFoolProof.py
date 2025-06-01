import sys
import math
#import numpy

#sys.path.append(r'C:\Program Files\VISIONAssembly_x64')
import GvVisionAssembly


class ScFoolProof(object):
    def __init__(self,x,y):
        self.x = x;
        self.y = y;

    #判断单条线夹角是否满足需求
    #line0 输入线1  scLine类型
    # stdAngle 标准夹角  double类型
    # AngleLimit 标准公差  double类型
    # strlabel 标注（NG时提示哪一个异常了）可忽略
    #返回值 True符合标准，False不符合标准
    @staticmethod
    def ScFoolProofline1(line0, stdAngle=90, AngleLimit=10, strlabel="L1"):
        dangle=0.0
        if math.fabs(stdAngle)<45:
            dangle=line0.GetRotation().SignedNormMod180().ToDouble()*180.0/math.pi

        elif math.fabs(stdAngle)<135:
            dangle = line0.GetRotation().NormMod180().ToDouble()*180.0/math.pi

        else:
            dangle = line0.GetRotation().SignedNormMod180().ToDouble() * 180.0 / math.pi+180

        print(dangle)
        if math.fabs(stdAngle-dangle) < AngleLimit:

            return True
        else:
            print(strlabel+"当前直线角度NG",dangle,"限制",str(stdAngle)+"±"+str(AngleLimit))
            return False

    #判断两条线夹角是否满足需求
    #line0 输入线1  scLine类型
    #line1 输入线2  scLine类型
    # stdAngle 标准夹角  double类型
    # AngleLimit 标准公差  double类型
    # strlabel 标注（NG时提示哪一个异常了）可忽略
    #返回值 True符合标准，False不符合标准
    @staticmethod
    def ScFoolProofline2(line0,line1,stdAngle=90,AngleLimit=1,strlabel="L1&L2"):
        dangle=0.0

        if math.fabs(stdAngle)<45:
            dangle=line0.GetAngle(line1).SignedNormMod180().ToDouble()*180.0/math.pi

        elif math.fabs(stdAngle)<135:
            dangle = line0.GetAngle(line1).NormMod180().ToDouble()*180.0/math.pi

        else:
            dangle = line0.GetAngle(line1).SignedNormMod180().ToDouble() * 180.0 / math.pi+180

        #print(dangle)
        if math.fabs(stdAngle-dangle) < AngleLimit:

            return True
        else:
            print(strlabel+"当前夹角角度NG ",dangle,"限制",str(stdAngle)+"±"+str(AngleLimit))
            return False

    #判断圆半径是否满足需求
    #circleR 输入圆  scCircle类型
    # stdR 标准圆半径  double类型
    # stdR 标准圆半径  double类型
    # strlabel 标注（NG时提示哪一个异常了）可忽略
    #返回值 True符合标准，False不符合标准
    @staticmethod
    def ScFoolProofCircle(circleR,stdR=100,RLimit=10,strlabel="R1"):
        dangle=0.0
        #print(dangle)
        if math.fabs(circleR.GetRadius()-stdR) < RLimit:
            return True
        else:
            print(strlabel+"当前半径NG ",dangle,"限制",str(stdR)+"±"+str(RLimit))
            return False

