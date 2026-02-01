#引导点超限判断
str_Flowpath=GvVar.GetVar("#str_Flowpath")
SendX,SendY=GvVar.GetVar("#SendX"),GvVar.GetVar("#SendY")

Spec_Down=GvVar.GetVar("#dbasepoint_down")
Spec_Up=GvVar.GetVar("#dbasepoint_up")


#左
if str_Flowpath=="L":
    BaseX,BaseY=GvVar.GetVar("#dbasepointX_1"),GvVar.GetVar("#dbasepointY_1")
    print("LX:",SendX,"(",BaseX+Spec_Down,",",BaseX+Spec_Up,")","   LY:",SendY,"(",BaseY+Spec_Down,",",BaseY+Spec_Up,")")
    if GvVar.GetVar("#bGlueJudge1")==True:
        if SendX<=(BaseX+Spec_Up) and SendX>=(BaseX+Spec_Down) and SendY<=(BaseY+Spec_Up) and SendY>=(BaseY+Spec_Down):
            state_L=True
        else:
            state_L=False
    else:
        state_L=True
    GvVar.SetVar("#bStartPointState",state_L)

#右
if str_Flowpath=="R":
    BaseX,BaseY=GvVar.GetVar("#dbasepointX_2"),GvVar.GetVar("#dbasepointY_2")
    print("RX:",SendX,"(",BaseX+Spec_Down,",",BaseX+Spec_Up,")","    RY:",SendY,"(",BaseY+Spec_Down,",",BaseY+Spec_Up,")")
    if GvVar.GetVar("#bGlueJudge2")==True:
        if SendX<=(BaseX+Spec_Up) and SendX>=(BaseX+Spec_Down) and SendY<=(BaseY+Spec_Up) and SendY>=(BaseY+Spec_Down):
            state_R=True
        else:
            state_R=False
    else:
        state_R=True
    GvVar.SetVar("#bStartPointState",state_R)