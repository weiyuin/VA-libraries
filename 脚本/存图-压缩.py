from ScFile import ScFile
import time
import os

# Tạo ngày giờ hiện tại của hệ thống
strCurDate = GvVar.GetVar("#strYearTime")
strCurentTime = GvVar.GetVar("#strCurTime")
struploadpath = GvVar.GetVar("#struploadpath")
strupload = GvVar.GetVar("#strIsupload")
sn = GvVar.GetVar("#strSN")
Local = GvVar.GetVar("@Local")[:2]
folderpth = Local + "\\IMG\\{}".format(strCurDate)
strStationID = GvVar.GetVar("#strStationID")
ScFile.mkdirFolder(folderpth)                   # Tạo thư mục ngày nếu chưa có

# Đường dẫn nén (sẽ được cập nhật lại)
struploadpath = Local + "\\GVIMAGES\\MES\\{date}\\{isupload}\\{SN}\\".format(date=strCurDate, SN=sn, isupload=strupload)
GvVar.SetVar("#struploadpath", struploadpath)

############################################################ Đợi đủ ảnh rồi mới nén
LSL = 1                                         # Số lượng ảnh tối thiểu phải có (ít nhất 1 tấm)
nSavenumber = GvVar.GetVar("@nSavenumber")      # Số lần kiểm tra tối đa (số vòng lặp)
dSavetime = GvVar.GetVar("@dSavetime")          # Thời gian ngủ giữa các lần kiểm tra (giây)

# Kiểm tra số lượng ảnh trong thư mục và đợi đến khi đủ
for a in range(0, nSavenumber):
    ImagePcs = 0	
    files = os.listdir(struploadpath)	
    for i in files:	
        if i.endswith(".jpg") or i.endswith(".bmp"):	
            ImagePcs += 1	
    print(ImagePcs)	
    if ImagePcs >= int(LSL):	
        break                   # Đủ ảnh → thoát vòng lặp ngay
    else:	
        time.sleep(dSavetime)   # Chưa đủ → đợi một khoảng rồi kiểm tra lại

##############################################################
# Nếu chạy hàng MES thì tiến hành nén ảnh lại thành file .zip
if strupload != "OFF":
    zip_file_path = Local + "\\IMG\\{}\\".format(strCurDate)
    try:
        isExists = os.path.exists(zip_file_path)
        # Nếu thư mục ngày chưa tồn tại thì tạo mới
        if not isExists:
            os.makedirs(zip_file_path)
    except:
        print(12)   # In mã lỗi nếu tạo thư mục thất bại

    # Tạo tên file zip theo định dạng: SN_StationID_Thời gian hoặc SN_Thời gian
    if strStationID != "":
        zip_name = Local + "\\IMG\\{}\\{}_{}_{}.zip".format(strCurDate, sn, strStationID, strCurentTime)
    else:
        zip_name = Local + "\\IMG\\{}\\{}_{}.zip".format(strCurDate, sn, strCurentTime)
        
    # Thực hiện nén toàn bộ thư mục ảnh của SN này thành 1 file zip duy nhất
    ScFile.Sczip_file(ScFile, struploadpath, zip_name)