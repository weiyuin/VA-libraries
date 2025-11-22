import GvVisionAssembly as my_lib  # Thay tên file (bỏ đuôi .pyd)
import inspect

print("--- DANH SÁCH TẤT CẢ (Gồm cả biến hệ thống) ---")
print(dir(my_lib))

print("\n--- CHỈ LỌC RA CÁC HÀM VÀ CLASS ---")
# Lặp qua các thành phần để xem cái nào là hàm (function) hoặc lớp (class)
for name, obj in inspect.getmembers(my_lib):
    if inspect.isbuiltin(obj) or inspect.isfunction(obj):
        print(f"[Hàm]: {name}")
    elif inspect.isclass(obj):
        print(f"[Class]: {name}")