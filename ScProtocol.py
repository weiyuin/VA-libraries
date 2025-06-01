import sys
# sys.path.append(r'C:\Program Files\VISIONAssembly_x64')
import GvVisionAssembly
import binascii

auchCRCHi = [
    0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81,
    0x40, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0,
    0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01,
    0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41,
    0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81,
    0x40, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0,
    0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01,
    0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40,
    0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81,
    0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0,
    0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01,
    0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41,
    0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81,
    0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0,
    0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01,
    0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41,
    0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81,
    0x40]
auchCRCLo = [
    0x00, 0xC0, 0xC1, 0x01, 0xC3, 0x03, 0x02, 0xC2, 0xC6, 0x06, 0x07, 0xC7, 0x05, 0xC5, 0xC4,
    0x04, 0xCC, 0x0C, 0x0D, 0xCD, 0x0F, 0xCF, 0xCE, 0x0E, 0x0A, 0xCA, 0xCB, 0x0B, 0xC9, 0x09,
    0x08, 0xC8, 0xD8, 0x18, 0x19, 0xD9, 0x1B, 0xDB, 0xDA, 0x1A, 0x1E, 0xDE, 0xDF, 0x1F, 0xDD,
    0x1D, 0x1C, 0xDC, 0x14, 0xD4, 0xD5, 0x15, 0xD7, 0x17, 0x16, 0xD6, 0xD2, 0x12, 0x13, 0xD3,
    0x11, 0xD1, 0xD0, 0x10, 0xF0, 0x30, 0x31, 0xF1, 0x33, 0xF3, 0xF2, 0x32, 0x36, 0xF6, 0xF7,
    0x37, 0xF5, 0x35, 0x34, 0xF4, 0x3C, 0xFC, 0xFD, 0x3D, 0xFF, 0x3F, 0x3E, 0xFE, 0xFA, 0x3A,
    0x3B, 0xFB, 0x39, 0xF9, 0xF8, 0x38, 0x28, 0xE8, 0xE9, 0x29, 0xEB, 0x2B, 0x2A, 0xEA, 0xEE,
    0x2E, 0x2F, 0xEF, 0x2D, 0xED, 0xEC, 0x2C, 0xE4, 0x24, 0x25, 0xE5, 0x27, 0xE7, 0xE6, 0x26,
    0x22, 0xE2, 0xE3, 0x23, 0xE1, 0x21, 0x20, 0xE0, 0xA0, 0x60, 0x61, 0xA1, 0x63, 0xA3, 0xA2,
    0x62, 0x66, 0xA6, 0xA7, 0x67, 0xA5, 0x65, 0x64, 0xA4, 0x6C, 0xAC, 0xAD, 0x6D, 0xAF, 0x6F,
    0x6E, 0xAE, 0xAA, 0x6A, 0x6B, 0xAB, 0x69, 0xA9, 0xA8, 0x68, 0x78, 0xB8, 0xB9, 0x79, 0xBB,
    0x7B, 0x7A, 0xBA, 0xBE, 0x7E, 0x7F, 0xBF, 0x7D, 0xBD, 0xBC, 0x7C, 0xB4, 0x74, 0x75, 0xB5,
    0x77, 0xB7, 0xB6, 0x76, 0x72, 0xB2, 0xB3, 0x73, 0xB1, 0x71, 0x70, 0xB0, 0x50, 0x90, 0x91,
    0x51, 0x93, 0x53, 0x52, 0x92, 0x96, 0x56, 0x57, 0x97, 0x55, 0x95, 0x94, 0x54, 0x9C, 0x5C,
    0x5D, 0x9D, 0x5F, 0x9F, 0x9E, 0x5E, 0x5A, 0x9A, 0x9B, 0x5B, 0x99, 0x59, 0x58, 0x98, 0x88,
    0x48, 0x49, 0x89, 0x4B, 0x8B, 0x8A, 0x4A, 0x4E, 0x8E, 0x8F, 0x4F, 0x8D, 0x4D, 0x4C, 0x8C,
    0x44, 0x84, 0x85, 0x45, 0x87, 0x47, 0x46, 0x86, 0x82, 0x42, 0x43, 0x83, 0x41, 0x81, 0x80,
    0x40
]


