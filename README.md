# 🧠 VA-libraries

**Vision Assembly Programming Libraries**  
Thư viện Python hỗ trợ phát triển phần mềm thị giác máy trong dây chuyền lắp ráp, đặc biệt dùng cho các ứng dụng kiểm tra keo như trong dự án AirPods.

---

## 📚 Thư viện thành phần

| 📁 File Name            | 📝 Mô tả chức năng chính |
|------------------------|--------------------------|
| `GvGluePathAOI.py`     | Thư viện kiểm tra đường keo, xử lý dữ liệu, hiển thị kết quả và tương tác MES. |
| `GvAsyncLog.py`        | Ghi log bất đồng bộ, hỗ trợ nhiều file log, xoay log theo ngày. |
| `redirectstdout.py`    | Chuyển hướng `stdout` của Python sang DLL, hỗ trợ log GUI. |
| `ScFile.py`            | Xử lý file: tạo thư mục, di chuyển ảnh, nén/giải nén ZIP, xử lý CSV. |
| `ScFoolProof.py`       | Kiểm tra sai thao tác trong lắp ráp: góc giữa các đường, bán kính v.v. |
| `ScImageShow.py`       | Hiển thị đồ họa (text, line, circle, polygon) trong GvVision GUI. |
| `ScProtocol.py`        | Tính CRC, hỗ trợ giao tiếp dữ liệu qua giao thức tùy chỉnh. |
| `ScShape.py`           | Xử lý hình học: đa giác, offset, transform, line utility. |
| `ScMsgReport.py`       | Quản lý và hiển thị thông báo hệ thống (chức năng phụ trợ). |

---

## 🔧 Yêu cầu hệ thống

- Python 3.6+
- SDK **GvVisionAssembly** (nội bộ)
- Windows + Cài đặt DLL `RedirectPythonPrint.dll` (nếu dùng redirectstdout)

---

## 🚀 Ứng dụng thực tế

- ✅ Kiểm tra chất lượng keo trong lắp ráp AirPods 4/5.
- ✅ Hiển thị thông tin NG trực quan trên giao diện hình ảnh.
- ✅ Tích hợp MES, lưu trữ kết quả và ảnh kiểm tra.
- ✅ Tùy chỉnh hiển thị phù hợp từng khách hàng: 36/37/39.

---

## 📁 Cấu trúc repo (đề xuất)

```bash
VA-libraries/
│
├── GvGluePathAOI.py         # AOI chính - kiểm tra keo, hiển thị, MES
├── GvAsyncLog.py            # Logging async
├── redirectstdout.py        # Chuyển stdout qua DLL
├── ScFile.py                # Quản lý file, ảnh, zip
├── ScFoolProof.py           # Kiểm tra sai thao tác lắp ráp
├── ScImageShow.py           # Hiển thị đồ họa Vision
├── ScProtocol.py            # Giao tiếp & CRC
├── ScShape.py               # Hình học & offset
├── ScMsgReport.py           # (Phụ trợ GUI)
└── README.md                # Tài liệu này
