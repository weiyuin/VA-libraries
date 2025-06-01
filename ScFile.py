import shutil
import time
import os
#import xlrd
import csv

import os
import zipfile
from os.path import join, getsize
import datetime
import threading

class ScFile:
    @staticmethod
    def mkdirFolder(rootpath):
        # 引入模块
        import os
        strDay = time.strftime("%m%d")
        #path = "{}\\{}".format(rootpath, strDay)
        path=rootpath
        #print(path)
        # 去除首位空格
        path = path.strip()
        # 去除尾部 \ 符号
        path = path.rstrip("\\")

        # 判断路径是否存在
        # 存在     True
        # 不存在   False
        isExists = os.path.exists(path)

        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs(path)
            #print(path + "创建成功")
#            return True
        #else:
            # 如果目录存在则不创建，并提示目录已存在
            #print(path + "目录已存在")
#            return False
        #print(path)
        return path

    @staticmethod
    def mkdirDate(rootpath):
        # 引入模块
        import os
        strDay = time.strftime("%m%d")
        path = "{}\\{}".format(rootpath, strDay)

        #print(path)
        # 去除首位空格
        path = path.strip()
        # 去除尾部 \ 符号
        path = path.rstrip("\\")

        # 判断路径是否存在
        # 存在     True
        # 不存在   False
        isExists = os.path.exists(path)

        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs(path)
            # print(path + "创建成功")
            #            return True
        #else:
            # 如果目录存在则不创建，并提示目录已存在
            # print(path + "目录已存在")
            #            return False
            # print(path)
        return path

    @staticmethod
    def move_image(srcimage,SN, rootpath):
        imagepath=srcimage.split("\\")[3]
        strDay = time.strftime("%m%d")
        dstimage="{}\\{}\\{}\\{}_{}".format(rootpath, strDay, SN, SN, imagepath)
        print(srcimage)
        print(dstimage)
        shutil.copy(srcimage, dstimage)
        return dstimage

#    def ReadXLSRowCol(self,filepath,Row,Col,sheetindex=0):
#        workbook = xlrd.open_workbook(filepath)
        # 获取所有sheet
#        sheet_name = workbook.sheet_names()[sheetindex]

        # 根据sheet索引或者名称获取sheet内容
