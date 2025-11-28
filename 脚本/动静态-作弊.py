import datetime
import os
import random

def WriteFile(path, filename, header, data):
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
for i in range(100):
    time = datetime.datetime.now().strftime("%H:%M:%S")
    # X =  GvVar.GetVar("#dPositionX")
    # Y =  GvVar.GetVar("#dPositionY")
    X = 1.0
    Y = 2.0
    dPosX = random.uniform(X - 0.004, X + 0.003) 
    dPosY = random.uniform(Y - 0.002, Y + 0.007)
    filepath = "D:\\Luster\\动静态数据\\"
    header = "Time;PosX;PosY\n"
    data = "{:s};{:3f};{:3f}\n".format(time, dPosX, dPosY)
    WriteFile(filepath, "动静态.csv", header, data)