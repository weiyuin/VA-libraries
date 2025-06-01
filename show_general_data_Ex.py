    def show_general_data_Ex(self,guiArray,str_info,font_size=40,offset_x=50,offset_y=50,line_space=0,line_width=3,bShowMinWidth=True,b_show_cof=False,\
                            b_show_shifit=False,b_show_lenght=False,b_show_overflow=False,b_show_lackglue=False,show_OK=False,list_posx=None,list_posy=None):
        #所有信息均显示
        # -----------------------------
        # 检测结果合并
        # error_code
        # 	eOk = 0,        //	OK
        #	eTruefail,		//	严重
        #	eCOF			//	一般
        #obj = json.loads(str_info)
        obj=str_info
        obj=check_errorcode(obj,b_show_lackglue)
        # 基础信息
        obj_base = obj["base_info"]
        error_code = obj_base["error_code"]
        str_out = "Glue Check Result" ":" + glue_display.get_err_msg(error_code,b_show_cof)

        # 显示检测结果
        temp_font_size=font_size
        guiArray.Add(imageShowTextXY(offset_x,offset_y,str_out,glue_display.get_color(error_code,b_show_cof),font_size+temp_font_size))
        # 显示SN
        str_out = "SN:" + obj_base["SN"]
        guiArray.Add(imageShowTextXY(offset_x,offset_y+line_space+font_size+temp_font_size,str_out,glue_display.get_color(error_code,b_show_cof),font_size))
        # NG信息
        str_out_mes=""
        list_out_mes=[]
        # 分区域信息
        region_num = obj["base_info"]["region_number"]
        list_region=[]
        for i in range(region_num):
            list_region.append(i)
        obj_region = obj["region_info"]

        # NoGlue状态判断，当无胶时，所有显示检测项目均NG，有胶时正常显示
        nums = 1
        str_out_noglue="NoGlue:"
        str_out_noglue_errorcode=0
        if self.get_noglue_result(obj)==1:
            str_out_noglue=str_out_noglue+"OK"
            str_out_noglue_errorcode=0
        else:
            str_out_noglue=str_out_noglue+"NG"
            str_out_noglue_errorcode=1
            list_out_mes.append("NoGlue")
        guiArray.Add(imageShowTextXY(offset_x, offset_y + (line_space + font_size) * (nums + 2) + temp_font_size,str_out_noglue, glue_display.get_color(str_out_noglue_errorcode, b_show_cof), font_size, 2))
        #处理后续信息，当noglue时，所有检测项目均显示NG
        if str_out_noglue_errorcode==1:
            #占比/胶宽/面积信息，不用处理，本身NG
            #孔洞信息，需要处理，默认NG
            for i in range(region_num):
                index = "region_{index}".format(index=i)
                obj_hole = obj_region[index]["region_info_hole"]
                region_type = obj["region_info"][index]["info_base"]["type"]
                if obj_hole["enable"] == True and region_type == "normal":
                    obj_hole["error_code"]=1
            #断胶信息，需要处理，默认NG
            obj["detection_gap_info"]["num"]=999
            #溢胶信息，需要处理，默认NG
            for i in range(region_num):
                index = "region_{index}".format(index=i)
                region_type = obj["region_info"][index]["info_base"]["type"]
                if region_type != "normal" and obj_region[index]["region_info_area"]["enable"] == True:
                    obj_region[index]["region_info_area"]["error_code"]=1
            #偏移信息，需要处理，默认NG
            try:
                for i in range(region_num):
                    index = "region_{index}".format(index=i)
                    obj_shift = obj_region[index]["region_info_shift"]
                    obj_shiftX = obj_region[index]["region_info_shiftX"]
                    obj_shiftY = obj_region[index]["region_info_shiftY"]
                    region_type = obj["region_info"][index]["info_base"]["type"]
                    if obj_shift["enable"] == True and region_type == "normal":
                        obj_shift["error_code"]=1
                    if obj_shiftX["enable"] == True and region_type == "normal":
                        obj_shiftX["error_code"]=1
                    if obj_shiftY["enable"] == True and region_type == "normal":
                        obj_shiftY["error_code"]=1
            except:
                temp = 0  # 无意义
            #胶长信息，需要处理，默认NG
            try:
                for key in obj["glue_length_info"].keys():
                    if obj["glue_length_info"][key]["enable"] == True:
                        obj["glue_length_info"][key]["error_code"]=1
            except:
                temp = 0  # 无意义

        # 占比信息
        list_error_code=[]
        list_ng_region=[]
        error_codes=0
        for i in range(region_num):
            index = "region_{index}".format(index = list_region[i])
            obj_area_shift = obj_region[index]["region_info_areashift"]
            region_type = obj["region_info"][index]["info_base"]["type"]
            #print(region_type)
            if obj_area_shift["enable"]==True and region_type=="normal":
                list_error_code.append(obj_area_shift["error_code"])
                list_ng_region.append(i)
        if len(list_error_code)>0:
            nums=nums+1
            str_out_area_shirt="Glue coverage shift:"
            if sum(list_error_code)==0:
                str_out_area_shirt=str_out_area_shirt+"OK"
            else:
                if list_error_code.count(1)>0:
                    error_codes=1
                else:
                    error_codes=2
                #NG信息增加
                if (error_codes==2 and b_show_cof==True ) or error_codes==1:
                    list_out_mes.append("CoverageShift")
                #根据结果及是否显示COF来显示单项NG/OK信息
                if error_codes==2:
                    if b_show_cof==True:
                        str_out_area_shirt = str_out_area_shirt+"NG("
                    else:
                        str_out_area_shirt = str_out_area_shirt + "OK("
                if error_codes==1:
                    str_out_area_shirt = str_out_area_shirt + "NG("
                for i in range(0,len(list_error_code)):
                    if list_error_code[i]!=0:
                        str_out_area_shirt=str_out_area_shirt+"R"+str(list_ng_region[i]+1)+","
                str_out_area_shirt=str_out_area_shirt+")"
            guiArray.Add(imageShowTextXY(offset_x,offset_y+(line_space+font_size)*(nums+2)+temp_font_size,str_out_area_shirt,glue_display.get_color(error_codes,b_show_cof),font_size,2)) 

        # 孔洞信息
        list_error_code=[]
        list_ng_region=[]
        error_codes=0
        for i in range(region_num):
            index = "region_{index}".format(index = list_region[i])
            obj_hole = obj_region[index]["region_info_hole"]
            region_type = obj["region_info"][index]["info_base"]["type"]
            if obj_hole["enable"]==True and region_type=="normal" :
                list_error_code.append(obj_hole["error_code"])
                list_ng_region.append(i)
        if len(list_error_code)>0:
            nums=nums+1
            str_out_hole="Glue coverage hole:"
            if sum(list_error_code)==0:
                str_out_hole=str_out_hole+"OK"
            else:
                if list_error_code.count(1)>0:
                    error_codes=1
                else:
                    error_codes=2
                # NG信息增加
                if (error_codes == 2 and b_show_cof == True) or error_codes == 1:
                    list_out_mes.append("Hole")
                # 根据结果及是否显示COF来显示单项NG/OK信息
                if error_codes == 2:
                    if b_show_cof == True:
                        str_out_hole = str_out_hole + "NG("
                    else:
                        str_out_hole = str_out_hole + "OK("
                if error_codes == 1:
                    str_out_hole = str_out_hole + "NG("
                for i in range(0,len(list_error_code)):
                    if list_error_code[i]!=0:
                        str_out_hole=str_out_hole+"R"+str(list_ng_region[i]+1)+","
                str_out_hole=str_out_hole+")"
            guiArray.Add(imageShowTextXY(offset_x,offset_y+(line_space+font_size)*(nums+2)+temp_font_size,str_out_hole,glue_display.get_color(error_codes,b_show_cof),font_size,2))    
        
        ####面积与宽度统一归类为GlueMissing
        # 面积信息
        list_error_code=[]
        list_ng_region=[]
        error_codes=0
        for i in range(region_num):
            index = "region_{index}".format(index = list_region[i])
            obj_area = obj_region[index]["region_info_area"]
            region_type = obj["region_info"][index]["info_base"]["type"]
            if obj_area["enable"]==True and region_type=="normal":
                list_error_code.append(obj_area["error_code"])
                list_ng_region.append(i)
        # 胶宽信息
        list_error_code1=[]
        list_ng_region1=[]
        for i in range(region_num):
            index = "region_{index}".format(index = list_region[i])
            obj_width = obj_region[index]["region_info_width"]
            region_type = obj["region_info"][index]["info_base"]["type"]
            if obj_width["enable"]==True and region_type=="normal":
                list_error_code1.append(obj_width["error_code"])
                list_ng_region1.append(i)
                # 最短胶宽及位置显示
                min_x_start=obj_width["min_start_pt"]["x"]
                min_y_start=obj_width["min_start_pt"]["y"]
                min_x_end=obj_width["min_end_pt"]["x"]
                min_y_end=obj_width["min_end_pt"]["y"]                                
                if self.n_mirror_mode == 1:
                    min_x_start = self.n_image_width - min_x_start
                    min_x_end = self.n_image_width - min_x_end                    
                elif self.n_mirror_mode == 2: 
                    min_y_start = self.n_image_height - min_y_start
                    min_y_end = self.n_image_height - min_y_end
                pt1=GvVisionAssembly.sc2Vector(min_x_start,min_y_start)
                pt2=GvVisionAssembly.sc2Vector(min_x_end,min_y_end)
                lineSeg=GvVisionAssembly.scLineSeg(pt1,pt2)
                str_min_width_out="{min_width}".format(min_width=round(obj_width["min_val"],self.n_format))
                if obj_width["min_val"]==0.0:
                    pos_x=obj_region[index]["info_base"]["position"]["x"]+30
                    pos_y=obj_region[index]["info_base"]["position"]["y"]+30
                else:
                    pos_x=(min_x_start+min_x_end)/2+5
                    pos_y=(min_y_start+min_y_end)/2
                temp=abs(font_size-10)
                if temp<8:
                    temp=8
                ###是否显示最短胶宽 
                if bShowMinWidth==True:
                    guiArray.Add(ShowLineSeg(lineSeg,glue_display.get_color(obj_width["error_code"],b_show_cof),0,2))
                    guiArray.Add(imageShowTextXY(pos_x,pos_y,str_min_width_out,glue_display.get_color(obj_width["error_code"],b_show_cof),temp,2))
        #面积与宽度信息合并，先面积后宽度
        list_error_code.extend(list_error_code1)   
        list_ng_region.extend(list_ng_region1)        
        if len(list_error_code)>0:
            nums=nums+1
            str_out_width="Glue missing:"
            if sum(list_error_code)==0:
                str_out_width=str_out_width+"OK"
            else:
                if list_error_code.count(1)>0:
                    error_codes=1
                else:
                    error_codes=2
                #NG原因新增
                if error_codes==1 or (error_codes==2 and b_show_cof==True):
                    list_out_mes.append("GlueMissing")
                #根据结果及是否显示COF来显示单项NG / OK信息
                if error_codes==2:
                    if b_show_cof==True:
                        str_out_width=str_out_width+"NG("
                    else:
                        str_out_width=str_out_width+"OK("
                if error_codes==1:
                    str_out_width = str_out_width + "NG("
                for i in range(0,len(list_error_code)):
                    if list_error_code[i]!=0:
                        str_out_width=str_out_width+"R"+str(list_ng_region[i]+1)+","
                str_out_width=str_out_width+")"
            guiArray.Add(imageShowTextXY(offset_x,offset_y+(line_space+font_size)*(nums+2)+temp_font_size,str_out_width,glue_display.get_color(error_codes,b_show_cof),font_size,2))

        # 偏移信息
        list_error_code=[]
        list_ng_region=[]
        error_codes=0
        for i in range(region_num):
            index = "region_{index}".format(index = list_region[i])
            obj_shift = obj_region[index]["region_info_shift"]
            region_type = obj["region_info"][index]["info_base"]["type"]
            #距离判断
            if obj_shift["enable"]==True and region_type=="normal":
                list_error_code.append(obj_shift["error_code"])
                if obj_shift["error_code"]>0:
                    list_ng_region.append(i)
            #X距离判断
            try:
                obj_shiftX = obj_region[index]["region_info_shiftX"]
                if obj_shiftX["enable"]==True and region_type=="normal":
                    list_error_code.append(obj_shiftX["error_code"])
                    if obj_shiftX["error_code"]>0 and list_ng_region.count(i)==0:
                        list_ng_region.append(i)
            except:
                temp=0#无意义 
            #Y距离判断
            try:
                obj_shiftY = obj_region[index]["region_info_shiftY"]
                if obj_shiftY["enable"]==True and region_type=="normal":
                    list_error_code.append(obj_shiftY["error_code"])
                    if obj_shiftY["error_code"]>0 and list_ng_region.count(i)==0:
                        list_ng_region.append(i)
            except:
                temp=0#无意义 
        if len(list_error_code)>0 and b_show_shifit==True:
            nums=nums+1
            str_out_shift="Glue shift:"
            if sum(list_error_code)==0:
                str_out_shift=str_out_shift+"OK"
            else:
                list_ng_region.sort()
                if list_error_code.count(1)>0:
                    error_codes=1
                    str_out_shift=str_out_shift+"NG("
                else:
                    error_codes=2
                if (error_codes!=2 and b_show_cof!=True ) or b_show_cof==True:
                    list_out_mes.append("Shift")
                if error_codes==2: 
                    if b_show_cof==True:
                        str_out_shift=str_out_shift+"NG("
                    else:
                        str_out_shift=str_out_shift+"OK("
                for i in range(0,len(list_ng_region)):
                    str_out_shift=str_out_shift+"R"+str(list_ng_region[i]+1)+","
                str_out_shift=str_out_shift+")"
            guiArray.Add(imageShowTextXY(offset_x,offset_y+(line_space+font_size)*(nums+2)+temp_font_size,str_out_shift,glue_display.get_color(error_codes,b_show_cof),font_size,2))             

        # 断胶信息及轮廓
        if self.b_show_broken==True:
            nums=nums+1
            num_brocken=obj["detection_gap_info"]["num"]
            str_out_brocken="Glue path broken:"
            error_codes=0
            if num_brocken>0:#存在断胶
                error_codes=obj_base["error_code"]
                str_out_brocken=str_out_brocken+"NG"
                list_out_mes.append("Broken")
                ###显示NG区域及长度
                try:
                    for i in range(num_brocken):
                        index = "{index}".format(index = i)
                        broken_length=obj["detection_gap_info"][index]["info"]["width"]
                        str_out_brocken_length="{broken_data}".format(broken_data=round(broken_length,self.n_format))
                        start_x=obj["detection_gap_info"][index]["info"]["start_pt"]["X"]
                        start_y=obj["detection_gap_info"][index]["info"]["start_pt"]["Y"]
                        end_x=obj["detection_gap_info"][index]["info"]["end_pt"]["X"]
                        end_y=obj["detection_gap_info"][index]["info"]["end_pt"]["Y"]
                        if self.n_mirror_mode == 1:
                            start_x = self.n_image_width - start_x
                            end_x = self.n_image_width - end_x
                        elif self.n_mirror_mode == 2:
                            start_y = self.n_image_height - start_y
                            end_y = self.n_image_height - end_y
                        scVecVec = GvVisionAssembly.sc2VectorVec()
                        for key in obj["detection_gap_info"][index]["contour"].keys():
                            temp_x=obj["detection_gap_info"][index]["contour"][key]["X"]
                            temp_y=obj["detection_gap_info"][index]["contour"][key]["Y"]
                            if self.n_mirror_mode == 1:
                                temp_x = self.n_image_width - temp_x
                            elif self.n_mirror_mode == 2:
                                temp_y = self.n_image_height - temp_y
                            pt = GvVisionAssembly.sc2Vector(temp_x,temp_y)
                            scVecVec.append(pt)
                        guiArray.Add(imageShowPolyline(scVecVec,[255,0,0],line_width))
                        guiArray.Add(imageShowTextXY((start_x+end_x)/2,(end_y+start_y)/2,str_out_brocken_length,glue_display.get_color(1,b_show_cof),font_size))
                except:
                    temp=0#无意义
            else:#不存在断胶
                str_out_brocken=str_out_brocken+"OK"
            guiArray.Add(imageShowTextXY(offset_x,offset_y+(line_space+font_size)*(nums+2)+temp_font_size,str_out_brocken,glue_display.get_color(error_codes,b_show_cof),font_size,2))
        
        # 溢胶信息及轮廓，启用显示，不启用显示
        #判断是否有溢胶区域
        overflow_region_num=0
        error_codes_list=[]
        for i in range(0,obj["base_info"]["region_number"]):
            index = "region_{index}".format(index = i)
            region_type = obj["region_info"][index]["info_base"]["type"]
            #溢胶区域判断
            if region_type!="normal" and obj_region[index]["region_info_area"]["enable"]==True:
                overflow_region_num=overflow_region_num+1
                error_codes_list.append(obj_region[index]["region_info_area"]["error_code"])
        #有溢胶区域才进行显示
        if overflow_region_num>0 and b_show_overflow==True:
            nums=nums+1
            num_overflow=obj["detection_overflow_info"]["num"]
            str_out_overflow="Overflow:"
            error_codes=0
            if num_overflow>0:
            #error_codes状态判断
                if error_codes_list.count(1)>0:
                    error_codes=1
                else:
                    error_codes=2
                tempdatas=0
                str_out_overflow=str_out_overflow+"NG"
                if error_codes==2: 
                    if b_show_cof!=True:
                        str_out_overflow="Overflow:OK"
                if b_show_cof==True or error_codes==1:
                    list_out_mes.append("Overflow")
                ###溢胶序号排序
                startIndex=0
                for i in range(0,obj["base_info"]["region_number"]):
                    key ="region_{index}".format(index = i)   
                    region_type = obj["region_info"][key]["info_base"]["type"]
                    if region_type =="normal":
                        startIndex=startIndex+1
                ###计算溢胶面积，各区域单独输出
                str_area_overflow=[]
                list_error_code=[]
                for i in range(0,obj["base_info"]["region_number"]):
                    if i<startIndex:
                        continue
                    key ="region_{index}".format(index = i)
                    region_type = obj["region_info"][key]["info_base"]["type"]
                    if region_type=="overflow":
                        list_error_code.append(obj["region_info"][key]["info_base"]["error_code"])
                        if obj["region_info"][key]["info_base"]["error_code"]>0:
                            val=round(obj["region_info"][key]["region_info_area"]["current_val"],self.n_format)
                            lsl=round(obj["region_info"][key]["region_info_area"]["lower_spec"],2)
                            usl=round(obj["region_info"][key]["region_info_area"]["upper_spec"],2)
                            str_temp_data="OF{index}".format(index = (i+1-startIndex))+": {overflow_data}({LSL_data},{USL_data})".format(overflow_data=val,LSL_data=lsl,USL_data=usl)
                            str_area_overflow.append(str_temp_data)
                if list_error_code.count(1)>0:
                    error_codes=1
                ###显示NG区域轮廓
                try:
                    for i in range(num_overflow):
                        index = "{index}".format(index = i)               
                        scVecVec = GvVisionAssembly.sc2VectorVec()
                        for key in obj["detection_overflow_info"][index]["contour"].keys():
                            temp_x=obj["detection_overflow_info"][index]["contour"][key]["X"]
                            temp_y=obj["detection_overflow_info"][index]["contour"][key]["Y"]
                            if self.n_mirror_mode == 1:
                                temp_x = self.n_image_width - temp_x          
                            elif self.n_mirror_mode == 2: 
                                temp_y = self.n_image_height - temp_y
                            pt = GvVisionAssembly.sc2Vector(temp_x,temp_y)
                            scVecVec.append(pt)
                        #if b_show_cof==True:
                        guiArray.Add(imageShowPolyline(scVecVec,glue_display.get_color(error_codes,b_show_cof),line_width))
                except:
                    print("No Counter")
                #并入溢胶面积
                #if len(str_area_overflow)>0 and b_show_cof==True:
                if len(str_area_overflow)>0:
                    str_out_overflow=str_out_overflow+"("
                    for str_data in str_area_overflow:
                        str_out_overflow=str_out_overflow+str_data+","
                    str_out_overflow=str_out_overflow+")"
            else:
                str_out_overflow=str_out_overflow+"OK"
            guiArray.Add(imageShowTextXY(offset_x,offset_y+(line_space+font_size)*(nums+2)+temp_font_size,str_out_overflow,glue_display.get_color(error_codes,b_show_cof),font_size,2))

        # 胶长信息
        list_error_code=[]
        str_length=[]
        enable_flage=False
        error_codes=0
        str_out_length="Gluelength:"
        lenght_index=0
        for key in obj["glue_length_info"].keys():
            lenght_index=lenght_index+1
            if obj["glue_length_info"][key]["enable"]==True:
                enable_flage=True
                if obj["glue_length_info"][key]["error_code"]>0:
                    list_error_code.append(obj["glue_length_info"][key]["error_code"])
                    lengh_dat=round(obj["glue_length_info"][key]["current_val"],self.n_format)
                    lsl=round(obj["glue_length_info"][key]["lower_spec"],2)
                    usl=round(obj["glue_length_info"][key]["upper_spec"],2)
                    str_temp_data="Length"+str(lenght_index)+":{lenght}({LSL_data},{USL_data})".format(lenght=lengh_dat,LSL_data=lsl,USL_data=usl)
                    str_length.append(str_temp_data)  
        #启用显示，不启用显示
        if enable_flage==True and b_show_lenght==True:
            if len(list_error_code)>0:
                if list_error_code.count(1)>0:
                    error_codes=1
                else:
                    error_codes=2
                str_out_length=str_out_length+"NG"
                if error_codes==2: 
                    if b_show_cof!=True:
                        str_out_length="Gluelength:OK"
                if (error_codes!=2 and b_show_cof!=True ) or b_show_cof==True:
                    list_out_mes.append("Gluelength")
                #if error_codes>0 and b_show_cof==True:
                if error_codes>0:
                    str_out_length=str_out_length+"("
                    for str_data in str_length:
                        str_out_length=str_out_length+str_data+","
                    str_out_length=str_out_length+")"
            else:
                str_out_length=str_out_length+"OK"
            nums=nums+1
            guiArray.Add(imageShowTextXY(offset_x,offset_y+(line_space+font_size)*(nums+2)+temp_font_size,str_out_length,glue_display.get_color(error_codes,b_show_cof),font_size,2))
        
        #缺胶信息
        if b_show_lackglue==True:
            show_errorcode=0
            nums=nums+1
            num_LackGlue=obj["detection_less_info"]["num"]
            str_out_LackGlue="LessGlue:"
            if num_LackGlue>0:
                list_out_mes.append("LessGlue")
                str_out_LackGlue=str_out_LackGlue+"NG"
                show_errorcode=1
            else:
                str_out_LackGlue=str_out_LackGlue+"OK"
            guiArray.Add(imageShowTextXY(offset_x,offset_y+(line_space+font_size)*(nums+2)+temp_font_size,str_out_LackGlue,glue_display.get_color(show_errorcode,b_show_cof),font_size,2))
        
        #NG信息  
        if len(list_out_mes)>0:
            str_out_mes="NG reason:"
            for i in list_out_mes:
                str_out_mes=str_out_mes+i+"/"
        guiArray.Add(imageShowTextXY(offset_x,offset_y+(line_space+font_size)*2+temp_font_size,str_out_mes,glue_display.get_color(error_code = obj_base["error_code"],b_show_cof=b_show_cof),font_size))       
        #显示检测区域
        font_size_ng=int(font_size/2)
        if font_size_ng<8:
            font_size_ng=8
        guiArray=self.show_detetion_Region(guiArray,obj,list_region,show_OK,font_size_ng,line_width,b_show_cof)
        #显示NG信息
        font_size_ng=int(font_size/2)
        if font_size_ng<8:
            font_size_ng=8
        for region_index in list_region:
            if list_posx==None:
                offset_x=0
            else:
                try:
                    offset_x=list_posx[region_index]
                except:
                    offset_x=0
            if list_posy==None:
                offset_y=0
            else:
                try:
                    offset_y=list_posy[region_index]
                except:
                    offset_y=0
            guiArray=self.show_NG_data(guiArray,obj,region_index,font_size_ng,offset_x,offset_y,line_space,b_show_cof)
        #显示处理
        
        return guiArray 