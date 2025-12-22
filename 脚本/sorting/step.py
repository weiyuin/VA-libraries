a = GvVar.GetVar("#strSortedIndices")
L0 = GvVar.GetVar("#L0")

b = a.split(",")
pos = b[L0]
pos = int(b[L0])

print(b)
print(a)
print(L0)
print(type(pos))
print("Vi tri hien tai" + str(pos))

GvVar.SetVar("#step",pos)