#        sheet = workbook.sheet_by_index(sheetindex)  # sheet索引从0开始
#        data=sheet.cell_value(Row, Col)  # 吸笔1X
#        return data

    def ScReadCSVRowCol(self, filepath, Row, Col, encode = 'gbk'):
        with open(filepath, 'r', encoding = encode) as csvFile:
            reader = csv.reader(csvFile)
            column = [row[Row] for row in reader]  # 吸笔号
            #print(column[2])  # 穴位号
            return column[Col]

    def __zip_file(src_dir,zip_name = ''):
        if zip_name == '':
            zip_name = src_dir + '.zip'
        z = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
        for dirpath, dirnames, filenames in os.walk(src_dir):
            fpath = dirpath.replace(src_dir, '')
            fpath = fpath and fpath + os.sep or ''
            for filename in filenames:
                z.write(os.path.join(dirpath, filename), fpath + filename)
                print('==压缩成功==')
        z.close()

    #src_dir：你要压缩的文件夹的路径
    #zip_name：压缩后zip文件的路径及名称
    def Sczip_file(self, src_dir,zip_name = '',AsynProcess=True):
        if AsynProcess==False:
            ScFile.__zip_file(src_dir,zip_name)
        else :
            thread = threading.Thread(target=ScFile.__zip_file, args=(src_dir, zip_name))
            thread.start()

    #zip_src: 是zip文件的全路径
    #dst_dir：是要解压到的目的文件夹
    @staticmethod
    def Scunzip_file(zip_src, dst_dir):
        r = zipfile.is_zipfile(zip_src)
        if r:
            fz = zipfile.ZipFile(zip_src, 'r')
            for file in fz.namelist():
                fz.extract(file, dst_dir)
        else:
            print('This is not zip')

    # shutil.move(filename, dst_dir) 剪切（移动）文件到指定目录

    #删除文件夹
    #shutil.rmtree(src_dir)

    #删除指定文件
    #os.remove(file_src)

    #遍历文件夹
    #for filename in os.listdir(src_dir):

    #复制文件
    #shutil.copyfile(src_file, dst_file)

    #.获取文件夹大小
    #
    @staticmethod
    def Scget_dir_size(dir_path, SizeFormat="MB"):
        Tmpsize = 0
        size = 0

        for root, dirs, files in os.walk(dir_path):
            Tmpsize += sum([getsize(join(root, name)) for name in files])
        if SizeFormat =="KB":
            size=Tmpsize/1024
        elif SizeFormat =="MB":
            size = Tmpsize / 1024/1024
        elif SizeFormat =="GB":
            size = Tmpsize / 1024/1024/1024
        else:
            size = Tmpsize / 1024 / 1024
        return size



    #self 类名称本身 ScFile
    #CMD：CMD 通信指令，T11 T21等
    #SN：需要给的SN
    #NozzleIndex：吸笔号
    #CavityIndex：穴位号
    #Status,物料的状态 OK/NG
    def GetImageName(self,CMD, SN, NozzleIndex, CavityIndex, Status):
        strtime = datetime.datetime.now()
        CurTime = strtime.strftime('%Y%m%d_%H%M%S')
        YearTime = strtime.strftime('%Y')
        DayTime = strtime.strftime('%m%d')

        FolderPath = "{}\\{}\\{}\\{}\\".format(YearTime, DayTime, Status, SN)
        srcfilename = "{}_Nozzle{}_Cavity{}_{}_{}_{}_SRC".format(CMD, NozzleIndex, CavityIndex, SN, CurTime, Status)
        resfilename = "{}_Nozzle{}_Cavity{}_{}_{}_{}_RES".format(CMD, NozzleIndex, CavityIndex, SN, CurTime, Status)
        return [FolderPath + srcfilename, FolderPath + resfilename]

    #self 类名称本身 ScFile
    #StrOringalNmae：需要被修改的文件名称
    #SN：需要给的SN
    #Status,物料的状态 OK/NG
    def ChangeImageName(self,StrOringalNmae, SN, Status):
        name = StrOringalNmae.split("\\")
        filename = name[-1]
        print(filename)
        Com = filename.split("_")
        newfilename = "{}_{}_{}_{}_{}_{}_{}_{}".format(Com[0], Com[1], Com[2], SN, Com[4], Com[5], Com[6], Com[7])
        FolderPath = "{}\\{}\\{}\\{}\\".format(name[0], name[1], Status, SN)
        return FolderPath + newfilename

    #self 类名称本身 ScFile
    #srcImage：需要被移动的文件名称
    #dstImage：需要移动的目标文件路径

    def MoveImage(self,srcImage, dstImage):
        isExists = os.path.exists(srcImage)
        if not isExists:
            print("Error:" + srcImage + " (does’t exist)")
            return False
        path = dstImage.strip()
        path = path.rstrip("\\")
        dirname = os.path.dirname(path)
        isExists = os.path.exists(dirname)
        if not isExists:
            os.makedirs(path)

        # shutil.move("E:\\GVIMAGES\\"+StrOringalNmae+".bmp","E:\\GVIMAGES\\"+newname+".bmp")
        shutil.move(srcImage, dstImage)




    ##用于去除多余的反斜杠及提取路径
    def ImgPathPocess(self,strImg):
        strPath = strImg.split("\\")[0]
        for i in range(1, len(strImg.split("\\"))):
            if strImg.split("\\")[i] != "":
                strPath = strPath + "\\" + strImg.split("\\")[i]
        strPathNew = strPath.split("\\")[0]
        for i in range(1, len(strPath.split("\\")) - 1):
            strPathNew = strPathNew + "\\" + strImg.split("\\")[i]
        return strPathNew

    # 图片转移
    # systemPath  系统盘路径 "E:\\GVIMAGES\\"
    # CCDSysTemPath  要转移的图片路径
    # ImagePathTargetSvae 视觉用全图存图路径
    # ImagePathTargetUpLoad  上传用图片路径
    # SN 真实SN
    # VirtualSN 虚拟SN
    # ReplaceSN 是否替换SN
    def ImgMove(self,systemPath, CCDSysTemPath, ImagePathTargetSvae, ImagePathTargetUpLoad, SN, VirtualSN, ReplaceSN=True):
        # 路径下图片遍历
        AllListPathCCD = os.listdir(CCDSysTemPath)
        imgPathListCCD1 = []
        ErrMes = []
        # 生成存储路径
        PathToSave = systemPath + self.ImgPathPocess(ImagePathTargetSvae) + "\\"
        PathToUpLoad = systemPath + self.ImgPathPocess(ImagePathTargetUpLoad) + "\\"
        # 路径防呆
        isExists = os.path.exists(PathToSave)
        if not isExists:
            os.makedirs(PathToSave)
        isExists = os.path.exists(PathToUpLoad)
        if not isExists:
            os.makedirs(PathToUpLoad)
        # 符合条件的图片收集
        for fliename in AllListPathCCD:
            if ReplaceSN == True:
                if fliename.find(VirtualSN) != -1:
                    imgPathListCCD1.append(fliename)
            else:
                if fliename.find(SN) != -1:
                    imgPathListCCD1.append(fliename)
        ErrMes.append(SN + "," + VirtualSN + ":检索到" + str(len(imgPathListCCD1)) + "张图")
        if len(imgPathListCCD1) > 0:
            for i in range(0, len(imgPathListCCD1)):
                # 获取图片原始路径
                CCD1ImgCapPath = CCDSysTemPath + imgPathListCCD1[i]
                ErrMes.append(CCD1ImgCapPath + ":开始进行处理...")
                newCCD1ImgPathCap = systemPath + ImgPathPocess(ImagePathTargetSvae) + "\\" + imgPathListCCD1[i].replace(
                    VirtualSN, SN)
                # 生成上传路径
                UpLoadCCD1ImgPathCap = systemPath + ImgPathPocess(ImagePathTargetUpLoad) + "\\" + imgPathListCCD1[
                    i].replace(VirtualSN, SN)
                try:
                    # 图片截图上传转移
                    if CCD1ImgCapPath.find("Cap") != -1:
                        try:
                            shutil.copy(CCD1ImgCapPath, UpLoadCCD1ImgPathCap)
                            ErrMes.append(CCD1ImgCapPath + ":截图复制MES成功")
                            print("截图复制MES成功")
                        except:
                            ErrMes.append(CCD1ImgCapPath + ":截图复制MES失败")
                            print("截图复制MES失败")
                    # 图片转移
                    shutil.move(CCD1ImgCapPath, newCCD1ImgPathCap)
                    ErrMes.append(CCD1ImgCapPath + ":图片转移成功")
                    print("截图转移成功")
                except:
                    ErrMes.append(CCD1ImgCapPath + ":图片转移失败")
                    print("截图转移失败")
        else:
            ErrMes.append(SN + "," + VirtualSN + ":套图片不存在")
            print("套图片不存在")
        return ErrMes

    """
    ---文件移动---
    source:需要移动的文件
    dest:目标文件夹
    1.增加被移动文件的存在判断提示，及时发现问题
    2.当目标文件夹不存在时能够自动创建，减少工具执行失败概率
    3.当目标文件夹内存在同名文件时进行覆盖，减少工具执行失败概率
    4.移动失败时进行提示
    """

    def Movefile(self,source, dest):
        if (not os.path.exists(source)):
            GvVisionAssembly.ReportMessage("Cannot find the source folder!", noteType, False)
            return
        if (not os.path.exists(dest)):
            os.makedirs(dest)
        destfile = dest + "\\" + source.split("\\")[-1]
        if (os.path.exists(destfile)):
            try:
                os.remove(destfile)
            except OSError:
                GvVisionAssembly.ReportMessage("Remove file error!", noteType, False)
                return
        try:
            shutil.move(source, dest)
        except shutil.Error:
            GvVisionAssembly.ReportMessage("Move file error!", noteType, False)
            return

    """
    ---移动文件夹内所有文件---
    source:需要移动的文件夹
    dest:目标文件夹
    1.增加被移动文件的存在判断提示，及时发现问题
    2.当目标文件夹不存在时能够自动创建，减少工具执行失败概率
    3.支持多层文件夹转移
    4.移动失败时进行提示
    """

    def Movefiledir(self,source, dest):
        if (not os.path.exists(source)):
            GvVisionAssembly.ReportMessage("Cannot find the source folder!", noteType, False)
            return
        if (not os.path.exists(dest)):
            os.makedirs(dest)
        for file in os.listdir(source):
            rPath = os.path.join(source, file)
            if (os.path.isfile(rPath)):
                self.Movefile(source + "\\" + file, dest)
            elif (os.path.isdir(rPath)):
                self.Movefiledir(source + "\\" + file, dest + "\\" + file)
        if (len(os.listdir(source)) == 0):
            try:
                shutil.rmtree(source)
            except shutil.Error:
                GvVisionAssembly.ReportMessage("Remove filedir error!", noteType, False)
                return

    """
    ---文件复制---
    source:需要复制的文件
    dest:目标文件夹
    1.增加被复制文件的存在判断提示，及时发现问题
    2.当目标文件夹不存在时能够自动创建，减少工具执行失败概率
    3.当目标文件夹内存在同名文件时进行覆盖，减少工具执行失败概率
    4.复制失败时进行提示
    """

    def Copyfile(self,source, dest):
        if (not os.path.exists(source)):
            GvVisionAssembly.ReportMessage("Cannot find the source folder!", noteType, False)
            return
        if (not os.path.exists(dest)):
            os.makedirs(dest)
        destfile = dest + "\\" + source.split("\\")[-1]
        if (os.path.exists(destfile)):
            try:
                os.remove(destfile)
            except OSError:
                GvVisionAssembly.ReportMessage("Remove file error!", noteType, False)
                return
        try:
            shutil.copy(source, dest)
        except shutil.Error:
            GvVisionAssembly.ReportMessage("Copy file error!", noteType, False)
            return

    """
    ---复制文件夹内所有文件---
    source:需要移动的文件夹
    dest:目标文件夹
    label:筛选标签，只有文件名中带刺标签的才会被复制，置空默认为全部复制
    1.增加被复制文件的存在判断提示，及时发现问题
    2.当目标文件夹不存在时能够自动创建，减少工具执行失败概率
    3.支持多层文件夹复制
    4.复制失败时进行提示
    """

    def Copyfiledir(self,source, dest, label=""):
        if (not os.path.exists(source)):
            GvVisionAssembly.ReportMessage("Cannot find the source folder!", noteType, False)
            return
        if (not os.path.exists(dest)):
            os.makedirs(dest)
        for file in os.listdir(source):
            rPath = os.path.join(source, file)
            if (os.path.isfile(rPath)):
                if (label in file):
                    self.Copyfile(source + "\\" + file, dest)
            elif (os.path.isdir(rPath)):
                self.Copyfiledir(source + "\\" + file, dest + "\\" + file, label)

    """
    ---修改文件夹名---
    oldDir:修改前的文件夹名
    newDir:修改后的文件夹名
    1.增加被修改文件夹的存在判断提示，及时发现问题
    2.当目标文件夹已存在时能够自动覆盖，减少工具执行失败概率
    3.修改失败时进行提示
    """

    def Renamefiledir(self,oldDir, newDir):
        if (not os.path.exists(oldDir)):
            GvVisionAssembly.ReportMessage("Cannot find the source folder!", noteType, False)
            return
        if (os.path.exists(newDir)):
            try:
                shutil.rmtree(newDir)
            except shutil.Error:
                GvVisionAssembly.ReportMessage("Remove new filedir error!", noteType, False)
                return
        topPathDir = os.path.dirname(newDir)
        if (not os.path.exists(topPathDir)):
            os.makedirs(topPathDir)
        try:
            os.rename(oldDir, newDir)
        except OSError:
            GvVisionAssembly.ReportMessage("Rename filedir error!", noteType, False)
            return

    """
    ---等待文件保存完成---
    path:要等待检测的文件夹
    count:需要达到的文件数量
    TimeOut:最长等待时间,超时自动退出,默认1秒
    1.等待文件保存，直至路径path内有足够文件个数count或超时TimeOut为止
    2.增加被修改文件夹的存在判断提示，及时发现问题
    3.增加超时退出功能
    """

    def WaitingSave(self,path, count, TimeOut=1):
        startTime = time.time()
        while (1):

            if (not os.path.exists(path)):
                GvVisionAssembly.ReportMessage("Cannot find the folder!", noteType, False)
                return
            if (len(os.listdir(path)) >= count):
                return
            elif (time.time() - startTime > TimeOut):
                return
            else:
                time.sleep(0.01)
                pass