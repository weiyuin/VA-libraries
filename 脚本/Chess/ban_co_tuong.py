import GvVisionAssembly
from ScImageShow import ScImageShow

# ==============================================================================
# 1. KHỞI TẠO (Chuẩn bị tờ giấy vẽ)
# ==============================================================================
# Tạo mảng chứa các hình vẽ (guiArray)
guiArray = GvVisionAssembly.GcScriptGuiArray()

# Cấu hình vị trí và kích thước bàn cờ
GOC_X = 100       # Điểm bắt đầu vẽ (cách mép trái 100 pixel)
GOC_Y = 100       # Điểm bắt đầu vẽ (cách mép trên 100 pixel)
O_CO  = 80        # Kích thước một ô cờ (80x80 pixel)

# Định nghĩa màu sắc [Đỏ, Xanh lá, Xanh dương]
MAU_DEN      = [0, 0, 0]       # Màu đen (Vẽ đường kẻ)
MAU_DO       = [255, 0, 0]     # Màu đỏ (Quân Đỏ)
MAU_XANH_DEN = [0, 0, 255]     # Màu xanh (Quân Đen - dùng xanh để dễ đọc chữ)
MAU_DIEM     = [0, 128, 0]     # Màu xanh lá đậm (Vẽ dấu cộng giao điểm)

# ==============================================================================
# 2. HÀM TÍNH TỌA ĐỘ (Giúp tìm vị trí pixel trên màn hình)
# ==============================================================================
# Hàm này đổi từ vị trí cờ (cột 0, hàng 0) -> vị trí màn hình (pixel 100, 100)
def tinh_toa_do(cot, hang):
    pixel_x = GOC_X + (cot * O_CO)
    pixel_y = GOC_Y + (hang * O_CO)
    return GvVisionAssembly.sc2Vector(pixel_x, pixel_y)

# ==============================================================================
# 3. VẼ BÀN CỜ (Kẻ đường thẳng)
# ==============================================================================

# --- Vẽ 10 đường kẻ ngang ---
for hang in range(10):
    diem_trai = tinh_toa_do(0, hang)
    diem_phai = tinh_toa_do(8, hang)
    # Cú pháp: Class.TenHam(Class, guiArray, Diem1, Diem2, Mau, DoDay)
    ScImageShow.ImageShowLineSegVec(ScImageShow, guiArray, diem_trai, diem_phai, MAU_DEN, 2)

# --- Vẽ 9 đường kẻ dọc ---
for cot in range(9):
    if cot == 0 or cot == 8:
        # Hai đường biên trái/phải: Vẽ liền một mạch từ trên xuống dưới
        diem_tren = tinh_toa_do(cot, 0)
        diem_duoi = tinh_toa_do(cot, 9)
        ScImageShow.ImageShowLineSegVec(ScImageShow, guiArray, diem_tren, diem_duoi, MAU_DEN, 2)
    else:
        # Các đường ở giữa: Bị ngắt quãng bởi Sông (ở giữa hàng 4 và 5)
        # Nửa trên (Đất Đen)
        ScImageShow.ImageShowLineSegVec(ScImageShow, guiArray, tinh_toa_do(cot, 0), tinh_toa_do(cot, 4), MAU_DEN, 2)
        # Nửa dưới (Đất Đỏ)
        ScImageShow.ImageShowLineSegVec(ScImageShow, guiArray, tinh_toa_do(cot, 5), tinh_toa_do(cot, 9), MAU_DEN, 2)

# --- Vẽ Cung Tướng (Hai dấu chéo chữ X) ---
# Cung Tướng Đen (Trên)
ScImageShow.ImageShowLineSegVec(ScImageShow, guiArray, tinh_toa_do(3, 0), tinh_toa_do(5, 2), MAU_DEN, 2)
ScImageShow.ImageShowLineSegVec(ScImageShow, guiArray, tinh_toa_do(5, 0), tinh_toa_do(3, 2), MAU_DEN, 2)

# Cung Tướng Đỏ (Dưới)
ScImageShow.ImageShowLineSegVec(ScImageShow, guiArray, tinh_toa_do(3, 9), tinh_toa_do(5, 7), MAU_DEN, 2)
ScImageShow.ImageShowLineSegVec(ScImageShow, guiArray, tinh_toa_do(5, 9), tinh_toa_do(3, 7), MAU_DEN, 2)

