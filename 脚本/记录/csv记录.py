import time
import os

def WriteFile(path, filename, header, data):
    # Nếu thư mục chưa tồn tại thì tạo mới
    if not os.path.exists(path):
        os.makedirs(path)
    if not os.path.exists(path + filename):
        file = open(path + filename, "a", encoding="utf-8")
        file.write(header)
        file.write(data)
        file.close()
    else:
        file = open(path + filename, "a", encoding="utf-8")
        file.write(data)
        file.close()

path = "D:\\LOG\\"
filename = time.strftime("%Y-%m-%d.csv", time.localtime())
header = "SN;n;Distance;Angle\n"

strSN = GvVar.GetVar("#strSN")
n = GvVar.GetVar("#n")
dDistance = GvVar.GetVar("#dDistance")
dAngle = GvVar.GetVar("#dAngle")
data = "{:s};{:d};{:3f};{:3f}\n".format(strSN,n,dDistance,dAngle)    

WriteFile(path, filename, header, data)

print(data)