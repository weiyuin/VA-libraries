import GvVisionAssembly

# 1. Lấy dữ liệu (Ví dụ 6 hàng 7 cột = 42 con)
search_array = GvTool.GetToolData("几何定位_002.搜索坐标数组")
num_elements = len(search_array)
delta_y = 20 # Khoảng cách Y tối đa giữa 2 con trong cùng 1 hàng (pixel)

# 2. Tạo danh sách dữ liệu kèm index gốc
data_list = []
for i in range(num_elements):
    data_list.append({
        'index': i, 
        'x': search_array[i].GetX(), 
        'y': search_array[i].GetY()
    })

# 3. Sắp xếp toàn bộ theo Y
data_list.sort(key=lambda p: p['y'])

# 4. Phân cụm hàng dựa trên delta_y
all_rows = []
if num_elements > 0:
    current_row = [data_list[0]]
    for i in range(1, num_elements):
        # Nếu con hiện tại cách con trước đó < delta_y -> Cùng hàng
        if abs(data_list[i]['y'] - data_list[i-1]['y']) < delta_y:
            current_row.append(data_list[i])
        else:
            # Nếu cách xa -> Sang hàng mới. Trước khi sang hàng mới, sort X hàng cũ
            current_row.sort(key=lambda p: p['x'])
            all_rows.append(current_row)
            current_row = [data_list[i]]
    
    # Sort X cho hàng cuối cùng và thêm vào danh sách
    current_row.sort(key=lambda p: p['x'])
    all_rows.append(current_row)

# 5. Nối tất cả các hàng lại thành mảng kết quả cuối cùng
final_sorted_list = []
for row in all_rows:
    final_sorted_list.extend(row)

# 6. Trích xuất Index và Tọa độ
sorted_indices = [p['index'] for p in final_sorted_list]
print(type(sorted_indices))
# Lưu biến để debug
GvVar.SetVar("#strSortedIndices", ",".join(map(str, sorted_indices)))
GvVar.SetVar("#nActualFound", num_elements) # Lưu số lượng thực tế tìm được

print("Số lượng tìm thấy: ", num_elements)
print("Thứ tự Index sau sắp xếp: ", sorted_indices)