# --- Viết chữ SỞ HÀ - HÁN GIỚI ---
# Vị trí giữa sông
ScImageShow.ImageShowTextXY(ScImageShow, guiArray, tinh_toa_do(2, 4).GetX(), tinh_toa_do(2, 4).GetY() + 20, "楚 河", MAU_DEN, 40, 0)
ScImageShow.ImageShowTextXY(ScImageShow, guiArray, tinh_toa_do(5, 4).GetX(), tinh_toa_do(5, 4).GetY() + 20, "漢 界", MAU_DEN, 40, 0)

# --- Vẽ dấu cộng (+) tại các giao điểm ---
for hang in range(10):
    for cot in range(9):
        vi_tri = tinh_toa_do(cot, hang)
        ScImageShow.ImagechowCrossVec(ScImageShow, guiArray, vi_tri, MAU_DIEM, 1)


# ==============================================================================
# 4. HÀM VẼ QUÂN CỜ
# ==============================================================================
def ve_quan(cot, hang, ten_quan, mau_sac):
    tam = tinh_toa_do(cot, hang)
    # 1. Vẽ vòng tròn
    ban_kinh = int(O_CO / 2 - 5)
    ScImageShow.ImageShowCircle(ScImageShow, guiArray, tam, ban_kinh, mau_sac, 2)
    
    # 2. Viết tên quân cờ (lùi lại xíu để chữ vào giữa)
    lech_x = 20
    lech_y = 15
    ScImageShow.ImageShowTextXY(ScImageShow, guiArray, tam.GetX() - lech_x, tam.GetY() - lech_y, ten_quan, mau_sac, 35, 0)

# ==============================================================================
# 5. ĐẶT QUÂN CỜ LÊN BÀN (Vị trí thực tế)
# ==============================================================================

# --- QUÂN ĐEN (Nửa trên - Màu Xanh Đen) ---
# Hàng 0: Xe - Mã - Tượng - Sĩ - Tướng - Sĩ - Tượng - Mã - Xe
ve_quan(0, 0, "車", MAU_XANH_DEN) # Xe
ve_quan(1, 0, "馬", MAU_XANH_DEN) # Mã
ve_quan(2, 0, "象", MAU_XANH_DEN) # Tượng
ve_quan(3, 0, "士", MAU_XANH_DEN) # Sĩ
ve_quan(4, 0, "將", MAU_XANH_DEN) # Tướng (Đen)
ve_quan(5, 0, "士", MAU_XANH_DEN)
ve_quan(6, 0, "象", MAU_XANH_DEN)
ve_quan(7, 0, "馬", MAU_XANH_DEN)
ve_quan(8, 0, "車", MAU_XANH_DEN)

# Hàng 2: Pháo
ve_quan(1, 2, "砲", MAU_XANH_DEN)
ve_quan(7, 2, "砲", MAU_XANH_DEN)

# Hàng 3: Tốt (5 con)
ve_quan(0, 3, "卒", MAU_XANH_DEN)
ve_quan(2, 3, "卒", MAU_XANH_DEN)
ve_quan(4, 3, "卒", MAU_XANH_DEN)
ve_quan(6, 3, "卒", MAU_XANH_DEN)
ve_quan(8, 3, "卒", MAU_XANH_DEN)


# --- QUÂN ĐỎ (Nửa dưới - Màu Đỏ) ---
# Hàng 9: Xe - Mã - Tượng - Sĩ - Tướng - Sĩ - Tượng - Mã - Xe
ve_quan(0, 9, "車", MAU_DO) # Xe
ve_quan(1, 9, "馬", MAU_DO) # Mã
ve_quan(2, 9, "相", MAU_DO) # Tượng (Đỏ)
ve_quan(3, 9, "仕", MAU_DO) # Sĩ (Đỏ)
ve_quan(4, 9, "帥", MAU_DO) # Soái (Đỏ)
ve_quan(5, 9, "仕", MAU_DO)
ve_quan(6, 9, "相", MAU_DO)
ve_quan(7, 9, "馬", MAU_DO)
ve_quan(8, 9, "車", MAU_DO)

# Hàng 7: Pháo
ve_quan(1, 7, "炮", MAU_DO)
ve_quan(7, 7, "炮", MAU_DO)

# Hàng 6: Tốt (5 con)
ve_quan(0, 6, "兵", MAU_DO)
ve_quan(2, 6, "兵", MAU_DO)
ve_quan(4, 6, "兵", MAU_DO)
ve_quan(6, 6, "兵", MAU_DO)
ve_quan(8, 6, "兵", MAU_DO)

# ==============================================================================
# 6. HIỂN THỊ LÊN MÀN HÌNH
# ==============================================================================
GvGuiDataAgent.SetGraphicDisplay("View-1", guiArray)