# 即可，路径名即为pyd文件所在的路径
class ScProtocol:

    # 控制光源通道亮度值
    # nChanne int型，取值 1,2,3,4，
    # nBrightValue int型，0-255，超出此区间，自动恢复到该区间
    # 返回值，string类型，可以直接发送的结果，带起始结束符号
    @staticmethod
    def LCRLightSendIntense(nChanne, nBrightValue):
        Light_strSTX = chr(0x02)
        Light_strETX = chr(0x03)

        # print("通道", nChanne, "亮度", nBrightValue)
        # 光源指令16进制ASCII加和，原始指令为：W1100010255
        # 亮度转换

        if nBrightValue > 255:
            nBrightValue = 255
        if nBrightValue < 0:
            nBrightValue = 0
        Light_nBright_1 = ord('0') + int(nBrightValue / 100)
        Light_nBright_2 = ord('0') + int(nBrightValue / 10 % 10)
        Light_nBright_3 = ord('0') + int(nBrightValue % 10)
        Light_Sum_n = ord('W') + ord('1') * 2 + ord('0') * 4 + Light_nBright_1 + Light_nBright_2 + Light_nBright_3 + ord(str(nChanne))
        # 计算校验位的末尾两字符
        Light_strCheckF = hex(Light_Sum_n)[-2:-1].upper()
        Light_strCheckL = hex(Light_Sum_n)[-1:].upper()

        # 生成触发指令
        Light_nBrightTemp = str(nBrightValue).zfill(4)

        Light_strCmdTemp = "W11000" + str(nChanne) + Light_nBrightTemp
        Light_strCmd = Light_strSTX + Light_strCmdTemp + Light_strCheckF + Light_strCheckL + Light_strETX
        print("触发指令", Light_strCmd)

        return Light_strCmd

    @staticmethod
    def LCRLightReceiveIntense(strmessage):

        print("返回指令", strmessage)
        errorcode = 1
        return errorcode

    # 打开单个通道自动负载
    # nChanne int型，取值 1,2,3,4，
    # bFlag bool型，True 打开自动负载，False关闭自动负载
    # 返回值，string类型，可以直接发送的结果，带起始结束符号
    @staticmethod
    def LCRLightOpenLoad(nChanne, bFlag):
        # 获取指令前后缀
        Light_strSTX = chr(0x02)
        Light_strETX = chr(0x03)
        Light_nChannel = nChanne

        print("通道", Light_nChannel)
        # 光源指令16进制ASCII加和，原始指令为：W0700010000

        Light_Sum_n = ""
        if bFlag:
            Light_Sum_n = ord('W') + ord('0') + ord('7') + ord('0') * 3 + ord(str(nChanne)) + ord('0') * 3 + ord('1')
        else:
            Light_Sum_n = ord('W') + ord('0') + ord('7') + ord('0') * 3 + ord(str(nChanne)) + ord('0') * 3 + ord('0')

        # print(Light_Sum_n)
        # 计算校验位的末尾两字符
        Light_strCheckF = hex(Light_Sum_n)[-2:-1].upper()
        Light_strCheckL = hex(Light_Sum_n)[-1:].upper()

        # 生成触发指令
        Light_strCmdTemp = "W07000" + str(Light_nChannel) + "0000"
        Light_strCmdElc = Light_strSTX + Light_strCmdTemp + Light_strCheckF + Light_strCheckL + Light_strETX
        print("触发指令", Light_strCmdElc)
        return Light_strCmdElc

    # 打开单个通道电流负载
    # nChanne int型，取值 1,2,3,4，
    # nCurrentLimit int型，0-999，超出此区间，自动恢复到该区间
    # 返回值，string类型，可以直接发送的结果，带起始结束符号
    @staticmethod
    def LCRLightCurrentLimit(nChanne, nCurrentLimit):
        # 获取指令前后缀
        Light_strSTX = chr(0x02)
        Light_strETX = chr(0x03)

        Light_nChannel = nChanne
        if nCurrentLimit > 999:
            nCurrentLimit = 999
        if nCurrentLimit < 0:
            nCurrentLimit = 0

        strlimit = str(nCurrentLimit).zfill(3)
        Light_Sum_n = ord('W') + ord('0') + ord('6') + ord('0') * 3 + ord(str(Light_nChannel)) + ord('0') + ord(strlimit[0:1]) + ord(strlimit[1:2]) + ord(strlimit[2:3])
        # print(Light_Sum_n)

        # 计算校验位的末尾两字符
        Light_strCheckF = hex(Light_Sum_n)[-2:-1].upper()
        Light_strCheckL = hex(Light_Sum_n)[-1:].upper()

        # 生成触发指令
        Light_strCmdTemp = "W06000" + str(Light_nChannel) + str(nCurrentLimit).zfill(4)
        Light_strCmdElc = Light_strSTX + Light_strCmdTemp + Light_strCheckF + Light_strCheckL + Light_strETX
        print(Light_strCmdElc)

        return Light_strCmdElc

    # 字符串类型转ASCII码
    # StrSN string型，取值 “ XXXX ”，
    # nType int型，0-3，超出此区间，自动恢复到0,0，逐个字符解析，1，前高后低，2前低后高
    # 返回值，int Vec类型

    def ScStringtoChar(self, strSN, nType=0):
        Res = []
        i = 0
        if nType < 0 or nType > 2:
            nType = 0

        if nType == 0:
            len_d = len(strSN)
            for i in range(0, len_d):
                Res.append(ord(strSN[i]))

        elif nType == 1:
            len_d = int(len(strSN) / 2)
            for i in range(0, len_d):
                Res.append(ord(strSN[2 * i]) * 256 + ord(strSN[2 * i + 1]))
            if (len(strSN) % 2 == 1):
                Res.append(ord(strSN[2 * i]) * 256)

        elif nType == 2:
            len_d = int(len(strSN) / 2)
            for i in range(0, len_d):
                Res.append(ord(strSN[2 * i + 1]) * 256 + ord(strSN[2 * i]))
            if (len(strSN) % 2 == 1):
                Res.append(ord(strSN[2 * i]))

        return Res

    # ASCII码转字符串类型
    # Rcv Ascii int数组类型，取值 0-255，
    # nType int型，0-3，超出此区间，自动恢复到0,0，逐个字符解析，1，前高后低，2前低后高
    # 返回值Res，string类型

    def ScChartoString(self, Rcv, nType=0):
        Res = ""
        if nType < 0 or nType > 2:
            nType = 0

        if nType == 0:
            for i in range(0, len(Rcv)):
                Res = Res + chr(Rcv[i])
        elif nType == 1:
            for i in range(0, len(Rcv)):
                Res = Res + chr(Rcv[i] // 256)
                Res = Res + chr(Rcv[i] % 256)

        elif nType == 2:
            for i in range(0, len(Rcv)):
                Res = Res + chr(Rcv[i] % 256)
                Res = Res + chr(Rcv[i] // 256)

        return Res

    @staticmethod
    def mchar(intv):
        if intv < 10:
            return chr(int(intv) + ord('0'))
        else:
            return chr(int(intv) - 10 + ord('a'))

    def getchar(self, x):
        h = x / 16
        l = x % 16
        return self.mchar(h) + self.mchar(l)

    def CRC16(self, beg):
        uindex = 0
        tempp = 0
        CRCHL = 0
        uchCRCHi = 0xFF
        uchCRCLo = 0xFF
        for i in range(len(beg)):
            uindex = uchCRCHi ^ beg[tempp]
            tempp = tempp + 1
            uchCRCHi = uchCRCLo ^ auchCRCHi[uindex]
            uchCRCLo = auchCRCLo[uindex]
        return [uchCRCHi, uchCRCLo]
        CRCHL = uchCRCHi << 8
        CRCHL |= uchCRCLo
        return CRCHL

    def MultiSpectrumWriteSingleRegsiter(self, Add, Value):
        sums = [0x01, 0x06]
        sums.append(((Add & 0xFF00) >> 8))
        sums.append((Add & 0xFF))

        sums.append(((Value & 0xFF00) >> 8))
        sums.append((Value & 0xFF))

        sums.append(0x00)

        H = self.CRC16(self, sums)
        sums.append(H[0])
        sums.append(H[1])
        return sums

    def MultiSpectrumWriteMultiRegsiter(self, Value):
        sums = [0x01, 0x16]
        sums.append(4 * len(Value))
        for i in range(len(Value)):
            sums.append(((Value[i][0] & 0xFF00) >> 8))
            sums.append((Value[i][0] & 0xFF))

            sums.append(((Value[i][1] & 0xFF00) >> 8))
            sums.append((Value[i][1] & 0xFF))

        sums.append(0x00)

        H = self.CRC16(self, sums)
        sums.append(H[0])
        sums.append(H[1])
        return sums

    def MultiSpectrumReset(self):
        return self.MultiSpectrumWriteSingleRegsiter(self, 0x1000, 0x0001)

    # 在一个扇区的8Bit 里，从低到高位对应颜色：白,蓝,绿,黄,红外730,红外850,紫外,红
    def MultiSpectrumOpenChannel(self, value):
        N1 = value[0]
        N2 = value[1]
        N3 = value[2]
        N4 = value[3]
        F1 = 0x00
        F2 = 0x00
        F2 = 0x00
        F2 = 0x00
        if not N1 == 0:
            F1 = 0x01 << (N1 - 1)
        if not N2 == 0:
            F2 = (0x01 << (N2 - 1 + 8)) ^ F1
        if not N3 == 0:
            F3 = 0x01 << (N3 - 1)
        if not N4 == 0:
            F4 = (0x01 << (N4 - 1 + 8)) ^ F3

        return self.MultiSpectrumWriteMultiRegsiter(self, [[0x0041, F2], [0x0042, F4]])

    def MultiSpectrumSetSignleChannel(self, nZone, nChannel, Value):
        nAddress = (nZone - 1) * 8 + nChannel
        return self.MultiSpectrumWriteSingleRegsiter(self, nAddress, Value)

    def MultiSpectrumSetChannel(self, nChannel, Value):
        nAddress1 = (1 - 1) * 8 + nChannel
        nAddress2 = (2 - 1) * 8 + nChannel
        nAddress3 = (3 - 1) * 8 + nChannel
        nAddress4 = (4 - 1) * 8 + nChannel
        return self.MultiSpectrumWriteMultiRegsiter(self, \
                                                    [[nAddress1, Value], \
                                                     [nAddress2, Value], \
                                                     [nAddress3, Value], \
                                                     [nAddress4, Value]])
